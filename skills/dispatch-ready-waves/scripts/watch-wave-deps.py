#!/usr/bin/env python3
import argparse
import pathlib
import re
import sys
import time
from typing import List, Set

HEADER_RE = re.compile(r'^##\s+(.*\S)\s*$')
WAVE_LINK_RE = re.compile(r'\[\[waves/([^\]]+)\]\]')
DEP_RE = re.compile(r'^depends_on:\s*$')
QUOTED_LINK_RE = re.compile(r'^\s*-\s*"\[\[waves/([^\]]+)\]\]"\s*$')
UNQUOTED_LINK_RE = re.compile(r'^\s*-\s*\[\[waves/([^\]]+)\]\]\s*$')


def parse_board_merged(board_path: pathlib.Path) -> Set[str]:
    merged: Set[str] = set()
    current = None
    for raw_line in board_path.read_text().splitlines():
        header = HEADER_RE.match(raw_line)
        if header:
            current = header.group(1)
            continue
        if current != 'Merged':
            continue
        match = WAVE_LINK_RE.search(raw_line)
        if match:
            merged.add(normalize_wave_stem(match.group(1)))
    return merged


def normalize_wave_stem(link_target: str) -> str:
    target = link_target.strip()
    if target.endswith('.md'):
        target = target[:-3]
    return pathlib.Path(target).name


def parse_wave_dependencies(wave_path: pathlib.Path) -> List[str]:
    deps: List[str] = []
    lines = wave_path.read_text().splitlines()
    in_frontmatter = False
    dep_mode = False
    for idx, line in enumerate(lines):
        if idx == 0 and line.strip() == '---':
            in_frontmatter = True
            continue
        if in_frontmatter and line.strip() == '---':
            break
        if not in_frontmatter:
            break
        if DEP_RE.match(line):
            dep_mode = True
            continue
        if dep_mode:
            quoted = QUOTED_LINK_RE.match(line)
            unquoted = UNQUOTED_LINK_RE.match(line)
            if quoted:
                deps.append(normalize_wave_stem(quoted.group(1)))
                continue
            if unquoted:
                deps.append(normalize_wave_stem(unquoted.group(1)))
                continue
            if line.startswith(' ') or line.startswith('\t') or line.strip() == '[]':
                continue
            dep_mode = False
    return deps


def main() -> int:
    parser = argparse.ArgumentParser(description='Wait until a wave\'s dependencies are in the Merged column of an Obsidian board.')
    parser.add_argument('board_path')
    parser.add_argument('wave_path')
    parser.add_argument('--interval', type=float, default=10.0)
    args = parser.parse_args()

    board_path = pathlib.Path(args.board_path).expanduser().resolve()
    wave_path = pathlib.Path(args.wave_path).expanduser().resolve()

    if not board_path.is_file():
        print(f'ERROR: board not found: {board_path}', file=sys.stderr)
        return 2
    if not wave_path.is_file():
        print(f'ERROR: wave file not found: {wave_path}', file=sys.stderr)
        return 2
    if args.interval <= 0:
        print('ERROR: --interval must be > 0', file=sys.stderr)
        return 2

    deps = parse_wave_dependencies(wave_path)
    wave_stem = wave_path.stem

    if not deps:
        print(f'{wave_stem}: no dependencies')
        return 0

    print(f'{wave_stem}: waiting for dependencies to reach Merged: {", ".join(deps)}', flush=True)

    while True:
        merged = parse_board_merged(board_path)
        missing = [dep for dep in deps if dep not in merged]
        if not missing:
            print(f'{wave_stem}: all dependencies merged', flush=True)
            return 0
        print(f'{wave_stem}: still waiting on: {", ".join(missing)}', flush=True)
        time.sleep(args.interval)


if __name__ == '__main__':
    raise SystemExit(main())
