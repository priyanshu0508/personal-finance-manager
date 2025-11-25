# Personal Finance Manager:

A clean and powerful web-based personal finance tracking application built with **Flask**, allowing users to manage income, expenses, budgets, analytics, search, pagination, and more all inside a beautiful modern UI.

---

## Features:-

### **User Authentication:-**

* Register / Login / Logout
* Password hashing using **bcrypt**
* Flash messages for success/error states

### **Transaction Management:-**

* Add, edit, and delete income or expense records
* Category selection & auto-categorized views
* Notes, dates, and amount tracking
* Instant UI feedback using Toastify

### **Filtering System:-**

Filter transactions by:-

* Type (Income / Expense)
* Category
* Month
* Year

### **Search + Pagination:-**

* Search by category, amount, or note
* Paginated transactions for large datasets
* Clean Previous/Next navigation

### **Interactive Financial Analytics:-**

Powered by **Chart.js**

* Monthly Income vs Expense Bar Chart
* Category-Wise Expense Pie Chart
* Auto-calculated totals (income, expense, balance)

### 🧾 **Budget Management:-**

* Set monthly limits per category
* Warning indicators
* Red-dot badge for exceeded categories
* Toast notification on limit breach

### **Dark Mode (Configurable):-**

* Tailwind’s class-based dark mode setup
* Ready for theme toggle integration

---

## 🏗️ Tech Stack

| Component      | Technology                                  |
| -------------- | ------------------------------------------- |
| Backend        | Flask, SQLAlchemy                           |
| Frontend       | TailwindCSS, HTML, JS                       |
| Charts         | Chart.js                                    |
| Authentication | Flask-Login, bcrypt                         |
| Database       | SQLite (can be changed to MySQL/PostgreSQL) |
| Notifications  | Toastify JS                                 |

---

## 📁 Project Structure

```
personal_finance_manager/
│
├── app.py
├── finance/
│   ├── __init__.py
│   ├── auth.py
│   ├── transactions.py
│   ├── models.py
│   ├── filters.py
│   ├── static/
│   └── templates/
│       ├── login.html
│       ├── register.html
│       ├── dashboard.html
│       ├── add_transaction.html
│       ├── edit_transaction.html
│       ├── terms.html
│       ├── privacy.html
│
├── venv/
└── requirements.txt
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```sh
git clone https://github.com/your-username/personal-finance-manager.git
cd personal-finance-manager
```

### 2️⃣ Create Virtual Environment

```sh
python -m venv venv
```

### 3️⃣ Activate Environment

**Windows**

```sh
venv\Scripts\activate
```

**Mac/Linux**

```sh
source venv/bin/activate
```

### 4️⃣ Install Dependencies

```sh
pip install -r requirements.txt
```

### 5️⃣ Run Application

```sh
python app.py
```

Visit:

```
http://127.0.0.1:5000
```

---

## 🔐 Environment Variables:-

You may use a `.env` file:

```
SECRET_KEY=your_secret_key
FLASK_ENV=development


Would you like me to also create a **perfect README badge header**, or generate a **professional GitHub project cover image**?
