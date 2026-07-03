import requests

def find_nearby_places(lat, lon, place_type="medical"):
    api_key = 'YOUR_GOOGLE_MAPS_API_KEY'  # Replace with your real API key
    endpoint = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    params = {
        "location": f"{lat},{lon}",
        "radius": 20000,
        "type": "pharmacy",
        "keyword": place_type,
        "key": api_key
    }

    response = requests.get(endpoint, params=params)
    results = response.json().get("results", [])
    places = []

    for place in results[:5]:
        places.append({
            "name": place["name"],
            "address": place.get("vicinity", "No address")
        })

    return places
