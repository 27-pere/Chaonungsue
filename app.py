from flask import Flask, render_template, request
from flask import redirect, url_for
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
# from ml.recommender import get_recommendations

books = pd.read_csv("books.csv")

category_matrix = pd.get_dummies(books['category'].str.split("|").apply(pd.Series).stack())

similarity = cosine_similarity(category_matrix)

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


app = Flask(__name__)
app.secret_key = "supersecretkey"
@app.route("/")
def login():
    return render_template("loginpage/login.html")

@app.route("/signup", methods=["POST"])
def signup():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    # For now just print (later you save to database)
    print(name, email, password)

    # Redirect to category page after signup
    return redirect(url_for("category_page"))

@app.route("/category")
def category_page():
    return render_template("askpage/ask.html")

@app.route("/like", methods=["POST"])
def like():
    book_id = request.form["book"]
    rec = get_recommendations(book_id)

    return render_template("homepage/home.html", rec=rec)

@app.route("/recommend", methods=["POST"])
def recommend():
    category = request.form["category"]
    rec = get_recommendations_by_category(category)
    return render_template("homepage/home.html", rec=rec)


if __name__ == "__main__":
    app.run(debug=True)