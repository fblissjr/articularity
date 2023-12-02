
import json
import argparse
import os

def format_timestamps(timestamps):
    """Converts a list of two timestamps (start and end) from seconds to a 'HH:MM:SS' format."""
    formatted_timestamps = []
    for timestamp in timestamps:
        if timestamp is not None:  # Check if timestamp is not None
            hours, remainder = divmod(int(timestamp), 3600)
            minutes, seconds = divmod(remainder, 60)
            formatted_timestamps.append(f"{hours:02}:{minutes:02}:{seconds:02}")
        else:
            formatted_timestamps.append("00:00:00")  # Default value for None timestamps
    return f"[{formatted_timestamps[0]} - {formatted_timestamps[1]}]"

def convert_json_to_readable_format(json_data, include_timestamps=True, include_speakers=True, speaker_ids=None):
    """Converts the JSON data to a readable text format, with options for timestamps and speakers."""
    readable_text = []
    for chunk in json_data:
        if isinstance(chunk, dict) and 'text' in chunk:
            text_line = ""
            if include_timestamps and 'timestamp' in chunk:
                timestamp = format_timestamps(chunk['timestamp'])
                text_line += f"{timestamp} "
            if include_speakers and 'speaker' in chunk:
                speaker = chunk['speaker']
                if speaker_ids:
                    speaker = speaker_ids.get(speaker, speaker)  # Replace with provided speaker ID if available
                text_line += f"{speaker}: "
            text_line += chunk['text']
            readable_text.append(text_line)
    return '\n'.join(readable_text)

def main():
    parser = argparse.ArgumentParser(description='Convert JSON transcription to readable text format.')
    parser.add_argument('input_json', help='Input JSON file path')
    parser.add_argument('output_txt', help='Output text file path')
    parser.add_argument('--no_timestamp', action='store_false', dest='timestamp', help='Exclude timestamps from the output')
    parser.add_argument('--no_speaker', action='store_false', dest='speaker', help='Exclude speaker information from the output')
    parser.add_argument('--speaker_id', nargs='*', help='List of custom speaker IDs (e.g., --speaker_id John Jane)')
    args = parser.parse_args()

    # Convert speaker_id list to a dictionary if provided
    speaker_ids = {f"SPEAKER_{i:02}": name for i, name in enumerate(args.speaker_id, 1)} if args.speaker_id else None

    # Read input JSON file
    with open(args.input_json, 'r') as json_file:
        json_data = json.load(json_file)

    # Convert JSON to readable format
    readable_text = convert_json_to_readable_format(json_data, include_timestamps=args.timestamp, include_speakers=args.speaker, speaker_ids=speaker_ids)

    # Write output to file
    with open(args.output_txt, 'w') as txt_file:
        txt_file.write(readable_text)

if __name__ == "__main__":
    main()
