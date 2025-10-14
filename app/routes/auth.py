from flask import Blueprint

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Authentication routes will be added in Week 5