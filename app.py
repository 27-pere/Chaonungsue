from flask import Flask, render_template, request
from flask import redirect, url_for
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from recommendation_engine import RecommendationEngine
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session

# from ml.recommender import get_recommendations



books = pd.read_csv("books.csv")

engine = RecommendationEngine(books)

category_matrix = pd.get_dummies(books['category'].str.split("|").apply(pd.Series).stack())

similarity = cosine_similarity(category_matrix)
"""
def get_recommendations(category, top_n=2):
    matched = books[books["category"] == category]

    if matched.empty:
        return ["No similar books found."]

    idx = matched.index[0]
    similarity_scores = list(enumerate(similarity[idx]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    books_indices = [i[0] for i in similarity_scores[1:top_n+1]]

    return books["title"].iloc[books_indices].tolist()

def get_recommendations_by_category(category, top_n=8):
    filtered_books = books[books["category"].str.contains(category, case=False, na=False)]

    if filtered_books.empty:
        return []

    return filtered_books.head(top_n).to_dict(orient="records")
"""

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

app = Flask(__name__)
app.secret_key = "super_secret_key"

init_db()

@app.route("/")
def login_page():
    return render_template("loginpage/login.html")

"""
@app.route("/signup", methods=["POST"])
def signup():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    # For now just print (later you save to database)
    print(name, email, password)

    # Redirect to category page after signup
    return redirect(url_for("category_page"))
"""
@app.route("/category")
def category_page():
    return render_template("askpage/ask.html")
"""
@app.route("/like", methods=["POST"])
def like():
    # Ensure 'book' matches the 'name' attribute in your ask.html <select> or <input>
    selected_item = request.form.get("book") 
    
    try:
        # If get_recommendations expects an index or exact category:
        rec = get_recommendations(selected_item)
        return render_template("homepage/home.html", rec=rec)
    except Exception as e:
        print(f"Error: {e}")
        return "Could not find recommendations for that selection."
"""    
@app.route("/recommend", methods=["POST"])
def recommend():
    category = request.form["category"]
    rec = engine.recommend_by_category(category)
    return render_template("homepage/home.html", rec=rec)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()

            # Check if email already exists
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                return "Email already registered. Try another one."

            # Insert new user
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, hashed_password)
            )
            conn.commit()

        return redirect(url_for("login"))

    return render_template("askpage/ask.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()

        if user and check_password_hash(user[3], password):
            session["user_id"] = user[0]
            session["username"] = user[1]
            return redirect(url_for("home"))
        else:
            return "Invalid username or password"

    # THIS handles GET request
    return render_template("loginpage/login.html")
    

    
@app.route("/home")
def home():
    if "user_id" not in session:
        return redirect(url_for("login_page"))
    
    return render_template("askpage/ask.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))

if __name__ == "__main__":
    app.run(debug=True)