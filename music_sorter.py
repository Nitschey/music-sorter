#!/usr/bin/env python3

from pathlib import Path
from shutil import move

# list of fluff that can appear in YT music videos
FLUFF_LIST = ["hd", "official", "music", "content", "video", "visual", "visualizer", "visualiser", "4k", "lyric", "lyrics" "(", ")", "[", "]" "@"]

def create_bands_set(music_dir: Path) -> set:
    bands = set()
    # add all folders in music directory to set
    for band_directory in music_dir.glob("*/"):
        bands.add(band_directory)
    return bands

def sort_song(song: Path, bands: set) -> bool:
    was_sorted = False
    for band in bands:
        # need to replace underscores to match with band folder names
        if band.name.lower() in song.name.lower().replace("_", "-"): 
            # move to band folder with cleaned song title for file name
            try:
                move(str(song), str(band) + "/" + clean_song_title(song.name))
                was_sorted = True
                print(f"[sorting] sorted {song.name} into {band.name}")
            except:
                print(f"[warning] couldn't sort {song.name}")
    return was_sorted

def clean_song_title(song: str) -> str:
    # remove spaces around dash separator
    removed_spaces = song.replace("_-_", "-")
    # create list of pairs of replacements (replace fluff with nothing)
    replace_pairs = [(fluff, "") for fluff in FLUFF_LIST]
    # remove extra underscores around dash separator
    replace_pairs.append(("_-_", "-"))
    for pair in replace_pairs:
        removed_spaces = removed_spaces.lower().replace(*pair)
    # everything back as a title with underscores
    removed_fluff = "_".join(removed_spaces.split())
    # remove trailing underscores left over from fluff removal
    stripped_underscores = removed_fluff.split(".")
    stripped_underscores[0] = stripped_underscores[0].strip("_").title()
    cleaned_title = ".".join(stripped_underscores)
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
    sorted_counter = 0
    failed_counter = 0
    for song in music_dir.glob("*.opus"):
        if sort_song(song, bands) == True:
            sorted_counter += 1
        else:
            failed_counter += 1
    if failed_counter > 0:
        print(f"[warning] failed sorting {failed_counter} songs, check manually")
    print(f"[finished] sorted {sorted_counter} songs, done")

if __name__ == "__main__":
    main()