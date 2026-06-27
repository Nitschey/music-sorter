#!/usr/bin/env python3

from pathlib import Path
from shutil import move

# list of fluff that can appear in YT videos
FLUFF_LIST = ["hd", "official", "video", "visual", "(", ")", "[", "]" "@"]

def create_bands_set(path: Path) -> set:
    bands = set()
    for band_directory in path.glob("*/"):
        bands.add(band_directory)
    return bands
    
def sort_song(song: Path, bands: set) -> bool:
    was_sorted = False
    song = song.parent / clean_song_title(song.name)
    for band in bands:
        if band.name.lower() in song.name.lower(): 
            move(str(song), str(band) + "/" + str(song.name))
            was_sorted = True
    return was_sorted

def clean_song_title(song: str) -> str:
    # remove spaces around dash separator
    removed_spaces = song.replace("_-_", "-")
    # create list of pairs of replacements
    replace_pairs = [(fluff, "") for fluff in FLUFF_LIST]
    # remove extra underscores around dash separator
    replace_pairs.append(("_-_", "-"))
    for pair in replace_pairs:
        removed_spaces = removed_spaces.lower().replace(*pair)
    # everything back as a title with underscores
    removed_fluff = "_".join(removed_spaces.split()).title()
    cleaned_title = removed_fluff.strip("_")
    return cleaned_title

def main() -> None:
    user_input = input("[input] path to the music folder (empty takes parent): ")
    if not user_input:
        music_dir = Path(__file__).resolve().parent
    else:
        try:
            music_dir = Path(user_input).resolve()
        except:
            print("[error] that path doesn't exist or you do nt have permissions for it :(")
            raise SystemExit("[error] execute me again with a valid path pls")
    bands = create_bands_set(music_dir)
    print(f"[searching] found {len(bands)} band folders!")
    print("[sorting] now getting to sorting...")
    counter = 0
    for song in music_dir.glob("*.opus"):
        counter += sort_song(song, bands)
    print(f"[finished] sorted {counter} songs, done")

if __name__ == "__main__":
    # main()
    print(clean_song_title("Kid_Kapichi_ft._Bob_Vylan_-_New_England_(Official_Video)"))