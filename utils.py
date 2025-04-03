import json

def load_guitar_analysis(filepath):
    """Load the guitar analysis JSON file."""
    with open(filepath, 'r') as file:
        return json.load(file)
