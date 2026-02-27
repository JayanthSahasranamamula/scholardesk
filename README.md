# 📚 ScholarDesk

A production-deployed full-stack academic resource manager built with Flask and PostgreSQL.

ScholarDesk is a structured, authentication-driven web application designed to help students organise notes, subjects, relational tags, and reference links in a clean, searchable system. It combines secure authentication, relational database modelling, REST-style API endpoints, pagination, and cloud deployment into a cohesive backend-focused project.

The application evolved incrementally — from a simple CRUD notes app into a relational, production-configured system with user lifecycle management, advanced filtering, and persistent cloud-hosted storage.

**Live Application:**  
https://scholardesk.onrender.com

---

# 🚀 Overview

ScholarDesk focuses on backend architecture, correct relational modelling, secure authentication flows, structured query design, and real-world deployment discipline.

It demonstrates not just feature implementation, but system evolution and production hardening.

---

# 🔐 Authentication & Security

ScholarDesk implements secure user authentication using established best practices.

### Features

- Secure user registration with bcrypt password hashing  
- Login and logout using Flask-Login  
- Session-based authentication  
- CSRF protection via Flask-WTF  
- Environment-based secret key configuration  
- Production-safe environment variable management  

Passwords are never stored in plaintext. Authentication relies on hashed verification and session management.

Each user’s data is strictly isolated — notes are scoped to the authenticated user and inaccessible across accounts.

---

# 👤 User Profile Management

ScholarDesk supports full user lifecycle control.

Users can:

- View profile information  
- Update username  
- Update email  
- Change password securely  
- Permanently delete their account  

Account deletion:

- Logs the user out safely  
- Removes the user record  
- Cascades deletion to associated notes  
- Maintains referential integrity via SQLAlchemy cascade rules  

This ensures data ownership and clean lifecycle management.

---

# 📝 Notes System (Full CRUD)

ScholarDesk provides a complete Create → Read → Update → Delete workflow.

Each authenticated user can:

- Create new notes  
- Edit existing notes  
- Delete notes  
- View paginated note listings  

Each note includes:

- Title  
- Subject  
- Content  
- Optional external resource link  
- Relational tags  

All note operations are securely bound to the authenticated user.

---

# 🏷 Relational Tagging Architecture

ScholarDesk uses a many-to-many relational tagging system.

Instead of storing tags as comma-separated strings:

- Tags are independent database entities  
- Notes and tags are linked via an association table  
- Tags are normalised (lowercase) before storage  
- Tags are reusable across notes  
- Filtering uses relational joins  

### Technical Implementation

- SQLAlchemy many-to-many relationship  
- Association table between `Note` and `Tag`  
- Dynamic tag creation during note submission  
- Reuse of existing tags when names match  

This design ensures:

- Database normalisation  
- Elimination of duplicate tag strings  
- Scalable filtering  
- Clean relational structure  

---

# 🔎 Advanced Search & Filtering

ScholarDesk performs filtering directly at the database level.

Users can:

- Search by keyword (title and content)  
- Filter by subject  
- Filter by relational tag  
- Combine filters simultaneously  

### Implementation Details

- `ilike()` for case-insensitive matching  
- SQLAlchemy query chaining  
- `join()` for relational tag filtering  
- Dynamic query composition  
- Pagination integration  

Filtering is executed in SQL, not in memory, ensuring scalable performance.

---

# 📄 Pagination

To support scalability:

- Notes are paginated (5 per page)  
- Page number passed via query parameters  
- Results ordered by most recent first  
- Pagination integrates seamlessly with filters  

This prevents long scroll lists and improves usability as data grows.

---

# 🔗 Resource Linking

Each note may optionally include an external reference link.

This allows:

- Linking documentation  
- Referencing research material  
- Attaching tutorials  
- Creating a lightweight academic knowledge system  

Links open in a new tab to preserve workflow continuity.

---

# 🌐 Authenticated API Endpoints

ScholarDesk exposes secure JSON endpoints to demonstrate backend serialization.

## `/api/user`

Returns authenticated user information:

```json
{
  "id": 1,
  "username": "student",
  "email": "student@example.com"
}
```

## `/api/notes`

Returns all notes belonging to the authenticated user, including relational tags:

```json
{
  "id": 1,
  "title": "Flask Basics",
  "subject": "Computer Science",
  "tags": ["backend", "flask", "api"],
  "resource_link": "https://flask.palletsprojects.com/"
}
```

### Demonstrated Concepts

- Secure route protection  
- JSON serialization  
- Relationship flattening (`Tag` → list of strings)  
- REST-style response formatting  

---

# 🎨 User Interface

ScholarDesk uses Bootstrap 5 for responsive layout.

### UI Characteristics

- Responsive design  
- Authentication-aware navigation bar  
- Flash messaging system  
- Card-based note presentation  
- Persistent search/filter inputs  
- Minimalist, clarity-focused layout  

The interface prioritises readability and structural clarity over visual complexity.

---

# ☁️ Deployment Architecture

ScholarDesk runs in a production-ready configuration.

### Hosting

- Render Web Service  
- Gunicorn WSGI server  

### Database

- Neon-hosted PostgreSQL (production)  
- SQLite (local development)  

### Configuration

- Automatic environment detection  
- Secure `DATABASE_URL` handling  
- SSL-enabled PostgreSQL connection  
- Automatic table creation on startup  

The application adapts automatically based on environment variables, allowing seamless local and production operation.

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
- PostgreSQL (Neon, production)  

## Frontend

- HTML  
- Jinja2 templating  
- Bootstrap 5  

## Testing

- Pytest  
- pytest-flask  

## Deployment

- Render  
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

### File Overview

- `app.py` – Routes, filtering logic, pagination, deployment configuration  
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

**Windows**
```bash
venv\Scripts\activate
```

**macOS/Linux**
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

SQLite will be used automatically in local development.

---

# 🧪 Running Tests

Run:

```bash
pytest
```

The test suite validates:

- Homepage availability  
- Authentication routes  
- API access behaviour  
- Basic application boot integrity  

---

# 📌 Version

Current stable release: **v1.4.1**

This version includes:

- Relational many-to-many tagging  
- Database-level tag filtering  
- Advanced search  
- Pagination  
- Full profile management  
- Account deletion with cascade handling  
- Persistent PostgreSQL production storage  
- Production-safe configuration management  

---

# 🧠 Engineering Focus

ScholarDesk demonstrates practical backend engineering concepts:

- Secure authentication workflows  
- Password hashing and verification  
- CSRF protection  
- Many-to-many relational modelling  
- SQLAlchemy join-based filtering  
- Database-level query composition  
- Pagination design  
- REST-style API development  
- Environment-based configuration  
- Cloud deployment discipline  
- Production debugging  
- Incremental architectural evolution  

---

ScholarDesk represents a structured backend system built through deliberate iteration, debugging, and production stabilization.