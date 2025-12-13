from app.extensions import db
from datetime import datetime

class SavedAddress(db.Model):
    __tablename__ = 'saved_addresses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100))  # Custom name like "Johnson House"
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    zip_code = db.Column(db.String(10))
    address_type = db.Column(db.String(50))  # residential, commercial
    filters_used = db.Column(db.JSON)  # What filters found this
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('saved_addresses', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'address_type': self.address_type,
            'filters_used': self.filters_used,
            'notes': self.notes,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }