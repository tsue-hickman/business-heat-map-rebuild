# Import all models here so they can be imported from app.models
from app.models.user import User
from app.models.demographic import Demographic
from app.models.location import Location
from app.models.search_history import SearchHistory
from app.models.saved_address import SavedAddress

__all__ = ['User', 'Demographic', 'Location', 'SearchHistory', 'SavedAddress']
