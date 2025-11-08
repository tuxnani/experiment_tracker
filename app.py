from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///experiment_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    assignments = db.relationship('TaskAssignment', backref='participant', lazy=True, cascade='all, delete-orphan')

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    assignments = db.relationship('TaskAssignment', backref='task', lazy=True, cascade='all, delete-orphan')

class TaskAssignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    progress = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='pending')
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Routes
@app.route('/')
def index():
    participants = Participant.query.all()
    tasks = Task.query.all()
    assignments = TaskAssignment.query.all()
    
    # Calculate statistics
    total_participants = len(participants)
    total_tasks = len(tasks)
    total_assignments = len(assignments)
    completed_assignments = len([a for a in assignments if a.progress == 100])
    
    stats = {
        'participants': total_participants,
        'tasks': total_tasks,
        'assignments': total_assignments,
        'completed': completed_assignments
    }
    
    return render_template('index.html', stats=stats)

@app.route('/participants')
def participants():
    participants = Participant.query.all()
    return render_template('participants.html', participants=participants)

@app.route('/participants/add', methods=['POST'])
def add_participant():
    name = request.form.get('name')
    email = request.form.get('email')
    
    if not name or not email:
        flash('Name and email are required!', 'error')
        return redirect(url_for('participants'))
    
    existing = Participant.query.filter_by(email=email).first()
    if existing:
        flash('Participant with this email already exists!', 'error')
        return redirect(url_for('participants'))
    
    participant = Participant(name=name, email=email)
    db.session.add(participant)
    db.session.commit()
    flash('Participant added successfully!', 'success')
    return redirect(url_for('participants'))

@app.route('/participants/delete/<int:id>')
def delete_participant(id):
    participant = Participant.query.get_or_404(id)
    db.session.delete(participant)
    db.session.commit()
    flash('Participant deleted successfully!', 'success')
    return redirect(url_for('participants'))

@app.route('/tasks')
def tasks():
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)

@app.route('/tasks/add', methods=['POST'])
def add_task():
    title = request.form.get('title')
    description = request.form.get('description')
    
    if not title:
        flash('Task title is required!', 'error')
        return redirect(url_for('tasks'))
    
    task = Task(title=title, description=description)
    db.session.add(task)
    db.session.commit()
    flash('Task added successfully!', 'success')
    return redirect(url_for('tasks'))

@app.route('/tasks/delete/<int:id>')
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('tasks'))

@app.route('/assignments')
def assignments():
    assignments = TaskAssignment.query.all()
    participants = Participant.query.all()
    tasks = Task.query.all()
    return render_template('assignments.html', assignments=assignments, 
                         participants=participants, tasks=tasks)

@app.route('/assignments/add', methods=['POST'])
def add_assignment():
    participant_id = request.form.get('participant_id')
    task_id = request.form.get('task_id')
    
    if not participant_id or not task_id:
        flash('Please select both participant and task!', 'error')
        return redirect(url_for('assignments'))
    
    existing = TaskAssignment.query.filter_by(
        participant_id=participant_id, 
        task_id=task_id
    ).first()
    
    if existing:
        flash('This task is already assigned to this participant!', 'error')
        return redirect(url_for('assignments'))
    
    assignment = TaskAssignment(participant_id=participant_id, task_id=task_id)
    db.session.add(assignment)
    db.session.commit()
    flash('Task assigned successfully!', 'success')
    return redirect(url_for('assignments'))

@app.route('/assignments/update/<int:id>', methods=['POST'])
def update_assignment(id):
    assignment = TaskAssignment.query.get_or_404(id)
    progress = request.form.get('progress', type=int)
    
    if progress is not None and 0 <= progress <= 100:
        assignment.progress = progress
        if progress == 100:
            assignment.status = 'completed'
        elif progress > 0:
            assignment.status = 'in_progress'
        else:
            assignment.status = 'pending'
        
        assignment.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Progress updated successfully!', 'success')
    else:
        flash('Invalid progress value!', 'error')
    
    return redirect(url_for('assignments'))

@app.route('/assignments/delete/<int:id>')
def delete_assignment(id):
    assignment = TaskAssignment.query.get_or_404(id)
    db.session.delete(assignment)
    db.session.commit()
    flash('Assignment deleted successfully!', 'success')
    return redirect(url_for('assignments'))

@app.route('/api/assignments/<int:id>/progress', methods=['POST'])
def update_progress_api(id):
    assignment = TaskAssignment.query.get_or_404(id)
    data = request.get_json()
    progress = data.get('progress')
    
    if progress is not None and 0 <= progress <= 100:
        assignment.progress = progress
        if progress == 100:
            assignment.status = 'completed'
        elif progress > 0:
            assignment.status = 'in_progress'
        else:
            assignment.status = 'pending'
        
        assignment.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({'success': True, 'progress': progress})
    
    return jsonify({'success': False, 'error': 'Invalid progress value'}), 400

# Initialize database
def init_db():
    with app.app_context():
        db.create_all()
        print("Database initialized!")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)