# app/utils/zip_coordinates.py
# This file provides approximate coordinates for ZIP codes in your regions
# In a real production app, you'd use a geocoding API, but for your project
# this hardcoded approach works fine and is faster

ZIP_COORDINATES = {
    # Atlantic Iowa Region
    '50022': (41.5914, -94.7633),   # Anita, IA
    '50025': (41.4036, -95.0139),   # Atlantic, IA
    '51520': (41.2619, -95.8608),   # Council Bluffs, IA
    '51601': (40.7658, -95.3769),   # Shenandoah, IA
    '50002': (41.0261, -93.6160),   # Adair, IA
    '50020': (41.6011, -94.3427),   # Adel, IA
    '50042': (41.4583, -94.6841),   # Bagley, IA
    '50048': (41.3269, -94.9894),   # Brayton, IA
    
    # More Iowa cities
    '51010': (42.4974, -96.4003),   # Akron, IA
    '51040': (42.7586, -96.2606),   # Hawarden, IA
    '51060': (42.4969, -95.8761),   # Orange City, IA
    
    # St. Joseph Missouri Region
    '64501': (39.7684, -94.8467),   # Saint Joseph, MO
    '64503': (39.7447, -94.8163),   # Saint Joseph, MO (North)
    '64504': (39.7905, -94.7961),   # Saint Joseph, MO (East)
    '64505': (39.7275, -94.8769),   # Saint Joseph, MO (South)
    
    # Leavenworth Kansas Region
    '66027': (39.3111, -94.9225),   # Leavenworth, KS
    '66048': (39.3697, -94.9858),   # Leavenworth, KS (North)
    '66002': (39.5631, -95.1218),   # Atchison, KS
    '66012': (39.0214, -94.8669),   # Bonner Springs, KS
    
    # Kansas City Metro (for context)
    '64101': (39.0997, -94.5786),   # Kansas City, MO (Downtown)
    '64102': (39.1008, -94.5822),   # Kansas City, MO (Crown Center)
    '64105': (39.0931, -94.5828),   # Kansas City, MO (Crossroads)
    '64106': (39.1139, -94.5744),   # Kansas City, MO (River Market)
    '64108': (39.0486, -94.5847),   # Kansas City, MO (Midtown)
    '64109': (39.0361, -94.5853),   # Kansas City, MO (Plaza)
    '64110': (39.0158, -94.5689),   # Kansas City, MO (South)
    '64111': (39.0508, -94.5953),   # Kansas City, MO (Westport)
    '64112': (39.0399, -94.5919),   # Kansas City, MO (Country Club Plaza)
    '64113': (39.0031, -94.5936),   # Kansas City, MO (Waldo)
    '64114': (38.9647, -94.5761),   # Kansas City, MO (South KC)
    '64030': (38.8861, -94.5333),   # Grandview, MO
    
    # Kansas Side
    '66207': (38.9822, -94.6708),   # Overland Park, KS
    '66204': (39.0267, -94.6689),   # Overland Park, KS (North)
    '66062': (39.1136, -94.7269),   # Shawnee, KS
    '66103': (39.1142, -94.6744),   # Kansas City, KS
}

def get_coordinates(zip_code):
    """
    Get coordinates for a ZIP code
    
    Args:
        zip_code (str): 5-digit ZIP code
        
    Returns:
        tuple: (latitude, longitude) or None if not found
    """
    return ZIP_COORDINATES.get(zip_code)

def get_coordinates_with_default(zip_code, default_lat=39.0997, default_lng=-94.5786):
    """
    Get coordinates with a default fallback (Kansas City downtown)
    
    Args:
        zip_code (str): 5-digit ZIP code
        default_lat (float): Default latitude if ZIP not found
        default_lng (float): Default longitude if ZIP not found
        
    Returns:
        tuple: (latitude, longitude)
    """
    coords = ZIP_COORDINATES.get(zip_code)
    if coords:
        return coords
    return (default_lat, default_lng)

def add_coordinates_to_location(location_obj):
    """
    Add coordinates to a Location object if they don't exist
    
    Args:
        location_obj: Location model instance
        
    Returns:
        bool: True if coordinates were added, False if they already existed
    """
    if location_obj.latitude and location_obj.longitude:
        return False  # Already has coordinates
    
    coords = get_coordinates(location_obj.zip_code)
    if coords:
        location_obj.latitude, location_obj.longitude = coords
        return True
    
    return False

# For your specific regions, here are the center points for the map
REGION_CENTERS = {
    'atlantic_iowa': (41.4036, -95.0139),     # Atlantic, IA
    'st_joseph_mo': (39.7684, -94.8467),      # St. Joseph, MO
    'leavenworth_ks': (39.3111, -94.9225),    # Leavenworth, KS
    'kansas_city': (39.0997, -94.5786),       # Kansas City Metro
}

def get_region_center(region_name):
    """Get the center coordinates for a region"""
    return REGION_CENTERS.get(region_name, REGION_CENTERS['kansas_city'])