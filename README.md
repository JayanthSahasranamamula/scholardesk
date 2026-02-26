# 📚 ScholarDesk

A full-stack academic resource manager built with Flask and PostgreSQL.

ScholarDesk is a production-deployed web application designed to help students organise notes, subjects, relational tags, and reference links in a structured, searchable system. It combines authentication, relational database modelling, REST-style API endpoints, and cloud deployment into a cohesive backend project.

This project was built as a practical exploration of full-stack development, database architecture, and deployment in a real production environment.

**Live Application:**  
https://scholardesk.onrender.com

---

# 🚀 Features

## 🔐 Authentication

- Secure user registration with bcrypt password hashing  
- Login and logout via Flask-Login  
- CSRF protection using Flask-WTF  
- Session-based authentication  
- Environment-based secret key configuration for production  

---

## 📝 Notes System (Full CRUD)

ScholarDesk provides a complete CRUD (Create, Read, Update, Delete) workflow for managing academic notes.

Users can:

- Create new notes  
- Edit existing notes  
- Delete notes  
- View all notes associated with their account  

Each note contains:

- Title  
- Subject  
- Content  
- Optional external resource link  
- Relational tags  

Notes are securely tied to the authenticated user and cannot be accessed across accounts.

---

## 🏷 Relational Tagging System

ScholarDesk implements a many-to-many relational tagging model using SQLAlchemy.

Instead of storing tags as simple comma-separated strings, tags are:

- Stored as independent database entities  
- Linked to notes through an association table  
- Normalised (stored in lowercase)  
- Reusable across multiple notes  
- Queryable using relational joins  

This design ensures:

- Proper database normalisation  
- Scalable tag management  
- Accurate filtering  
- No substring-based filtering hacks  

---

## 🔎 Advanced Search & Filtering

ScholarDesk supports database-level filtering using SQLAlchemy query composition.

Users can:

- Search by keyword (title and content)  
- Filter by subject  
- Filter by tag  
- Combine multiple filters in a single query  

Filtering is executed at the database level using:

- `ilike()` for case-insensitive matching  
- SQLAlchemy joins for relational tag filtering  
- Query chaining for combined filters  

This ensures efficient, scalable querying even as data grows.

---

## 🔗 Resource Linking

Each note may optionally include an external reference link.

Features:

- Clickable links open in a new tab  
- Enables integration with textbooks, documentation, research papers, or tutorials  
- Allows ScholarDesk to function as a lightweight knowledge management system  

---

## 🌐 API Endpoints

ScholarDesk exposes authenticated REST-style JSON endpoints:

### `/api/user`
Returns authenticated user information.

### `/api/notes`
Returns all notes belonging to the authenticated user, including relational tags.

Example response:

```json
{
  "id": 1,
  "title": "Flask Basics",
  "subject": "Computer Science",
  "tags": ["backend", "flask", "api"],
  "resource_link": "https://flask.palletsprojects.com/"
}
```

This demonstrates:

- Secure API routing  
- Backend serialization  
- JSON response structuring  
- Relational data transformation  

---

## 🎨 UI & UX

- Bootstrap 5 responsive layout  
- Clean navigation bar with authentication awareness  
- Flash messaging system for user feedback  
- Card-based note display  
- Persistent search/filter inputs  
- Clean and structured layout for readability  

The interface prioritises clarity and usability over visual complexity.

---

## ☁️ Deployment & Production Configuration

ScholarDesk is deployed on Render using:

- PostgreSQL cloud database  
- Gunicorn WSGI production server  
- Environment variable-based configuration  
- Automatic table creation on startup  
- Secure secret key management  

The application supports:

- SQLite (local development)  
- PostgreSQL (production environment)  

Database configuration automatically adapts based on environment variables.

---

# 🛠 Tech Stack

## Backend

- Python 3  
- Flask  
- Flask-Login  
- Flask-WTF  
- Flask-Bcrypt  
- Flask-SQLAlchemy  
- SQLAlchemy ORM  

## Database

- SQLite (development)  
- PostgreSQL (production, Render-hosted)  

## Frontend

- HTML  
- Jinja2 templating  
- Bootstrap 5  

## Testing

- Pytest  
- pytest-flask  

## Deployment

- Render Web Service  
- Gunicorn  

---

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

- `app.py` – Routes, configuration, filtering logic  
- `models.py` – SQLAlchemy models (User, Note, Tag, association table)  
- `forms.py` – Flask-WTF forms  
- `extensions.py` – Extension initialisation  
- `templates/` – Jinja2 templates  
- `tests/` – Basic pytest suite  

---

# 💻 Running Locally

## 1. Clone the repository

```bash
git clone https://github.com/JayanthSahasranamamula/scholardesk.git
cd scholardesk
```

## 2. Create a virtual environment

```bash
python -m venv venv
```

Activate:

- Windows:
  ```bash
  venv\Scripts\activate
  ```

- macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Run the application

```bash
python app.py
```

Visit:

```
http://127.0.0.1:5000
```

---

# 🧪 Running Tests

Run:

```bash
pytest
```

The test suite validates:

- Homepage availability  
- Login and registration routes  
- Basic API authentication behaviour  

---

# 📌 Final Note

ScholarDesk represents a complete backend lifecycle:

Design → Build → Refactor → Test → Deploy → Debug → Stabilise

It demonstrates:

- Authentication workflows  
- Secure password handling  
- CSRF protection  
- Many-to-many relational modelling  
- SQLAlchemy query composition  
- Database-level filtering  
- REST-style API design  
- Cloud deployment with PostgreSQL  
- Production configuration management  
- Incremental refactoring and structured iteration  

This project reflects practical backend engineering and deployment readiness.