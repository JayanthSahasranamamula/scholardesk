# 📚 ScholarDesk

A full-stack academic resource manager built with Flask.

ScholarDesk is a web application designed to help students organise their notes, subjects, tags, and reference links in one structured system. It goes beyond simple note-taking by introducing categorisation, tagging, and resource management — all backed by authentication, a relational database, and REST-style API endpoints.

This project was built as a practical exploration of backend development, database design, and cloud deployment.

**Live Application:**
https://scholardesk.onrender.com

# 🚀 Features

**🔐 Authentication**
1. User registration with secure password hashing (bcrypt)
2. Login and logout functionality
3. CSRF protection using Flask-WTF
4. Session management via Flask-Login

**📝 Notes System (Full CRUD)**
1. Create new notes
2. Edit existing notes
3. Delete notes
4. View all notes associated with the logged-in user

**📂 Subject & Tag Management**
1. Assign each note to a subject
2. Add comma-separated tags
3. Categorise and organise content clearly

**🔗 Resource Linking**
1. Attach external links to notes
2. Clickable references open in a new tab
3. Enables ScholarDesk to function as a knowledge hub

**🌐 API Endpoints**
1. /api/user – Returns authenticated user information in JSON
2. /api/notes – Returns all user notes in JSON format

These endpoints demonstrate backend data serialization and authenticated REST-style responses.

**🎨 UI & UX**
1. Bootstrap-based responsive layout
2. Clean navigation bar with authentication awareness
3. Flash messaging for feedback
4. Card-based note display

**☁️ Deployment**

1. Deployed on Render
2. Gunicorn production server
3. Environment variable-based configuration
4. CSRF secret management in production

# 🛠 Tech Stack

**Backend**
1. Python 3
2. Flask
3. Flask-Login
4. Flask-WTF
5. Flask-Bcrypt
6. Flask-SQLAlchemy

**Database**
1. SQLite (development)
2. Cloud-hosted database (Render environment)

**Frontend**
1. HTML (Jinja2 templating)
2. Bootstrap 5

**Testing**
1. Pytest
2. pytest-flask

**Deployment**
1. Render (Web Service)
2. Gunicorn (WSGI server)

# 📦 Project Structure
```
scholardesk/
│
├── app.py
├── models.py
├── forms.py
├── extensions.py
├── templates/
├── tests/
├── requirements.txt
└── README.md
```

1. app.py – Application routes and configuration
2. models.py – SQLAlchemy models
3. forms.py – Flask-WTF forms
4. extensions.py – Database and extension initialization
5. templates/ – Jinja2 HTML templates
6. tests/ – Basic pytest suite

# 💻 Running Locally

**1️⃣ Clone the repository**
```
git clone https://github.com/JayanthSahasranamamula/scholardesk.git
cd scholardesk
```

**2️⃣ Create virtual environment**
```
python -m venv venv
venv\Scripts\activate   (Windows)
source venv/bin/activate  (Mac/Linux)
```

**3️⃣ Install dependencies**
`pip install -r requirements.txt`

**4️⃣ Run the application**
`python app.py`

Visit http://127.0.0.1:5000

# 🧪 Running Tests

`pytest`

This runs the basic test suite covering:
1. Homepage availability
2. Login page
3. Register page
4. API authentication behavior

# 🌐 Live Demo

A live version of the application is available at: https://scholardesk.onrender.com.

All features can be tested **directly** through the deployed instance.

# 🧠 What This Project Demonstrates

This project reflects practical understanding of:
1. Authentication workflows
2. Secure password handling
3. CSRF protection
4. Relational database modeling
5. REST-style API design
6. Cloud deployment
7. Production configuration
8. Debugging production errors
9. Code refactoring and modularisation
10. Basic automated testing
ScholarDesk was built incrementally, with structured refactoring and deployment as part of the learning process.

# 🔮 Possible Future Improvements

1. PostgreSQL integration for full production persistence
2. Advanced search and filtering
3. Tag-based filtering
4. User profile management
5. Pagination for large note sets

# 📌 Final Note
ScholarDesk is not just a note-taking application. It represents a complete backend lifecycle:

Design → Build → Refactor → Test → Deploy → Debug → Stabilise

The focus of this project was to build a clean, structured, production-aware Flask application that demonstrates backend fundamentals and deployment readiness.