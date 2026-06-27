#!/usr/bin/env python3

from pathlib import Path
from shutil import move

def create_bands_set(path: Path) -> set:
    bands = set()
    for band_directory in path.glob("*/"):
        bands.add(band_directory)
    return bands
    
def sort_song(song: Path, bands: set) -> bool:
    was_sorted = False
    song_normalised = song.name.replace("_", "-").lower()
    for band in bands:
        if band.name.lower() in song_normalised: 
            move(str(song), str(band) + "/" + str(song.name))
            was_sorted = True
    return was_sorted

def main() -> None:
    user_input = input("[input] path to the music folder (empty takes parent): ")
    if not user_input:
        music_dir = Path(__file__).resolve().parent
    else:
        try:
            music_dir = Path(user_input).resolve()
        except:
            print("[error] that path doesn't exist or you dont have permissions for it :(")
            raise SystemExit("[error] execute me again with a valid path pls")
    bands = create_bands_set(music_dir)
    print(f"[searching] found {len(bands)} band folders!")
    print("[sorting] now getting to sorting...")
    counter = 0
    for song in music_dir.glob("*.opus"):
        counter += sort_song(song, bands)
    print(f"[finished] sorted {counter} songs, done")

if __name__ == "__main__":
    main()