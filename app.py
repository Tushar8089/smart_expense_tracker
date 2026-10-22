
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'mysql+pymysql://root:Placement%402027@localhost/smart_expense_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)

with open('expense_model.pkl', 'rb') as f:
    model = pickle.load(f)


@app.route('/')
def index():
    expenses = Expense.query.order_by(Expense.id.desc()).all()

    total_spent = sum(item.amount for item in expenses)

    category_summary = {}
    for item in expenses:
        cat = item.category
        category_summary[cat] = category_summary.get(cat, 0.0) + item.amount

    return render_template(
        'index.html',
        expenses=expenses,
        total=total_spent,
        summary=category_summary
    )


@app.route('/add', methods=['POST'])
def add_expense():
    desc = request.form.get('description', '').strip()
    amount_str = request.form.get('amount', '0')

    if desc and amount_str:
        amount = float(amount_str)

        predicted_category = model.predict([desc])[0]

        expense = Expense(
            description=desc,
            amount=round(amount, 2),
            category=predicted_category
        )

        db.session.add(expense)
        db.session.commit()

    return redirect(url_for('index'))


@app.route('/clear', methods=['POST'])
def clear_expenses():
    Expense.query.delete()
    db.session.commit()

    return redirect(url_for('index'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=5000)