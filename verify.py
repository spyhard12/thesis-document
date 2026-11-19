#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Verification tool for the thesis rewrite.

Usage:
    python verify.py <relative_path_to_tex_file>

The script compares the current version of a LaTeX source file
with its backup (../thesis_backup_original) and reports any
differences in:
  • citation commands (\cite, \citet, \citep, \parencite, \textcite, \autocite, ...)
  • label / reference commands (\label, \ref, \eqref, \autoref, \cref, ...)
  • math environments (equation, align, $$ ... $$, $ ... $ )
  • figure / table environments (figure, table, subfigure, subtable)
If no differences are found, the script prints "PASS".
"""
import sys
import pathlib
import re
from collections import Counter

CITATION_RE = re.compile(r'\\(?:cite|citet|citep|parencite|textcite|autocite)\b')
LABEL_RE = re.compile(r'\\(?:label|ref|eqref|autoref|cref|Cref|pageref)\b')
MATH_ENV_RE = re.compile(
    r'\\begin\{(?:equation\*?|align\*?|multline\*?|gather\*?)\}|'
    r'\\end\{(?:equation\*?|align\*?|multline\*?|gather\*?)\}|'
    r'\$(?!\$).*?\$|(?<!\\)\$\$(?!\$).*?\$\$',
    re.DOTALL
)
FIGTABLE_RE = re.compile(r'\\begin\{(?:figure\*?|table\*?)\}|\\end\{(?:figure\*?|table\*?)\}')

def token_set(content: str, pattern: re.Pattern) -> Counter:
    return Counter(m.group(0) for m in pattern.finditer(content))

def load_file(path: pathlib.Path) -> str:
    return path.read_text(encoding='utf-8')

def main():
    if len(sys.argv) != 2:
        print('Usage: python verify.py <tex_file>', file=sys.stderr)
        sys.exit(1)

    rel_path = pathlib.Path(sys.argv[1])
    cur_path = pathlib.Path.cwd() / rel_path
    bak_path = pathlib.Path.cwd() / 'thesis_backup_original' / rel_path

    if not cur_path.is_file() or not bak_path.is_file():
        print('ERROR: file not found in current or backup location')
        sys.exit(1)

    cur = load_file(cur_path)
    bak = load_file(bak_path)

    diffs = []
    for name, regex in [
        ('Citations', CITATION_RE),
        ('Labels/Refs', LABEL_RE),
        ('Math Envs', MATH_ENV_RE),
        ('Fig/Table Envs', FIGTABLE_RE)
    ]:
        cur_set = token_set(cur, regex)
        bak_set = token_set(bak, regex)
        if cur_set != bak_set:
            added = cur_set - bak_set
            removed = bak_set - cur_set
            msgs = []
            if added:
                msgs.append(f'  + Added: {list(added.elements())}')
            if removed:
                msgs.append(f'  - Removed: {list(removed.elements())}')
            diffs.append(f'{name} mismatch:\n' + '\n'.join(msgs))

    if diffs:
        print('FAIL – differences detected:')
        for d in diffs:
            print(d)
        sys.exit(1)
    else:
        print('PASS')
        sys.exit(0)

if __name__ == '__main__':
    main()
