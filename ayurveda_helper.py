import json

def load_ayurveda_data(filepath="data/ayurveda_knowledge.json"):
    with open(filepath, 'r') as f:
        return json.load(f)

def get_ayurveda_tip(issue, data):
    return data.get(issue.lower(), "Sorry, no ayurvedic tip found for this issue.")
