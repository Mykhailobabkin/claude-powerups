#!/usr/bin/env python3
"""Shared checks: --staged reads the index; --committed reads HEAD, never working edits."""
import argparse, re, subprocess, sys
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

HEADINGS = ['Docs map','Architecture','Key Files','Patterns & Conventions','Deploy','Dev Commands','Gotchas']
REQUIRED = ['README.md','CLAUDE.md','CHANGELOG.md','docs/README.md','docs/project.md']
IGNORED_DIRS = {'.git','node_modules','vendor','.venv','venv','dist','build','.next','__pycache__','.worktrees','.superpowers'}

def git(root, *args):
    p = subprocess.run(['git','-C',str(root),*args],capture_output=True)
    if p.returncode: raise RuntimeError(p.stderr.decode(errors='replace').strip())
    return p.stdout

def check(root, staged=False, base=None, committed=False):
    errors, warnings = [], []
    snapshot = staged or committed
    listing = git(root,'ls-tree','-r','--name-only','-z','HEAD') if committed else git(root,'ls-files','-z')
    tracked = set(listing.decode().split('\0')) - {''}
    if snapshot:
        def read(name):
            return git(root,'show',('HEAD:' if committed else ':')+name).decode('utf-8',errors='replace')
        names = tracked
    else:
        def read(name): return (root/name).read_text(errors='replace')
        # Only inspect documentation, not the entire dependency tree.
        names = set(tracked)
        if (root/'docs').exists():
            for path in (root/'docs').rglob('*.md'):
                rel=path.relative_to(root)
                if not any(part in IGNORED_DIRS for part in rel.parts): names.add(rel.as_posix())
        names.update(n for n in REQUIRED if (root/n).exists())
    for name in REQUIRED:
        if name not in names or (not snapshot and not (root/name).is_file()): errors.append(f'{name}: required file missing')
    modes = git(root,'ls-tree','-r','-z','HEAD') if committed else git(root,'ls-files','--stage','-z')
    for entry in modes.split(b'\0'):
        if entry.startswith(b'160000 '):errors.append(entry.split(b'\t',1)[1].decode()+': nested repository is tracked')
    for name in tracked:
        p=PurePosixPath(name)
        if (p.name.startswith('.env') and not p.name.endswith(('.example','.sample','.template'))) or p.suffix in {'.pem','.p12','.pfx','.key'} or (p.name == 'secrets.toml' and '.streamlit' in p.parts):
            errors.append(f'{name}: credential-like file is tracked')
        vendor_dependency = any(part == 'vendor' and (i == 0 or '/'.join(p.parts[:i] + ('composer.json',)) in names) for i, part in enumerate(p.parts))
        if vendor_dependency or any(part in {'node_modules','.venv','venv','__pycache__'} for part in p.parts):errors.append(f'{name}: generated dependency/cache tracked')
    if 'CLAUDE.md' in names and (snapshot or (root/'CLAUDE.md').is_file()):
        guide=read('CLAUDE.md')
        if re.findall(r'^## (.+)$',guide,re.M)!=HEADINGS:errors.append('CLAUDE.md: expected seven standard sections in order')
        if len(guide.splitlines())>120:warnings.append('CLAUDE.md: over 120 lines; consider moving detail into docs')
    if 'CHANGELOG.md' in names and (snapshot or (root/'CHANGELOG.md').is_file()):
        log=read('CHANGELOG.md')
        if len(re.findall(r'^## \[Unreleased\]\s*$',log,re.M))!=1:errors.append('CHANGELOG.md: exactly one Unreleased section required')
        else:
            unreleased=re.split(r'^## \[Unreleased\]\s*$',log,flags=re.M)[1]
            unreleased=re.split(r'^## ',unreleased,flags=re.M)[0]
            if re.findall(r'^### (.+)$',unreleased,re.M)!=['Added','Changed','Fixed']:errors.append('CHANGELOG.md: Unreleased needs Added, Changed, Fixed in order')
        if not re.search(r'^## History \(before \d{4}-\d{2}-\d{2}\)',log,re.M):errors.append('CHANGELOG.md: missing history boundary')
    docs=sorted(n for n in names if n.endswith('.md') and (n.startswith('docs/') or n in REQUIRED))
    for name in docs:
        try: text=read(name)
        except (FileNotFoundError,RuntimeError):
            errors.append(f'{name}: cannot read');continue
        history=name.startswith('docs/superpowers/')
        if name.startswith('docs/') and not history:
            fm=re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)',text,re.S)
            if not fm:errors.append(f'{name}: missing or unclosed frontmatter')
            else:
                for field in ['title','status','last_updated']:
                    if not re.search(r'^'+field+r':\s*\S',fm[1],re.M):errors.append(f'{name}: missing/empty {field}')
        # Historical plans can refer to intentionally retired files.
        if history:continue
        body=re.sub(r'^(`{3,}|~{3,}).*?^\1\s*$', '',text,flags=re.M|re.S)
        for match in re.finditer(r'\]\((<[^>]+>|[^)]+)\)',body):
            target=match[1].strip()
            if target.startswith('<'):target=target[1:target.find('>')]
            else:target=re.sub(r'\s+["\'].*$', '',target)
            target=unquote(target.split('#',1)[0].split('?',1)[0])
            if not target or urlsplit(target).scheme or target.startswith(('~','//')):continue
            parts=[]
            link_path = PurePosixPath(target.lstrip('/')) if target.startswith('/') else PurePosixPath(name).parent/PurePosixPath(target)
            for part in link_path.parts:
                if part=='..':
                    if parts and parts[-1]!='..':parts.pop()
                    else:parts.append(part)
                elif part!='.':parts.append(part)
            resolved='/'.join(parts)
            if resolved.startswith('../'):
                # Sibling repo links are optional on a standalone checkout.
                warnings.append(f'{name}: sibling checkout link {target}');continue
            exists=(resolved in names or any(n.startswith(resolved.rstrip('/')+'/') for n in names)) if snapshot else (root/resolved).exists()
            if not exists:errors.append(f'{name}: missing relative target {target}')
    if staged or base:
        args=['diff','--cached','--name-only','-z'] if staged else ['diff','--name-only','-z',base+'...HEAD']
        changed=set(git(root,*args).decode().split('\0'))-{''}
        code=[n for n in changed if not n.endswith(('.md','.mdx','.txt')) and not n.startswith(('docs/','.repo-standard/','.github/','.githooks/')) and n not in {'.gitignore','.gitattributes'}]
        if code and not any(PurePosixPath(n).name=='CHANGELOG.md' for n in changed):errors.append('Code changed without a CHANGELOG.md change in this commit/range')
    return sorted(set(errors)),sorted(set(warnings))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repo',nargs='?',default='.')
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument('--staged',action='store_true');mode.add_argument('--committed',action='store_true')
    parser.add_argument('--base')
    args=parser.parse_args()
    try:errors,warnings=check(Path(args.repo).resolve(),args.staged,args.base,args.committed)
    except RuntimeError as exc:print(str(exc),file=sys.stderr);return 2
    for item in errors:print('FAIL '+item)
    for item in warnings:print('WARN '+item)
    print(f'docs-standard: {len(errors)} errors, {len(warnings)} warnings')
    return bool(errors)
if __name__=='__main__':sys.exit(main())
