from app.extensions import db
from datetime import datetime

class SearchHistory(db.Model):
    __tablename__ = 'search_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    zip_code = db.Column(db.String(10))
    filters = db.Column(db.JSON)  # Store filter criteria as JSON
    search_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('searches', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'zip_code': self.zip_code,
            'filters': self.filters,
            'search_date': self.search_date.strftime('%Y-%m-%d %H:%M')
        }