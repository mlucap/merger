import os
import subprocess

channel_file = 'channel.txt'
cookies_file = 'cookies.txt'
shorts_dir = 'shorts'

# Check if channel.txt exists
if not os.path.exists(channel_file):
    print('channel.txt not found!')
    input('Press Enter to exit...')
    exit()

# Read channel URL
with open(channel_file, 'r', encoding='utf-8') as f:
    channel_url = f.read().strip()

if os.path.exists("cookies.txt"):
    pass
else:
    raise FileNotFoundError("cookies.txt not found")

print(f"Using channel: {channel_url}")

# Create shorts folder if it doesn't exist
os.makedirs(shorts_dir, exist_ok=True)

# Run yt-dlp with filters
command = [
    'yt-dlp',
    '--cookies', "cookies.txt",
    channel_url,
    '-o', os.path.join(shorts_dir, '%(title)s.%(ext)s'),
    '-f', 'bestvideo+bestaudio/best',
    '--merge-output-format', 'mp4',
    '--sleep-interval', '2',
    '--max-sleep-interval', '10',
    '--throttled-rate', '500K',
    '--retries', '10',
    '--retry-sleep', '20'
]

subprocess.run(command)

input("Press Enter to exit...")
