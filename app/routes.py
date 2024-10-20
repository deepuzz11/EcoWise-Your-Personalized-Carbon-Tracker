from flask import render_template, request, redirect, url_for, flash
from app import app, db
from .models import User

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    users = User.query.all()
    return render_template('dashboard.html', users=users)

@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form.get('username')
    new_user = User(username=username)
    db.session.add(new_user)
    db.session.commit()
    flash('User added successfully!')
    return redirect(url_for('dashboard'))
