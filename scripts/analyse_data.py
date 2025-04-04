import os
import json
import collections
import guitarpro

def analyze_guitarpro_file(filepath):
    """Analyze a Guitar Pro file and return the analysis as a dictionary."""
    try:
        demo = guitarpro.parse(filepath)
        analysis = {
            "title": demo.title,
            "artist": demo.artist,
            "album": demo.album,
            "tracks": []
        }

        # Loop through the tracks in the demo
        for track in demo.tracks:
            track_info = {
                "name": track.name,
                "instrument": track.channel.instrument,
                "tuning": [string.value for string in track.strings],
                "string_fret_frequency": {},
                "chords": []
            }

            # Analyze string and fret usage
            string_fret_frequency = {string.number: collections.Counter() for string in track.strings}
            for measure in track.measures:
                for voice in measure.voices:
                    for beat in voice.beats:
                        # Record string and fret usage
                        for note in beat.notes:
                            string_fret_frequency[note.string][note.value] += 1

            # Convert Counter to a regular dictionary for JSON serialization
            track_info["string_fret_frequency"] = {
                string: dict(frets) for string, frets in string_fret_frequency.items()
            }

            analysis["tracks"].append(track_info)

        return analysis
    except Exception as e:
        print(f"Error processing file {filepath}: {e}")
        return None

def process_dataset_folder(dataset_folder, output_json):
    """Process the entire dataset folder and save the analysis to a JSON file."""
    results = []
    file_count = 0  # Counter for the number of files analyzed
    fail_file_count = 0
    failed_filepaths = []
    for tuning_folder in os.listdir(dataset_folder):
        tuning_path = os.path.join(dataset_folder, tuning_folder)
        if os.path.isdir(tuning_path):
            for genre_folder in os.listdir(tuning_path):
                genre_path = os.path.join(tuning_path, genre_folder)
                if os.path.isdir(genre_path):
                    for root, _, files in os.walk(genre_path):
                        for file in files:
                            if file.endswith(('.gp3', '.gp4', '.gp5', '.gpx', '.gp')):
                                filepath = os.path.join(root, file)
                                print(f"Processing file: {filepath}")
                                analysis = analyze_guitarpro_file(filepath)
                                if analysis:
                                    # Add tuning and genre information to the analysis
                                    for track in analysis["tracks"]:
                                        track["tuning_folder"] = tuning_folder
                                        track["genre"] = genre_folder
                                    results.append(analysis)
                                    file_count += 1  # Increment the file counter
                                else:
                                    fail_file_count += 1
                                    failed_filepaths.append(filepath)

    # Save results to JSON
    with open(output_json, 'w') as json_file:
        json.dump(results, json_file, indent=4)

    with open('failed_files.txt', 'w') as fail_file:
        for failed_filepath in failed_filepaths:
            fail_file.write(f"{failed_filepath}\n")

    print(f"Analysis saved to {output_json}")
    print(f"Total files analyzed: {file_count}")
    print(f"Total files failed: {fail_file_count}")
    print(f"Total files processed: {file_count + fail_file_count}")