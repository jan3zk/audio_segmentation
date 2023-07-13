import os
import requests
from pydub import AudioSegment
from bs4 import BeautifulSoup
import argparse

def get_segments(segment_file):
    with open(segment_file, 'r') as f:
        lines = f.readlines()

    segments = []
    current_segment = []
    sent_id = None
    for line in lines:
        line = line.strip()
        if not line:  # Skip empty or whitespace-only lines
            continue
        if line.startswith('# sent_id = '):
            if current_segment:
                segments.append((sent_id, current_segment))
                current_segment = []
            sent_id = line.replace('# sent_id = ', '')
        else:
            current_segment.append(line)
    if current_segment:
        segments.append((sent_id, current_segment))

    return segments

def find_file(filename, search_path):
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)

def get_mp3_links(link_file):
    with open(link_file, 'r') as f:
        data = f.read()
    soup = BeautifulSoup(data, 'html.parser')
    links = {}
    for s in soup.find_all('s'):
        links[s['id']] = s['speech']
    return links

def download_mp3(url, filename):
    r = requests.get(url, allow_redirects=True)
    with open(filename, 'wb') as f:
        f.write(r.content)

def concatenate_files(sent_id, segment, mp3_links, output_folder):
    audio_segments = []
    for s in segment:
        filename = f"{s}.mp3"
        url = mp3_links[s]
        download_mp3(url, filename)
        audio = AudioSegment.from_mp3(filename)
        audio_segments.append(audio)
        os.remove(filename)
    
    start_segment = segment[0].split('.')[-1]
    end_segment = segment[-1].split('.')[-1]
    #if start_segment == end_segment:
    #    output_filename = f"{output_folder}/{segment[0].split('.')[0]}.{start_segment}.{sent_id}.mp3"
    #else:
    #    output_filename = f"{output_folder}/{segment[0].split('.')[0]}.{start_segment}-{end_segment}.{sent_id}.mp3"
    output_filename = f"{output_folder}/{segment[0].split('.')[0]}.{sent_id}.mp3"

    combined = sum(audio_segments, AudioSegment.empty())
    combined.export(output_filename, format='mp3')

def concatenate_segments(segment_file, output_folder):
    segments = get_segments(segment_file)
    os.makedirs(output_folder, exist_ok=True)
    
    for sent_id, segment in segments:
        link_file = find_file(segment[0][:21]+".vert", "./Gos.vert/")
        mp3_links = get_mp3_links(link_file)
        concatenate_files(sent_id, segment, mp3_links, output_folder)
        print("Concatenating " + ", ".join(segment) + ".")

# Command-line interface
def main():
    parser = argparse.ArgumentParser(description='Concatenate audio segments.')
    parser.add_argument('segment_file', help='File containing segment info')
    parser.add_argument('output_folder', help='Output folder for the concatenated mp3 files')

    args = parser.parse_args()

    concatenate_segments(args.segment_file, args.output_folder)

if __name__ == "__main__":
    main()