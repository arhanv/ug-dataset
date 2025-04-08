import os
import json
from pathlib import Path

XML_DATASET_FOLDER = "../dataset-converted-xml"
JSON_FILE = "../notebooks/analysis_results2.json"

def match_tuning_to_musicxml(json_analysis_file, musicxml_folder, output_json_file="xml_analysis_index.json"):
     """
     Iterate through the analysis file and match the tuning to the MusicXML files.
     """
     with open(json_analysis_file, "r") as f:
          data = json.load(f)

     matched_tracks = {}
     for track in data:
          path = Path(track["filepath"])

          # Extract parts
          tuning = path.parts[-3]  # "Open D"
          genre = path.parts[-2]    # "Rock"
          artist_song_name = path.stem         # "Jeff Buckley - Vancouver"

          # Construct the path to the MusicXML file
          musicxml_path = os.path.join(musicxml_folder, tuning, genre, artist_song_name + ".musicxml")

          identifier = f"{tuning}/{genre}/{artist_song_name}"

          if os.path.exists(musicxml_path):
               matched_tracks[identifier] = track
          else:
               print(f"No matching MusicXML file found for {tuning}/{genre}/{artist_song_name}")

     # Save the matched tracks to a JSON file
     with open(output_json_file, "w") as output_file:
          json.dump(matched_tracks, output_file, indent=4)

     print(f"Matched tracks saved to {output_json_file}")

match_tuning_to_musicxml(JSON_FILE, XML_DATASET_FOLDER)

                    
                    


