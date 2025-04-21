#!/usr/bin/env python3
import os
import re
import shutil

# 1) Pattern to identify and strip off unwanted suffixes:
#    • -- checksum or "-- ..." trailing metadata
#    • [BD Fr], [Scan-1830], etc.
#    • from Les Arenes / from Anna’s Archive
#    • any trailing whitespace
cleanup_re = re.compile(
    r'''
    ^(?P<core>.+?)           # capture the main title as 'core'
    (?:\s*--[^.\n]+)?        # optional ' -- ...' chunk
    (?:\s*\[.*?\])?          # optional '[...]' chunk
    (?:\s*from\s+[^.\n]+)?   # optional 'from ...' chunk
    \s*                       # trailing whitespace
    \.(?P<ext>cbr|cbz|pdf|epub|rar|azw3)$
    ''',
    re.IGNORECASE | re.VERBOSE
)

# 2) Pattern to split series vs. volume/issue:
#    matches things like "Series Name T02", "Series Name v1", "Series Name Vol. 3"
series_vol_re = re.compile(
    r'''
    ^(?P<series>.+?)         # the series name
    [\s._-]*                 # spacing or separators
    (?:(?:T|v|Vol(?:ume)?)[\s._-]*  # T / v / Vol or Volume
      (?P<number>\d+))       # issue/volume number
    $
    ''',
    re.IGNORECASE | re.VERBOSE
)

# Supported extensions
valid_exts = {'.cbr', '.cbz', '.pdf', '.epub', '.rar', '.azw3'}

def normalize_and_move(filename):
    name, ext = os.path.splitext(filename)
    if ext.lower() not in valid_exts:
        return  # skip non‐comic files

    m = cleanup_re.match(filename)
    if not m:
        print(f"Skipping (no match): {filename}")
        return

    core = m.group('core').strip()
    ext = '.' + m.group('ext').lower()

    # Try to split out volume/issue
    mv = series_vol_re.match(core)
    if mv:
        series = mv.group('series').strip()
        num = mv.group('number').lstrip('0')  # drop leading zeros
        new_filename = f"{series} – Vol {num}{ext}"
    else:
        series = core
        new_filename = f"{series}{ext}"

    # Create directory for the series
    os.makedirs(series, exist_ok=True)

    # Move & rename
    src = filename
    dst = os.path.join(series, new_filename)
    if os.path.exists(dst):
        print(f"  ↳ Destination exists, skipping: {dst}")
    else:
        print(f"  ↳ Moving '{src}' → '{dst}'")
        shutil.move(src, dst)

def main():
    for f in os.listdir('.'):
        if os.path.isfile(f):
            normalize_and_move(f)

if __name__ == '__main__':
    main()
