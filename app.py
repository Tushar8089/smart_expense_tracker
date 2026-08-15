from flask import Flask, render_template, request, redirect, url_for
import pickle

app = Flask(__name__)

# Load the trained machine learning model
with open('expense_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Storage for expenses
expenses = []

@app.route('/')
def index():
    # Calculate overall total
    total_spent = sum(item['amount'] for item in expenses)
    
    # Calculate spending by category
    category_summary = {}
    for item in expenses:
        cat = item['category']
        category_summary[cat] = category_summary.get(cat, 0.0) + item['amount']
    
    return render_template('index.html', expenses=expenses, total=total_spent, summary=category_summary)

@app.route('/add', methods=['POST'])
def add_expense():
    desc = request.form.get('description', '').strip()
    amount_str = request.form.get('amount', '0')
    
    if desc and amount_str:
        amount = float(amount_str)
        # AI prediction step
        predicted_category = model.predict([desc])[0]
        
        expenses.insert(0, {
            'description': desc,
            'amount': round(amount, 2),
            'category': predicted_category
        })
        
    return redirect(url_for('index'))

@app.route('/clear', methods=['POST'])
def clear_expenses():
    expenses.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)