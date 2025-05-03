# Smart Waste Management System ♻️🌍

![Built with Django](https://img.shields.io/badge/Backend-Django-green)
![Frontend](https://img.shields.io/badge/Frontend-HTML%2FCSS%2FJS-blue)
![Database](https://img.shields.io/badge/Database-PostgreSQL-lightblue)
![Machine Learning](https://img.shields.io/badge/ML-LogisticRegression-orange)
![Chatbot](https://img.shields.io/badge/Chatbot-Dialogflow-yellowgreen)
![License](https://img.shields.io/badge/license-MIT-blue)

A full-stack platform to help communities and organizations streamline waste collection and recycling. This project enables users to schedule pickups, tracks recycling activity, calculates environmental impact (CO₂ savings), and includes an AI-powered chatbot for assistance — all while rewarding users through a points-based system aligned with Massachusetts Bottle Bill regulations.

> ♻️ Making sustainable waste management smarter, measurable, and accessible for everyone.
---

## 🚀 Key Features

- 🗑️ **User Pickup Scheduling** – Schedule garbage pickups by ZIP code and number of bags.
- ✅ **Admin Approval Flow** – Admins review requests and assign drivers.
- 🚚 **Driver Dashboard** – View and update pickup status.
- 🏭 **Redemption Worker Role** – Track and process recyclable materials and credit allocation.
- 📬 **Automated Email Notifications** – For request approval, driver assignment, and status updates.
- 💬 **AI Chatbot** – Built using Landbot.io for real-time assistance.
- 📊 **User Dashboard** – Includes:
  - Pickup History
  - Items Recycled
  - CO₂ Emissions Saved
  - 📈 **ML Model Prediction** of future CO₂ savings using logistic regression.

---

## 🧠 Technologies Used

| Category           | Tool / Library                  | Purpose                                                  |
|--------------------|----------------------------------|----------------------------------------------------------|
| **Frontend**       | HTML, CSS, JavaScript, Bootstrap| Build responsive user interfaces                         |
| **Backend**        | Python, Django             | Handle authentication, roles, scheduling, APIs          |
| **Database**       | PostgreSQL                      | Persist user data, pickups, credits                      |
| **Machine Learning**| Scikit-learn                    | Logistic regression to predict CO₂ impact                |
| **Chatbot**        | Landbot.io                      | AI-powered user guidance and help flow                   |
| **Visualization**  | Matplotlib                        | Graphs for CO₂ stats and predictions                     |
| **Notifications**  | Django SMTP                     | Automated email alerts                                   |
| **Testing**        | Postman, Manual QA              | API & workflow validation                                |
| **Deployment**     | Render                          | Host and manage the full web app                         |
| **Version Control**| Git, GitHub                     | Collaborative development and code management            |

---


---

## ⚙️ Installation & Setup

1. **Clone the repository**
```bash
git clone https://github.com/NinaadSawant23/smart-waste-management.git
cd smart-waste-management
```
2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
```
3. **Install dependencies**
```bash
pip install -r requirements.txt
```
4. **Run database migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```
5. **Run server**
```bash
python manage.py runserver
```

## 📊 ML Model – CO₂ Impact Predictor
- 🧠 Algorithm: Logistic Regression (Scikit-learn)
- 🔢 Inputs: Number of items recycled, pickup frequency, bag count
- 📈 Output: Projected CO₂ emissions savings


## 👥 Contributors
- Ninaad Sawant – Backend & Machine Learning
- Gitesh Sagvekar – Frontend & Chatbot
- Deepika Konda – Full-Stack Integration
