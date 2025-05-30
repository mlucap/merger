import os
import subprocess

SHORTS_DIR = "shorts"
OUTPUT_FILE = "output.mp4"

def get_mp4_files(directory):
    return sorted([f for f in os.listdir(directory) if f.lower().endswith(".mp4")])

def reencode_to_ts(input_dir):
    ts_files = []
    mp4_files = get_mp4_files(input_dir)
    
    for i, mp4 in enumerate(mp4_files):
        input_path = os.path.join(input_dir, mp4)
        ts_filename = f"reencoded_{i}.ts"
        ts_path = os.path.join(input_dir, ts_filename)
        ts_files.append(ts_path)

        ffmpeg_cmd = [
            "ffmpeg",
            "-i", input_path,
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "23",
            "-c:a", "aac",
            "-b:a", "192k",
            "-ar", "44100",
            "-ac", "2",
            "-f", "mpegts",
            ts_path
        ]

        print(f"Re-encoding {mp4} → {ts_filename}")
        subprocess.run(ffmpeg_cmd, check=True)

    return ts_files

def concatenate_ts_files(ts_files, output_path):
    concat_str = "|".join(ts_files)
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", f"concat:{concat_str}",
        "-c", "copy",
        output_path
    ]
    print(f"Concatenating {len(ts_files)} TS files into {output_path}...")
    subprocess.run(ffmpeg_cmd, check=True)

def delete_ts_files(directory="./shorts"):
    ts_files = [f for f in os.listdir(directory) if f.lower().endswith(".ts")]
    if not ts_files:
        print("No .ts files found.")
        return

    for ts_file in ts_files:
        try:
            os.remove(os.path.join(directory, ts_file))
            print(f"Deleted: {ts_file}")
        except Exception as e:
            print(f"Error deleting {ts_file}: {e}")

if __name__ == "__main__":
    if not os.path.isdir(SHORTS_DIR):
        print(f"Error: '{SHORTS_DIR}' folder not found.")
        exit(1)

    ts_files = reencode_to_ts(SHORTS_DIR)
    concatenate_ts_files(ts_files, OUTPUT_FILE)
    delete_ts_files()
    print(f"Done! Created '{OUTPUT_FILE}' in current directory.")


