import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# 1. Dataset covering various spending categories
data = {
    'description': [
        'Starbucks coffee', 'McDonalds burger', 'Grocery shopping', 'Dominos pizza', 'Dinner with friends', 'Milk and bread',
        'Uber trip', 'Bus ticket', 'Metro recharge', 'Petrol fuel', 'Auto rickshaw', 'Flight ticket',
        'Netflix subscription', 'Movie tickets', 'Spotify premium', 'Video game purchase', 'Cinema popcorn',
        'Electricity bill', 'Wi-Fi broadband bill', 'Water bill', 'Mobile recharge', 'LPG cylinder',
        'Amazon shopping shoes', 'T-shirt purchase', 'Pharmacy medicines', 'Gym membership', 'Doctor consultation fee'
    ],
    'category': [
        'Food & Dining', 'Food & Dining', 'Food & Dining', 'Food & Dining', 'Food & Dining', 'Food & Dining',
        'Transportation', 'Transportation', 'Transportation', 'Transportation', 'Transportation', 'Transportation',
        'Entertainment', 'Entertainment', 'Entertainment', 'Entertainment', 'Entertainment',
        'Utilities & Bills', 'Utilities & Bills', 'Utilities & Bills', 'Utilities & Bills', 'Utilities & Bills',
        'Shopping & Personal', 'Shopping & Personal', 'Health & Fitness', 'Health & Fitness', 'Health & Fitness'
    ]
}

df = pd.DataFrame(data)

# 2. Build Pipeline (TF-IDF + Naive Bayes)
model = make_pipeline(TfidfVectorizer(ngram_range=(1, 2)), MultinomialNB())
model.fit(df['description'], df['category'])

# 3. Save the trained model
with open('expense_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("AI Model retrained and saved successfully!")