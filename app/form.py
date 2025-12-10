# app/forms.py
# This file creates forms for adding locations and demographics
# Forms make it easier to validate user input before saving to database

from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Optional, NumberRange

class LocationForm(FlaskForm):
    """Form for adding a new business location"""
    # Each field is like an input box on a web form
    # DataRequired() means the field must be filled out
    
    name = StringField('Business Name', validators=[DataRequired()])
    address = StringField('Street Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zip_code = StringField('ZIP Code', validators=[DataRequired()])
    
    # Optional means these fields can be left blank
    latitude = FloatField('Latitude (optional)', validators=[Optional()])
    longitude = FloatField('Longitude (optional)', validators=[Optional()])
    
    # SelectField creates a dropdown menu
    business_type = SelectField('Business Type', 
                                choices=[
                                    ('', 'Select Type...'),
                                    ('residential', 'Residential Home'),
                                    ('office', 'Office Building'),
                                    ('retail', 'Retail Store'),
                                    ('restaurant', 'Restaurant'),
                                    ('medical', 'Medical Facility'),
                                    ('hotel', 'Hotel/Hospitality'),
                                    ('education', 'School/University'),
                                    ('warehouse', 'Warehouse/Industrial'),
                                    ('government', 'Government Building'),
                                    ('religious', 'Church/Religious'),
                                    ('other', 'Other')
                                ],
                                validators=[DataRequired()])
    
    # TextAreaField is for longer text (like a paragraph)
    notes = TextAreaField('Notes', validators=[Optional()])


class DemographicForm(FlaskForm):
    """Form for adding demographic data for a ZIP code"""
    
    zip_code = StringField('ZIP Code', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    
    # NumberRange ensures the number is reasonable (between 0 and 10 million)
    population = FloatField('Population', 
                           validators=[Optional(), 
                                     NumberRange(min=0, max=10000000)])
    
    median_income = FloatField('Median Income', 
                              validators=[Optional(), 
                                        NumberRange(min=0, max=1000000)])
    
    median_age = FloatField('Median Age', 
                           validators=[Optional(), 
                                     NumberRange(min=0, max=120)])
    
    median_home_value = FloatField('Median Home Value', 
                                  validators=[Optional(), 
                                            NumberRange(min=0, max=10000000)])
    
    households = FloatField('Number of Households', 
                           validators=[Optional(), 
                                     NumberRange(min=0, max=1000000)])