# from flask import Blueprint, render_template, redirect, url_for, request, flash
# from flask_login import login_user, logout_user, current_user, login_required
# from .models import User, Transaction
# from . import db, bcrypt
# from sqlalchemy import or_
# from .models import User, Transaction, Budget


# auth_blueprint = Blueprint('auth', __name__)

# @auth_blueprint.route('/')
# def home():
#     return redirect(url_for('auth.login'))

# @auth_blueprint.route('/login', methods=['GET', 'POST'])
# def login():
#     errors = {}

#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')

#         user = User.query.filter_by(email=email).first()

#         if not user or not bcrypt.check_password_hash(user.password, password):
#             return redirect(url_for('auth.login', invalid="1"))


#         login_user(user)
#         return redirect(url_for('auth.dashboard', login_success="1"))

#     return render_template('login.html')


# @auth_blueprint.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         email = request.form.get('email')
#         password = request.form.get('password')

#         errors = {}

#         # Field validations
#         if len(username) < 3:
#             errors['username'] = "Username must be at least 4 characters long"

#         if '@' not in email:
#             errors['email'] = "Enter a valid email address"

#         if len(password) < 6:
#             errors['password'] = "Password must be at least 6 characters"

#         # Check for duplicates
#         existing_user = User.query.filter(
#             or_(User.username == username, User.email == email)
#         ).first()

#         if existing_user:
#             errors['email'] = "Email or Username already exists. Try Login!"

#         # If error exists return same page
#         if errors:
#             return render_template('register.html',
#                                    errors=errors,
#                                    username=username,
#                                    email=email)

#         hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
#         new_user = User(username=username, email=email, password=hashed_password)

#         db.session.add(new_user)
#         db.session.commit()

#         return redirect(url_for('auth.login', registered="1"))


#     return render_template('register.html', errors={}, username="", email="")



# @auth_blueprint.route("/set-budget", methods=["POST"])
# @login_required
# def set_budget():
#     category = request.form.get("category")
#     limit_amount = float(request.form.get("limit_amount"))

#     budget = Budget.query.filter_by(user_id=current_user.id, category=category).first()

#     if budget:
#         budget.limit_amount = limit_amount
#     else:
#         new_budget = Budget(user_id=current_user.id, category=category, limit_amount=limit_amount)
#         db.session.add(new_budget)

#     db.session.commit()
#     return redirect(url_for("auth.dashboard", budget_set="1"))




# @auth_blueprint.route('/dashboard')
# @login_required
# def dashboard():
#     filter_type = request.args.get('type')
#     filter_category = request.args.get('category')
#     filter_month = request.args.get('month')
#     filter_year = request.args.get('year')

#     # Fetch all user transactions (for chart data)
#     all_transactions = Transaction.query.filter_by(user_id=current_user.id).all()

#     # Apply filters to table data only
#     query = Transaction.query.filter_by(user_id=current_user.id)

#     if filter_type and filter_type != "all":
#         query = query.filter_by(type=filter_type)

#     if filter_category and filter_category != "all":
#         query = query.filter_by(category=filter_category)

#     if filter_month and filter_month != "all":
#         query = query.filter(db.extract('month', Transaction.date) == int(filter_month))

#     if filter_year and filter_year != "all":
#         query = query.filter(db.extract('year', Transaction.date) == int(filter_year))

#     filtered_transactions = query.all()

#     total_income = sum(t.amount for t in filtered_transactions if t.type == 'income')
#     total_expense = sum(t.amount for t in filtered_transactions if t.type == 'expense')
#     net_balance = total_income - total_expense

#     # -----------------------------------
#     # Month & Year dropdown source
#     # -----------------------------------
#     months_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
#                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

#     year_list = sorted(set(t.date.year for t in all_transactions))

#     # -----------------------------------
#     # Chart data from ALL transactions (not filtered)
#     # -----------------------------------
#     from collections import defaultdict

#     monthly_data = defaultdict(lambda: {"income": 0, "expense": 0})
#     for t in all_transactions:
#         month = t.date.strftime("%b")
#         monthly_data[month][t.type] += t.amount

#     months = list(monthly_data.keys())
#     income_values = [monthly_data[m]["income"] for m in months]
#     expense_values = [monthly_data[m]["expense"] for m in months]

#     category_data = defaultdict(float)
#     for t in all_transactions:
#         if t.type == "expense":
#             category_data[t.category] += t.amount

#     # Default categories so dropdown is not empty
#     default_categories = ["Food", "Travel", "Shopping", "Rent", "Bills", "Salary"]

#     # Merge user categories with default categories
#     categories = sorted(set(default_categories + [t.category for t in all_transactions]))
#     category_values = list(category_data.values())

#     # Fetch all budgets for user
#     budgets = {b.category: b.limit_amount for b in Budget.query.filter_by(user_id=current_user.id).all()}

#     # Check exceeded categories for warning UI
#     exceeded_categories = []
#     for cat, spend in category_data.items():
#         if cat in budgets and spend > budgets[cat]:
#             exceeded_categories.append(cat)


