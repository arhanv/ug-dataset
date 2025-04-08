import json
from pathlib import Path

def load_guitar_analysis(filepath):
    """Load the guitar analysis JSON file."""
    with open(filepath, 'r') as file:
        return json.load(file)


def get_id_from_path(filepath):
    path = Path(filepath)
    tuning = path.parts[-3]  # "Open D" 
    genre = path.parts[-2]    # "Rock"
    artist_song_name = path.stem         # "Jeff Buckley - Vancouver"
    return f"{tuning}/{genre}/{artist_song_name}"


def lookup_analysis_for_file(filepath, analysis_data="id_analysis_index.json"):
    """Load the analysis data and lookup an analysis by its filepath."""
    with open(analysis_data, 'r') as file:
        analysis_data = json.load(file)

    # Check if the file exists
    if not Path(filepath).exists():
        print(f"File {filepath} does not exist.")
        return None
    
    identifier = get_id_from_path(filepath)
    
    # Check if the identifier exists in the analysis data
    if identifier not in analysis_data:
        print(f"No analysis found for {identifier}.")
        return None
    return analysis_data[identifier]