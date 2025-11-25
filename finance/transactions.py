from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from .models import Transaction, Budget  # <-- Fix here
from . import db


transaction_blueprint = Blueprint('transaction', __name__)

@transaction_blueprint.route('/add', methods=['GET', 'POST'])
@login_required
def add_transaction():
    if request.method == 'POST':
        t_type = request.form.get('type')
        category = request.form.get('category')
        amount = float(request.form.get('amount'))
        date_str = request.form.get('date')
        note = request.form.get('note')

        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

        new_transaction = Transaction(
            user_id=current_user.id,
            type=t_type,
            category=category,
            amount=amount,
            date=date_obj,
            note=note
        )
        db.session.add(new_transaction)
        db.session.commit()

        # Only check budget when expense is added
        if t_type == "expense":
            budget = Budget.query.filter_by(user_id=current_user.id, category=category).first()

            if budget:
                total_expense = sum(t.amount for t in Transaction.query.filter_by(
                    user_id=current_user.id,
                    category=category,
                    type="expense"
                ).all())

                if total_expense > budget.limit_amount:
                    return redirect(url_for('auth.dashboard', exceeded=category))

        flash("Transaction added successfully!", "success")
        return redirect(url_for('auth.dashboard'))

    today_date = datetime.today().date().isoformat()
    return render_template('add_transaction.html', today=today_date)



# ======================
# ADD THESE BELOW
# ======================

@transaction_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(id):
    transaction = Transaction.query.get_or_404(id)

    if transaction.user_id != current_user.id:
        return redirect(url_for('auth.dashboard'))

    if request.method == 'POST':
        transaction.type = request.form.get('type')
        transaction.category = request.form.get('category')
        transaction.amount = float(request.form.get('amount'))
        date_str = request.form.get('date')
        transaction.date = datetime.strptime(date_str, "%Y-%m-%d").date()
        transaction.note = request.form.get('note')

        db.session.commit()
        flash("Transaction updated successfully!", "success")
        return redirect(url_for('auth.dashboard'))

    return render_template('edit_transaction.html', transaction=transaction)


@transaction_blueprint.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)

    if transaction.user_id != current_user.id:
        return redirect(url_for('auth.dashboard'))

    db.session.delete(transaction)
    db.session.commit()
    flash("Transaction deleted successfully!", "success")
    return redirect(url_for('auth.dashboard'))
