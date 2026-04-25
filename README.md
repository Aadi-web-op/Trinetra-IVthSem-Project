# TRINETRA: Advanced AI Surveillance & Legal System v3.0

> **"Eyes of the Law, Mind of a Machine."**

Trinetra is a sophisticated **Intelligence Officer Portal** developed as a 2nd-year academic project. It serves as a modern command center for managing cyber cases, analyzing evidence logs, and auto-generating legal drafts. The platform integrates **Generative AI** directly into an officer's workflow, all wrapped in a highly responsive, futuristic **Cyberpunk/Glassmorphism UI**.

---

## 📖 What is this project about?

Trinetra is built to simulate a high-security intelligence and case management system. The primary goal is to empower officers with AI tools to speed up their investigation and legal drafting process. 

A first-time user (or officer) logs into the portal and can:
1. **Manage Cases & Evidence:** Create case files, track suspects, and upload evidence documents.
2. **Consult the AI Lab:** Use a built-in AI chat interface to analyze uploaded log files, parse raw text, or get quick insights on a case.
3. **Generate Legal Drafts:** Input case facts and generate professional, formatted legal PDF opinions instantly using AI.
4. **Command Center (Admin):** Higher-ranking officials have access to an admin dashboard with strict role-based access, audit logging, and security monitoring.

---

## 🛠️ How is it made? (Tech Stack)

The project is structured as a monolithic web application utilizing modern frontend aesthetics without relying on heavy JavaScript frameworks like React.

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend Framework** | Python 3.11 + Django 5.0 | Handles all routing, core logic, and ORM. |
| **Database** | SQLite (Local) / PostgreSQL (NeonDB) | Stores cases, evidence, chat history, and audit logs. |
| **AI Integration** | Hugging Face (Gradio Client) | Connects to external Hugging Face Spaces for heavy LLM lifting, keeping the local app lightweight. |
| **Frontend UI** | HTML5, Tailwind CSS, Vanilla JS | Delivers the sleek "Glassmorphism" design with translucent panels, neon accents, and smooth animations. |
| **Icons & Fonts** | Lucide Icons, Google Fonts (Inter) | Provides the clean, modern aesthetic. |

---

## 📂 Project Structure

The Django project is divided into several modular apps:
- **`officer_portal/`**: The heart of the app. Contains the AI chat interface, case/evidence management, and PDF generation logic.
- **`authentication/`**: Handles secure user login, biometric logic placeholders, and session management.
- **`access_control/`**: Manages Role-Based Access Control (RBAC) ensuring strict separation between standard Officers and Commanders (Admins).
- **`audit_logs/`**: Tracks and records sensitive actions taken on the platform.
- **`config/`**: The core Django settings, including security middleware ("Iron Dome") and database routing.

---

## ⚙️ Setup & Installation

Follow these steps to run the project locally.

### 1. Prerequisites
- Python 3.10+
- Git

### 2. Clone and Setup
```powershell
# Clone the repository
git clone <repository-url>
cd Trinetra-IVthSem-Project/Trinetra-IVthSem-Project

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows:
.\.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate

# Install Dependencies
pip install -r requirements.txt
```

### 3. Environment Variables
To use the AI features, you need a Hugging Face API Token.
Create a `.env` file in the same folder as `manage.py` and add:
```env
HF_API_TOKEN=your_huggingface_token_here
DEBUG=True
```

### 4. Database Setup & Run
```powershell
# Run Migrations to setup the database
python manage.py migrate

# Create a Superuser (Admin account)
python manage.py createsuperuser

# Start the Development Server
python manage.py runserver
```

Once the server is running, visit **[http://localhost:8000/](http://localhost:8000/)** in your browser to access the portal!

---

## 🔐 Security Protocols (Iron Dome)

The system includes custom middleware (`IPFortressMiddleware`) for enhanced security.
- By default, in local development (`DEBUG=True`), strict SSL redirects and IP-locking are bypassed.
- In production (`DEBUG=False`), the system enforces HTTPS, sets secure cookies, and restricts access based on `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`.

---
**Verified By:** Trinetra Command Center  
**Clearance Level:** TOP SECRET // NOFORN
