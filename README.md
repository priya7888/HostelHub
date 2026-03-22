# 🏠 HostelHub — Digital Hostel Management System

<div align="center">

![HostelHub](https://img.shields.io/badge/HostelHub-Hostel%20Management-e8b96a?style=for-the-badge&logo=django&logoColor=black)
![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**A complete digital hostel management portal for students and wardens.**
Built with Django · Dark/Light Theme · WhatsApp Integration · QR Gate System

[🚀 Features](#-features) · [⚙️ Installation](#️-installation) · [📋 URLs](#-urls-reference)

</div>

---

## ✨ Features

### 🎓 Student Portal — 9 Apps

| # | App | Description |
|---|---|---|
| 1 | 🔐 **Login** | Role-based login — Student / Warden |
| 2 | 🏠 **Student Home** | Hero page with animated background |
| 3 | 📊 **Dashboard** | 7 service cards + Emergency SOS |
| 4 | 🍽️ **Mess Voting** | Vote for daily meals and shape weekly menu |
| 5 | 📝 **Complaint System** | Post and track complaints to warden |
| 6 | 🔍 **Lost & Found** | Post and browse lost/found items |
| 7 | 📢 **Notice Board** | View hostel announcements |
| 8 | 🌙 **Night Attendance** | Check attendance records |
| 9 | 🚪 **Outing Request** | Request with parent + warden approval + QR pass |
| 10 | 🚨 **Emergency SOS** | Send instant alert to warden |

### 👮 Warden Portal — 9 Apps

| # | App | Description |
|---|---|---|
| 1 | 🏠 **Warden Home** | Hero page with live stats |
| 2 | 📊 **Dashboard** | 7 cards + QR gate scanner shortcut |
| 3 | 🍽️ **Mess Management** | View votes + add food items |
| 4 | 📝 **Complaints** | Reply and update complaint status |
| 5 | 🔍 **Lost & Found** | View and mark items resolved |
| 6 | 📢 **Notice Board** | Post and delete notices |
| 7 | 🌙 **Attendance** | Mark attendance + quick mark all |
| 8 | 🚪 **Outing Approvals** | Review + approve + WhatsApp notify |
| 9 | 🚨 **SOS Alerts** | View + respond + WhatsApp parent |

---

## 🚪 Outing QR System

Complete 8-step outing process:

```
1. Student submits outing request
        ↓
2. Student sends WhatsApp link to parent
        ↓
3. Parent opens link → Approves or Rejects
        ↓
4. Warden sees request → Reviews → Approves
        ↓
5. QR Pass generated → WhatsApp sent to student
        ↓
6. Gate Scan 1 → CHECKED OUT
   → Attendance: On Leave
   → WhatsApp to parent: "Your child left hostel"
        ↓
7. Gate Scan 2 → RETURNED
   → Attendance: Present
   → WhatsApp to parent: "Your child safely returned"
        ↓
8. Gate Scan 3 → INVALID (QR permanently disabled)
```

---

## 📱 WhatsApp Integration

No API keys needed — uses wa.me links:

| Event | Recipient | Message |
|---|---|---|
| Student submits | Parent | Approval link |
| Parent approves | Warden | Notification |
| Parent rejects | Student | Rejection notice |
| Warden approves | Student | QR pass link |
| Gate scan — checkout | Parent | Child left hostel |
| Gate scan — return | Parent | Child returned safely |

---

## 🛠️ Tech Stack

```
Backend    →  Django 6.0, Python 3.14
Database   →  SQLite
Frontend   →  HTML5, CSS3, Vanilla JavaScript
Fonts      →  Playfair Display + Outfit (Google Fonts)
QR Code    →  qrcode[pil] library
Scanner    →  html5-qrcode CDN library
Theme      →  Dark / Light mode toggle
Accent     →  Amber #e8b96a
```

---

## 📁 Project Structure

```
Hostel_Helper/
│
├── login/                  → Role-based login
├── student_dashboard/      → Student hero page
├── dashboard1/             → Student 7-card dashboard
├── mess/                   → Food voting
├── complaint/              → Complaint system
├── lost_and_found/         → Lost & found board
├── notice_board/           → Notices
├── night_attendance/       → Attendance records
├── emergency_sos/          → SOS alerts
├── outing/                 → Outing request + QR pass
├── student_profile/        → Student profiles
│
├── warden_home/            → Warden hero page
├── warden_dash/            → Warden dashboard + QR scanner
├── warden_mess/            → Mess management
├── warden_complaints/      → Complaint replies
├── warden_lost_found/      → Lost & found management
├── warden_notices/         → Notice posting
├── warden_attendance/      → Attendance marking
├── warden_outings/         → Outing approvals
└── warden_sos/             → SOS management
```

---

## ⚙️ Installation

### Step 1 — Clone repository
```bash
git clone https://github.com/priya7888/HostelHub.git
cd HostelHub/Hostel_Helper
```

### Step 2 — Create virtual environment
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install django pillow qrcode[pil]
```

### Step 4 — Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5 — Create superuser
```bash
python manage.py createsuperuser
```

### Step 6 — Run server
```bash
python manage.py runserver
```

### Step 7 — Open browser
```
http://127.0.0.1:8000/
```

---

## 🔧 Admin Setup

Go to `http://127.0.0.1:8000/admin/` and:

```
1. Create warden users     → set is_staff = True
2. Create student users    → set last_name = room number
3. Create Student Profiles → assign warden to each student
4. Add food items          → for mess voting
5. Post notices            → for notice board
```

---

## 📋 URLs Reference

### Student URLs
| URL | Page |
|---|---|
| `/` | Login |
| `/student/` | Student home |
| `/dashboard/` | Student dashboard |
| `/mess/` | Mess voting |
| `/complaints/` | Complaints |
| `/lost-found/` | Lost & found |
| `/notices/` | Notice board |
| `/attendance/` | Night attendance |
| `/sos/` | Emergency SOS |
| `/outing/` | Outing requests |
| `/outing/qr/<id>/` | QR pass view |

### Warden URLs
| URL | Page |
|---|---|
| `/warden/` | Warden home |
| `/warden/dash/` | Warden dashboard |
| `/warden/dash/scanner/` | QR gate scanner |
| `/warden/mess/` | Mess management |
| `/warden/complaints/` | Complaint replies |
| `/warden/lost-found/` | Lost & found |
| `/warden/notices/` | Notice posting |
| `/warden/attendance/` | Attendance marking |
| `/warden/outings/` | Outing approvals |
| `/warden/sos/` | SOS alerts |
| `/admin/` | Admin panel |

---

## 🎨 Design System

| Property | Dark Mode | Light Mode |
|---|---|---|
| Background | `#0d0d0d` | `#f7f4ef` |
| Accent | `#e8b96a` | `#c47d20` |
| Text | `#f5f2ed` | `#1a1612` |
| Card | `#141414` | `#ffffff` |
| Heading Font | Playfair Display | Playfair Display |
| Body Font | Outfit | Outfit |

---

## 🔒 Security Features

```
✅ Role-based login (Student / Warden)
✅ Student room number verification
✅ Parent approval via UUID token (no login needed)
✅ QR pass with UUID token
✅ Warden scanner only processes assigned students
✅ QR permanently disabled after student returns
✅ CSRF protection on all forms
```

---

## 📦 Dependencies

```
django==6.0.3
pillow
qrcode[pil]
```

---

## 👩‍💻 Developer

**Priya** — Full Stack Django Developer

- GitHub: [@priya7888](https://github.com/priya7888)
- Project: [HostelHub](https://github.com/priya7888/HostelHub)

---

## 📄 License

This project is licensed under the MIT License.

---

<div align="center">

Made with ❤️ using Django + Python

**HostelHub · Student & Warden Portal · 2026–27**

⭐ Star this repo if you found it helpful!

</div>
