from flask import Flask, render_template, request
from ml.recommender import get_recommendations
app = Flask[__name__]

@app.route("/")
def home():
    books = ["book1", "book2", "book3"]
    return render_template("books.html", books=books)

@app.route("/like", methods=["POST"])
def like():
    book_id = request.form["book"]
    rec = get_recommendations(book_id)

    return render_template("recommand.html", rec=rec)

if __name__ == "__main__":
    app.run(debug=True)