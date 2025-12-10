from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Optional

class LocationForm(FlaskForm):
    name = StringField('Business Name', validators=[DataRequired()])
    address = StringField('Street Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zip_code = StringField('ZIP Code', validators=[DataRequired()])
    latitude = FloatField('Latitude', validators=[Optional()])
    longitude = FloatField('Longitude', validators=[Optional()])
    business_type = SelectField('Business Type', 
                                choices=[
                                    ('', 'Select Type...'),
                                    ('coffee', 'Coffee Shop'),
                                    ('restaurant', 'Restaurant'),
                                    ('retail', 'Retail'),
                                    ('fitness', 'Fitness'),
                                    ('service', 'Service'),
                                    ('other', 'Other')
                                ])
    notes = TextAreaField('Notes', validators=[Optional()])