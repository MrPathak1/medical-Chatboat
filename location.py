import geocoder

def get_user_location():
    g = geocoder.ip('me')
    if g.ok:
        return g.latlng  # returns [latitude, longitude]
    return None
