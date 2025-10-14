from flask import Blueprint, render_template, jsonify

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return render_template('index.html')

@bp.route('/hello')
def hello():
    return jsonify({
        'message': 'Flask app is working!',
        'status': 'success'
    })