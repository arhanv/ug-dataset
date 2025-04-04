import json
from constants import TUNING_LABELS

def load_guitar_analysis(filepath):
    """Load the guitar analysis JSON file."""
    with open(filepath, 'r') as file:
        return json.load(file)

def filter_guitars_by_tuning_label(data, tuning_label):
    """Filter guitars using a specific tuning label."""
    # Look up the tuning values directly from the label
    tuning = TUNING_LABELS.get(tuning_label)
    
    if tuning is None:
        raise ValueError(f"Tuning label '{tuning_label}' not found in TUNING_LABELS.")
    
    # Filter the guitars using the tuning values
    filtered_data = []
    for song in data:
        for track in song.get("tracks", []):
            if tuple(track.get("tuning", [])) == tuning and "Guitar" in track.get("name", ""):
                filtered_data.append({
                    "title": song.get("title", "Unknown"),
                    "artist": song.get("artist", "Unknown"),
                    "track_name": track.get("name", "Unknown"),
                    "tuning": track.get("tuning"),
                    "tuning_label": tuning_label,
                    "string_fret_frequency": track.get("string_fret_frequency")
                })
    return filtered_data

def load_analysis_file_by_tuning(filepath, tuning_label):
    """Load the guitar analysis JSON file and filter by tuning label."""
    data = load_guitar_analysis(filepath)
    filtered_data = filter_guitars_by_tuning_label(data, tuning_label)
    return filtered_data