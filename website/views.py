from flask import Blueprint, render_template

views = Blueprint('views' , __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@views.route('/example', methods=['GET', 'POST'])
def example():
    return render_template('example.html')