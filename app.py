from flask import Flask, render_template, request

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
# from ml.recommender import get_recommendations

books = pd.read_csv("books.csv")

category_matrix = pd.get_dummies(books['category'].str.split("|").apply(pd.Series).stack())

similarity = cosine_similarity(category_matrix)

def get_recommendations(category, top_n=2):
    print(books["category"] == category)
    idx = books[books["category"] == category].index[0]
    similarity_scores = list(enumerate(similarity[idx]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    books_indices = [i[0] for i in similarity_scores[1:top_n+1]]
    return books["title"].iloc[books_indices].tolist()

def get_recommendations_by_category(category, top_n=5):
    filtered_books = books[books["category"].str.contains(category, case=False, na=False)]

    if filtered_books.empty:
        return ["No books found in this category."]

    return filtered_books["title"].head(top_n).tolist()


app = Flask(__name__)

@app.route("/")
def home():
    books = ["book1", "book2", "book3"]
    return render_template("askpage/ask.html", books=books)

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