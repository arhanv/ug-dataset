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

        # Loop through the traks in demo
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
                        
                        # Record chords
                        # if beat.chord:
                        #     track_info["chords"].append(beat.chord.name)
            
            # Convert Counter to a regular dictionary for JSON serialization
            track_info["string_fret_frequency"] = {
                string: dict(frets) for string, frets in string_fret_frequency.items()
            }

            analysis["tracks"].append(track_info)
        
        return analysis
    except Exception as e:
        print(f"Error processing file {filepath}: {e}")
        return None

def process_folder(folder_path, output_json):
    """Process all Guitar Pro files in a folder and save the analysis to a JSON file."""
    results = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(('.gp3', '.gp4', '.gp5', '.gpx', '.gp')):
                filepath = os.path.join(root, file)
                print(f"Processing file: {filepath}")
                analysis = analyze_guitarpro_file(filepath)
                if analysis:
                    results.append(analysis)
    
    # Save results to JSON
    with open(output_json, 'w') as json_file:
        json.dump(results, json_file, indent=4)
    print(f"Analysis saved to {output_json}")

# folder_path = "Open D/Rock" 
# output_json = "guitar_analysis.json"
# process_folder(folder_path, output_json)