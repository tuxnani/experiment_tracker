# 🧪 Experiment Tracking Dashboard

A comprehensive Flask web application for managing experiment participants, tasks, and progress tracking with visual progress bars.

## ✨ Features

- **Participant Management**: Add, view, and delete participants
- **Task Management**: Create and manage experiment tasks
- **Task Assignment**: Assign tasks to participants
- **Progress Tracking**: Update and visualize progress with dynamic progress bars
- **Dashboard Overview**: Real-time statistics and quick actions
- **Responsive UI**: Beautiful, modern interface that works on all devices

## 📁 Project Structure

```
experiment_tracker/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── templates/
│   ├── base.html              # Base template with navigation
│   ├── index.html             # Dashboard page
│   ├── participants.html      # Participants management
│   ├── tasks.html             # Tasks management
│   └── assignments.html       # Assignment & progress tracking
└── instance/
    └── experiment_tracker.db  # SQLite database (auto-created)
```

## 🚀 Installation & Setup

### Step 1: Create Project Directory
```bash
mkdir experiment_tracker
cd experiment_tracker
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
Create `requirements.txt`:
```txt
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
```

Install packages:
```bash
pip install -r requirements.txt
```

### Step 4: Create Folder Structure
```bash
mkdir templates
mkdir instance
```

### Step 5: Add All Files
Place the following files in their respective locations:
- `app.py` in the root directory
- All `.html` files in the `templates/` folder

### Step 6: Run the Application
```bash
python app.py
```

The application will:
1. Initialize the database automatically
2. Start the development server
3. Be accessible at `http://127.0.0.1:5000`

## 📱 Usage Guide

### Dashboard (`/`)
- View statistics: total participants, tasks, assignments, and completed tasks
- Quick access to add participants, create tasks, and assign tasks

### Participants (`/participants`)
- **Add Participant**: Click "Add Participant" button, fill in name and email
- **View All**: See list of all participants with their assigned task counts
- **Delete**: Remove participants (will also remove their assignments)

### Tasks (`/tasks`)
- **Create Task**: Click "Add Task" button, provide title and description
- **View All**: See list of all tasks and how many times they're assigned
- **Delete**: Remove tasks (will also remove related assignments)

### Assignments (`/assignments`)
- **Assign Task**: Click "Assign Task" button, select participant and task
- **Update Progress**: Click edit button on any assignment
  - Enter progress value (0-100%)
  - Progress bar updates in real-time
  - Status automatically updates:
    - 0%: Pending
    - 1-99%: In Progress
    - 100%: Completed
- **View Progress**: Visual progress bars with percentages in table
- **Delete**: Remove assignments

## 🎨 Features in Detail

### Progress Tracking System
- **Visual Progress Bars**: Color-coded gradient bars showing completion percentage
- **Status Badges**: Automatic status updates based on progress
  - 🟡 Pending (0%)
  - 🔵 In Progress (1-99%)
  - 🟢 Completed (100%)
- **Live Updates**: Real-time preview when adjusting progress
- **Timestamp Tracking**: Records when assignments are created and updated

### Database Schema
```sql
Participant
- id (Primary Key)
- name
- email (Unique)
- created_at

Task
- id (Primary Key)
- title
- description
- created_at

TaskAssignment
- id (Primary Key)
- participant_id (Foreign Key)
- task_id (Foreign Key)
- progress (0-100)
- status (pending/in_progress/completed)
- assigned_at
- updated_at
```

## 🔧 Customization

### Change Color Scheme
Edit the CSS variables in `templates/base.html`:
```css
:root {
    --primary-color: #4f46e5;    /* Change primary color */
    --secondary-color: #7c3aed;  /* Change secondary color */
}
```

### Change Secret Key
In `app.py`, update:
```python
app.config['SECRET_KEY'] = 'your-secure-secret-key-here'
```

### Database Location
The SQLite database is stored in `instance/experiment_tracker.db`. To change location, modify:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///path/to/your/db.db'
```

## 🐛 Troubleshooting

### Port Already in Use
Change the port in `app.py`:
```python
app.run(debug=True, port=5001)
```

### Database Not Created
Manually initialize:
```python
from app import app, db
with app.app_context():
    db.create_all()
```

### Template Not Found
Ensure all HTML files are in the `templates/` folder

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Dashboard |
| GET | `/participants` | View participants |
| POST | `/participants/add` | Add participant |
| GET | `/participants/delete/<id>` | Delete participant |
| GET | `/tasks` | View tasks |
| POST | `/tasks/add` | Add task |
| GET | `/tasks/delete/<id>` | Delete task |
| GET | `/assignments` | View assignments |
| POST | `/assignments/add` | Assign task |
| POST | `/assignments/update/<id>` | Update progress |
| GET | `/assignments/delete/<id>` | Delete assignment |

## 🔐 Security Notes

- Change the `SECRET_KEY` before deployment
- Use environment variables for sensitive data
- Enable HTTPS in production
- Implement user authentication for production use
- Add input validation and sanitization

## 📈 Future Enhancements

- User authentication system
- Export data to CSV/Excel
- Email notifications for task assignments
- Advanced filtering and search
- Charts and analytics
- Task deadlines and reminders
- File attachments for tasks

## 📝 License

This project is open source and available for educational purposes.

## 🤝 Support

For issues or questions, please check the troubleshooting section or create an issue.

---

**Happy Experimenting! 🧪**
