#!/usr/bin/env python3

import shutil
from pathlib import Path

def create_dir_set(path: Path) -> set:
    dirs = set()
    for directory in path.glob("*/"):
        dirs.add(directory)
    return dirs

def sort_into_dir(song: str) -> None:
    pass

def compare_with_dirs(file: str, dirs: set) -> bool:
    was_sorted = False
    song = file.replace("_", "-")
    for band in dirs:
        if band in song:
            sort_into_dir(song)
            was_sorted = True
    
    return was_sorted

def main():
    for item in create_dir_set(Path("C:/Users/niklas.nitsch/Documents/Teaching").resolve()):
        print(item)

if __name__ == "main":
    main()