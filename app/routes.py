from flask import render_template, request, redirect, url_for, flash, Response
from app import app, db
from .models import User
import csv

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
        carbon_footprint = request.form.get('carbon_footprint', 0.0)
        if not username:
            flash('Username cannot be empty.')
            return redirect(url_for('dashboard'))
        new_user = User(username=username, carbon_footprint=float(carbon_footprint))
        db.session.add(new_user)
        db.session.commit()
        flash('User added successfully!')
    except Exception as e:
        db.session.rollback()
        flash('Error adding user: {}'.format(str(e)))
    return redirect(url_for('dashboard'))

@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.get(id)
    if not user:
        flash('User not found.')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        try:
            user.username = request.form.get('username', user.username)
            user.carbon_footprint = float(request.form.get('carbon_footprint', user.carbon_footprint))
            db.session.commit()
            flash('User updated successfully!')
        except Exception as e:
            db.session.rollback()
            flash('Error updating user: {}'.format(str(e)))
        return redirect(url_for('dashboard'))
    
    return render_template('edit_user.html', user=user)

@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    try:
        user = User.query.get(id)
        if not user:
            flash('User not found.')
            return redirect(url_for('dashboard'))
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting user: {}'.format(str(e)))
    return redirect(url_for('dashboard'))

@app.route('/search_user', methods=['GET', 'POST'])
def search_user():
    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
        users = User.query.filter(User.username.ilike(f"%{search_query}%")).all()
        return render_template('dashboard.html', users=users)
    return redirect(url_for('dashboard'))

@app.route('/leaderboard')
def leaderboard():
    try:
        users = User.query.order_by(User.carbon_footprint.asc()).all()
        return render_template('leaderboard.html', users=users)
    except Exception as e:
        flash('Error fetching leaderboard: {}'.format(str(e)))
        return redirect(url_for('dashboard'))

@app.route('/export', methods=['GET'])
def export_data():
    try:
        users = User.query.all()
        # Create CSV data
        csv_data = [['ID', 'Username', 'Carbon Footprint']]
        for user in users:
            csv_data.append([user.id, user.username, user.carbon_footprint])
        
        # Create Response object
        def generate():
            for row in csv_data:
                yield ','.join(map(str, row)) + '\n'
        
        return Response(generate(), mimetype='text/csv',
                        headers={'Content-Disposition': 'attachment;filename=users.csv'})
    except Exception as e:
        flash('Error exporting data: {}'.format(str(e)))
        return redirect(url_for('dashboard'))
