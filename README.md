# TRINETRA: Advanced AI Surveillance & Legal System v3.0

> **"Eyes of the Law, Mind of a Machine."**

Trinetra is a cutting-edge **Intelligence Officer Portal** designed for high-security clearance operations. It integrates **Generative AI** for log analysis and legal drafting with a futuristic **Cyberpunk/Glassmorphism UI**.

---

## 🚀 Key Features

### 1. 🧠 Intelligence Lab (AI Node)
- **Universal File Analyzer**: Upload logs, code, or documents for instant AI analysis.
- **Legal Auto-Drafter**: Generates professional PDF legal opinions based on case facts.
- **Hybrid Engine**: Connects to **Hugging Face Spaces** for heavy lifting, with local fallbacks.

### 2. 🛡️ Advanced Security
- **Iron Dome Upgrade**: Certificate-based binding and IP-locking middleware (Configurable).
- **Biometric Logic**: Ready for WebAuthn (Fingerprint/FaceID) integration.
- **Role-Based Access**: Strict separation between Commanders (Admins) and Field Officers.

### 3. 💻 Future-Ready UI
- **Glassmorphism**: Translucent panels, neon accents, and blurs.
- **Reactive Dashboard**: Real-time threat levels and case tracking.
- **Responsive**: Fully functional on tactical tablets and desktop command centers.

---

## 🛠️ Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend** | Python 3.11 + Django 5.0 | Core logic and ORM |
| **Database** | PostgreSQL (Neon DB) | Cloud-native serverless SQL |
| **AI Engine** | Gradio Client + Hugging Face | Interface for LLM operations |
| **Frontend** | HTML5 + Tailwind + Vanilla JS | Lightweight, high-performance UI |
| **Deployment**| Azure App Service | Enterprise-grade hosting |

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.11+
- Git

### 1. Local Development
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/TRINETRA_REPO.git
cd Trinetra_Root

# Install Dependencies
pip install -r requirements.txt

# Create .env file (See deployment_guide.md for keys)
# Run Migrations
python manage.py migrate

# Create Superuser (Admin)
python manage.py createsuperuser

# Start Server
python manage.py runserver
```

### 2. Azure Deployment
This project is **Cloud-Ready**.
- **Startup Script**: `startup.sh` includes migration and user creation.
- **Database**: Configured for `DATABASE_URL` (Postgres).
- **Static Files**: Served via `WhiteNoise`.

👉 **[Read the Deployment Guide](deployment_guide.md)** for full Azure commands.

---

## 🔐 Security Protocols (Config)

The system runs in **Prototyping Mode** by default for ease of testing.

- **Enable Iron Dome**: Set `TRINETRA_STRICT_FIREWALL = True` in `config/settings.py`.
- **IP Allowlist**: Configure `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` in production.

---

## 🤝 Contribution
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---
**Verified By:** Trinetra Command Command
**Clearance Level:** TOP SECRET // NOFORN
