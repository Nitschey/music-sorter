#!/usr/bin/env python3

from pathlib import Path
from shutil import move

# list of fluff that can appear in YT music videos -> just removed
# not exhaustive, some arcane title constructions will still need manual editing
FLUFF_LIST = ["hd", "official", "music", "content", "video", "visual", "visualizer", "visualiser", 
            "4k", "upgrade", "lyric", "lyrics" "(", ")", "[", "]" "@"]
# structural & grammar constructions that get created by yt-dlp normalising file names -> changed/cleaned
STRUCTURES_LIST = [("_-_", "-"), ("_s_", "s_"), ("_re_", "re_"), ("_d_", "d_"), ("_&_", "_and_")]
# formats to handle
AUDIO_FORMATS = ("opus", "m4a", "mp3", "flac", "ogg", "wav", "webm")

def create_bands_set(music_dir: Path) -> set:
    bands = set()
    # filter out hidden folders (for windows)
    band_directories = (dir for dir in music_dir.glob("*/")
                        if not dir.name.startswith("."))
    # add all folders in music directory to set
    for band_directory in band_directories:
        bands.add(band_directory)
    return bands

def clean_song_title(song: Path) -> str:
    # cant apply lower directly to name attribute
    song_name = song.stem.lower()
    # create list of pairs of replacements (replace fluff with nothing)
    replace_pairs = [(fluff, "") for fluff in FLUFF_LIST]
    replace_pairs.extend(STRUCTURES_LIST)
    for pair in replace_pairs:
        song_name = song_name.replace(*pair)
    # remove leftover underscores from cleaning fluff
    song_name = song_name.strip("_").title()
    return song_name + song.suffix

def sort_song(song: Path, bands: set) -> bool:
    was_sorted = False
    cleaned_name = clean_song_title(song)
    for band in bands:
        # need to replace underscores to match with band folder names
        if band.name.lower() in cleaned_name.lower().replace("_", "-"): 
            # move to band folder with cleaned song title for file name
            try:
                move(str(song), str(band) + "/" + cleaned_name)
                print(f"[sorting] sorted {song.name} into {band.name}")
                was_sorted = True
                return was_sorted
            except:
                print(f"[warning] couldn't sort {song.name}")
                return was_sorted
    return was_sorted

def main() -> None:
    user_input = input("[input] path to the music folder (empty takes parent): ")
    if not user_input:
        music_dir = Path(__file__).resolve().parent
    else:
        try:
            music_dir = Path(user_input).resolve()
        except:
            print("[error] that path doesn't exist or you don't have permissions for it :(")
            raise SystemExit("[error] execute me again with a valid path pls")
    bands = create_bands_set(music_dir)
    print(bands)
    print(f"[searching] found {len(bands)} band folders!")
    print("[sorting] now getting to sorting...")
    sorted_counter = 0
    failed_counter = 0
    music_files = list()
    for format in AUDIO_FORMATS:
        music_files.extend(music_dir.glob("*." + format))
    for song in music_files:
        if sort_song(song, bands) == True:
            sorted_counter += 1
        else:
            failed_counter += 1
    if failed_counter > 0:
        print(f"[warning] failed sorting {failed_counter} songs, check manually")
    print(f"[finished] sorted {sorted_counter} songs, done")

if __name__ == "__main__":
    main()