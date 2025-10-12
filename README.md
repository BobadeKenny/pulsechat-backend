
# ⚙️ PulseChat — Backend API

PulseChat Backend is a **Django + Channels** application that powers real-time messaging, authentication, and user management for the PulseChat mobile app. It provides REST and WebSocket APIs for secure, scalable chat functionality.

---

## 🚀 Features

- 🔐 **JWT Authentication** — Login, signup, and token refresh using SimpleJWT  
- 💬 **Real-time Communication** — Powered by Django Channels & WebSockets  
- 🗂 **User Profiles** — Extended custom user model for flexibility  
- 📨 **Message Persistence** — Chats stored and retrieved from the database  


---

## 🧩 Tech Stack

| Category | Technology |
|-----------|-------------|
| Framework | [Django](https://www.djangoproject.com/) |
| Realtime | [Django Channels](https://channels.readthedocs.io/) |
| Authentication | [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/) |
| Database | PostgreSQL  |
| Message Queue | Redis (for Channels layer) |
| API | Django REST Framework |
| Deployment | Docker / Gunicorn / Daphne |

---

## 📜 License

This project is licensed under the MIT License
.
