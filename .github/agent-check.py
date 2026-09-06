# Generated from shared agent rules; local commits refresh this file automatically.
#!/usr/bin/env python3
"""Machine-wide Git checks, independent of which assistant invokes Git."""
import json,os,re,subprocess,sys
from pathlib import Path
TYPES="feat|fix|docs|refactor|test|chore"
BRANCH=re.compile(r"^(?:"+TYPES+r")/[a-z0-9][a-z0-9._/-]*$")
MESSAGE=re.compile(r"^(?:"+TYPES+r")(?:\([^)\n]+\))?!?: \S.+$")
CODE={".py",".js",".jsx",".ts",".tsx",".php",".go",".rs",".swift",".sh",".sql",".vue",".svelte",".html",".css",".scss",".toml",".json",".yaml",".yml"}

def git(*args):
    p=subprocess.run(["git",*args],capture_output=True)
    if p.returncode: raise RuntimeError(p.stderr.decode(errors="replace").strip())
    return p.stdout.decode(errors="replace")

def reserved(root):
    return "fleet" in root.parts or "air-translate" in root.parts

def staged_errors(ci=False):
    errors=[]
    branch=os.environ.get("GITHUB_HEAD_REF") or os.environ.get("BITBUCKET_BRANCH") or git("branch","--show-current").strip()
    default=git("symbolic-ref","--quiet","--short","refs/remotes/origin/HEAD").strip().split("/")[-1] if subprocess.run(["git","symbolic-ref","--quiet","refs/remotes/origin/HEAD"],capture_output=True).returncode==0 else "main"
    if not ci and (branch in {"main","master",default} or not BRANCH.fullmatch(branch)):errors.append("Use a branch named type/short-name; never commit on the default branch.")
    base=os.environ.get("AGENT_RULES_BASE")
    if ci and base:entries=git("diff",base+"...HEAD","--name-only","--diff-filter=ACMRT","-z").split("\0")
    elif ci:entries=git("ls-files","-z").split("\0")
    else:entries=git("diff","--cached","--name-only","--diff-filter=ACMRT","-z").split("\0")
    if ci and os.environ.get("GITHUB_EVENT_PATH"):
        event=json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
        pr=event.get("pull_request")
        if pr and not MESSAGE.fullmatch(pr.get("title","")):errors.append("PR title must be type: short outcome (optional scope).")
        if pr and not BRANCH.fullmatch(pr.get("head",{}).get("ref","")):errors.append("PR branch must be type/short-name.")
    changed=[n for n in entries if n]
    has_code=any(Path(n).suffix in CODE and not n.startswith(("docs/",".github/")) for n in changed)
    if has_code and (not ci or base) and "CHANGELOG.md" not in changed:errors.append("Code changed without an accompanying CHANGELOG.md entry.")
    for n in changed:
        p=Path(n)
        if (p.name.startswith(".env") and not p.name.endswith((".example",".sample",".template"))) or p.suffix in {".pem",".p12",".pfx",".key"}:errors.append(n+": credential-like file must stay untracked.")
        if any(x in p.parts for x in {"node_modules",".venv","venv","__pycache__"}):errors.append(n+": generated dependencies must stay untracked.")
        mode=git("ls-files","--stage","--",n).split(" ",1)[0]
        if mode=="160000":errors.append(n+": nested repositories must not be staged.")
        if p.name.lower()=="claude.md" and not any(part in p.parts for part in {"fixtures","testdata"}):
            if mode!="120000" or git("show",":"+n).strip()!="AGENTS.md":errors.append(n+": must link to the sibling AGENTS.md, not contain a second guide.")
        if p.suffix in {".md",".mdc",".sh",".py",".json",".toml",".yaml",".yml"}:
            diff=git("diff",base+"...HEAD","--unified=0","--",n) if ci and base else ("" if ci else git("diff","--cached","--unified=0","--",n))
            if any(re.search(("/"+"Users/"+r"[^/\s]+/"),line) for line in diff.splitlines() if line.startswith("+") and not line.startswith("+++")):
                errors.append(n+": added an account-specific home path; use ~/ or $HOME.")
    for n in ["README.md","AGENTS.md","CHANGELOG.md"]:
        if subprocess.run(["git","cat-file","-e",":"+n],capture_output=True).returncode:errors.append(n+": missing from the proposed commit; use docs-standard to set up the project.")
    return errors

def main():
    try:root=Path(git("rev-parse","--show-toplevel").strip())
    except RuntimeError:return 0
    if reserved(root):return 0
    event=sys.argv[1] if len(sys.argv)>1 else "pre-commit"
    errors=[]
    try:
        if event=="pre-commit":
            # The installed source refreshes only its own generated CI files.
            helper=Path(__file__).with_name("sync_ci.py")
            if helper.is_file():subprocess.run([sys.executable,str(helper),str(root),"--stage"],check=True)
            errors=staged_errors()
        elif event=="ci":errors=staged_errors(ci=True)
        elif event=="commit-msg":
            title=Path(sys.argv[2]).read_text().splitlines()[0]
            if not MESSAGE.fullmatch(title) and not title.startswith(("Merge ","Revert ")):errors.append("Commit title must be type: short outcome (optional scope).")
        elif event=="pre-push":
            for line in sys.stdin:
                local,oid,remote,old=line.split()
                if set(oid)=={"0"}:continue
                if local.startswith("refs/heads/") and not BRANCH.fullmatch(local[len("refs/heads/"):]):errors.append("Push a type/short-name branch; merge default-branch changes through review.")
                if local.startswith("refs/tags/"):
                    if not re.fullmatch(r"refs/tags/v\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?",local):errors.append("Release tags must use vMAJOR.MINOR.PATCH.")
                    if set(old)!={"0"} and old!=oid:errors.append("Published release tags must never move.")
    except (RuntimeError,ValueError,IndexError) as e:errors.append(str(e))
    for error in errors:print("shared-agent-rules: "+error,file=sys.stderr)
    return 1 if errors else 0

if __name__=="__main__":sys.exit(main())
