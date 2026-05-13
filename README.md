# Capstone-Project
# 📚 Libris | University Book Exchange Platform

**Libris** is a robust peer-to-peer resource sharing application designed for university ecosystems. It facilitates the exchange of textbooks, notes, and research papers through a secure, token-based economy, significantly lowering the financial barriers to academic materials.

---

## 🚀 Key Features

* **Token-Based Economy:** Users earn and spend virtual credits to exchange resources, fostering a sustainable circular economy within the campus.
* **Secure Authentication:** A multi-step signup process featuring a session-based.
* **Resource Marketplace:** Full CRUD (Create, Read, Update, Delete) functionality for academic listings with integrated image upload support.
* **Atomic Transactions:** High-integrity backend logic using SQLAlchemy transactions to ensure credit transfers and status updates occur simultaneously, preventing data drift.
* **Automated File Management:** Integrated system-level logic via the `os` module to automatically prune orphaned image files from the server upon resource deletion.
* **Database Versioning:** Managed schema evolution using **Flask-Migrate (Alembic)** to handle database updates without risking existing user data.

---

## 🛠️ Tech Stack

* **Backend:** Python 3.x, Flask
* **Database:** SQLite, Flask-SQLAlchemy (ORM)
* **Migrations:** Flask-Migrate (Alembic)
* **Frontend:** HTML5, CSS3, Jinja2 Templating
* **Environment Management:** Python Virtual Environments (venv)

---

## 📦 Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/shashanktam/Capstone-Project.git](https://github.com/shashanktam/Capstone-Project.git)
cd Capstone-Project
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Initialize the Database
```bash
flask db upgrade
```
### 5. Run the Application
```bash
python app.py
```

## 📂 Project Structure
```
Capstone-Project/
├── app.py              # Application factory & routes
├── models.py           # Database models
├── static/             # Static assets
│   ├── css/
│   └── uploads/
├── templates/          # Jinja2 templates
├── migrations/         # DB migration history
├── requirements.txt    # Dependencies
└── README.md           # Documentation