#     return render_template(
#         'dashboard.html',
#         user=current_user,
#         transactions=filtered_transactions,
#         total_income=total_income,
#         total_expense=total_expense,
#         net_balance=net_balance,
#         months=months,
#         income_values=income_values,
#         expense_values=expense_values,
#         categories=categories,
#         category_values=category_values,
#         months_list=months_list,
#         year_list=year_list,
#         exceeded_categories=exceeded_categories,
#         budgets=budgets

#     )


# @auth_blueprint.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('auth.login', loggedout="1"))









from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required
from .models import User, Transaction
from . import db, bcrypt
from sqlalchemy import or_
from .models import User, Transaction, Budget


auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/')
def home():
    return redirect(url_for('auth.login'))

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    errors = {}

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not user or not bcrypt.check_password_hash(user.password, password):
            return redirect(url_for('auth.login', invalid="1"))


        login_user(user)
        return redirect(url_for('auth.dashboard', login_success="1"))

    return render_template('login.html')


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        errors = {}

        # Field validations
        if len(username) < 3:
            errors['username'] = "Username must be at least 4 characters long"

        if '@' not in email:
            errors['email'] = "Enter a valid email address"

        if len(password) < 6:
            errors['password'] = "Password must be at least 6 characters"

        # Check for duplicates
        existing_user = User.query.filter(
            or_(User.username == username, User.email == email)
        ).first()

        if existing_user:
            errors['email'] = "Email or Username already exists. Try Login!"

        # If error exists return same page
        if errors:
            return render_template('register.html',
                                   errors=errors,
                                   username=username,
                                   email=email)

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login', registered="1"))


    return render_template('register.html', errors={}, username="", email="")

@auth_blueprint.route("/terms")
def terms():
    return render_template("terms.html")


@auth_blueprint.route("/privacy")
def privacy():
    return render_template("privacy.html")


@auth_blueprint.route("/set-budget", methods=["POST"])
@login_required
def set_budget():
    category = request.form.get("category")
    limit_amount = float(request.form.get("limit_amount"))

    budget = Budget.query.filter_by(user_id=current_user.id, category=category).first()

    if budget:
        budget.limit_amount = limit_amount
    else:
        new_budget = Budget(user_id=current_user.id, category=category, limit_amount=limit_amount)
        db.session.add(new_budget)

    db.session.commit()
    return redirect(url_for("auth.dashboard", budget_set="1"))




@auth_blueprint.route('/dashboard')
@login_required
def dashboard():
    filter_type = request.args.get('type')
    filter_category = request.args.get('category')
    filter_month = request.args.get('month')
    filter_year = request.args.get('year')

    # Fetch all transactions for charts
    all_transactions = Transaction.query.filter_by(user_id=current_user.id).all()

    # Apply filters
    query = Transaction.query.filter_by(user_id=current_user.id)

    if filter_type and filter_type != "all":
        query = query.filter_by(type=filter_type)

    if filter_category and filter_category != "all":
        query = query.filter_by(category=filter_category)

    if filter_month and filter_month != "all":
        query = query.filter(db.extract('month', Transaction.date) == int(filter_month))

    if filter_year and filter_year != "all":
        query = query.filter(db.extract('year', Transaction.date) == int(filter_year))

    # Search
    search_query = request.args.get("search", "").strip()

    if search_query:
        query = query.filter(
            Transaction.category.ilike(f"%{search_query}%") |
            Transaction.note.ilike(f"%{search_query}%")
        )

    # Pagination
    page = request.args.get("page", 1, type=int)
    transactions_paginated = query.order_by(Transaction.date.desc()).paginate(
        per_page=8, page=page
    )
    transactions = transactions_paginated.items

    # Totals calculation based on filtered list
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expense = sum(t.amount for t in transactions if t.type == 'expense')
    net_balance = total_income - total_expense

    # Month and Year dropdown
    months_list = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    year_list = sorted(set(t.date.year for t in all_transactions))

    # Chart data
    from collections import defaultdict
    monthly_data = defaultdict(lambda: {"income": 0, "expense": 0})
    category_data = defaultdict(float)

    for t in all_transactions:
        month = t.date.strftime("%b")
        monthly_data[month][t.type] += t.amount
        if t.type == "expense":
            category_data[t.category] += t.amount

    months = list(monthly_data.keys())
    income_values = [monthly_data[m]["income"] for m in months]
    expense_values = [monthly_data[m]["expense"] for m in months]

    # Ensure dropdown category list is not empty
    default_categories = ["Food","Travel","Shopping","Rent","Bills","Salary"]
    categories = sorted(set(default_categories + [t.category for t in all_transactions]))
    category_values = list(category_data.values())

    # Budget exceeded check
    budgets = {b.category: b.limit_amount for b in Budget.query.filter_by(user_id=current_user.id).all()}
    exceeded_categories = [cat for cat, amt in category_data.items() if cat in budgets and amt > budgets[cat]]

    return render_template(
        'dashboard.html',
        user=current_user,
        transactions=transactions,
        transactions_paginated=transactions_paginated,
        search_query=search_query,
        total_income=total_income,
        total_expense=total_expense,
        net_balance=net_balance,
        months=months,
        income_values=income_values,
        expense_values=expense_values,
        categories=categories,
        category_values=category_values,
        months_list=months_list,
        year_list=year_list,
        exceeded_categories=exceeded_categories,
        budgets=budgets
    )


@auth_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login', loggedout="1"))









