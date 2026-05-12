# MAD2 Quiz Master - Vue + Flask Project

MAD2 Quiz Master is a full-stack quiz management web application built using Vue.js for the frontend and Flask REST API for the backend. The application supports admin and user roles, quiz management, scoring, summary charts, caching, and background tasks.

## Features

### Admin Features
- Admin login
- Manage subjects
- Manage chapters
- Manage quizzes
- Add and manage questions
- View registered users
- View admin summary charts
- Export quiz/user details

### User Features
- User signup and login
- View available quizzes
- Attempt quizzes
- View quiz scores
- View result summary

### Background Features
- Redis caching
- Celery background tasks
- Scheduled reminders
- Email/report generation support

## Tech Stack

### Frontend
- Vue.js
- Vite
- Chart.js
- Vue Chart.js

### Backend
- Python
- Flask
- Flask-RESTful
- Flask-JWT-Extended
- Flask-SQLAlchemy
- SQLite
- Redis
- Celery

## Project Structure

```text
Mad2_project_23f3004254/
│
├── app.py
├── requirements.txt
├── backend/
│   ├── api.py
│   ├── config.py
│   ├── models.py
│   ├── task.py
│   ├── worker.py
│   └── templates/
│
└── frontend/
    ├── package.json
    ├── index.html
    └── src/
