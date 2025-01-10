from flask import render_template, request, redirect, url_for, flash
from app import app, db
from .models import User

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    try:
        users = User.query.all()
        return render_template('dashboard.html', users=users)
    except Exception as e:
        flash('Error fetching users: {}'.format(str(e)))
        return redirect(url_for('index'))

@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        username = request.form.get('username')
        if not username:
            flash('Username cannot be empty.')
            return redirect(url_for('dashboard'))
        new_user = User(username=username)
        db.session.add(new_user)
        db.session.commit()
        flash('User added successfully!')
    except Exception as e:
        db.session.rollback()
        flash('Error adding user: {}'.format(str(e)))
    return redirect(url_for('dashboard'))
