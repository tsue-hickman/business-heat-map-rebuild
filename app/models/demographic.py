from app import db
from datetime import datetime

class Demographic(db.Model):
    __tablename__ = 'demographics'
    
    id = db.Column(db.Integer, primary_key=True)
    zip_code = db.Column(db.String(10), unique=True, nullable=False)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    population = db.Column(db.Integer, nullable=True)
    median_income = db.Column(db.Integer, nullable=True)
    median_age = db.Column(db.Float, nullable=True)
    median_home_value = db.Column(db.Integer, nullable=True)
    households = db.Column(db.Integer, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Demographic {self.zip_code} - {self.city}, {self.state}>'
    
    def get_income_range(self):
        """Return income bracket category"""
        if not self.median_income:
            return 'Unknown'
        if self.median_income < 40000:
            return 'Low Income'
        elif self.median_income < 75000:
            return 'Middle Income'
        elif self.median_income < 120000:
            return 'Upper Middle Income'
        else:
            return 'High Income'