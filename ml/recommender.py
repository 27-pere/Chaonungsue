import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

books = pd.read_csv("books.csv")

category_matrix = pd.get_dummies(books['category'].str.split("|").apply(pd.Series).stack())

similarity = cosine_similarity(category_matrix)

def get_recommendations(title, top_n=5):
    idx = books[books["title"] == title].index[0]
    similarity_scores = list(enumerate(similarity[idx]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    books_indices = [i[0] for i in similarity_scores[1:top_n+1]]
    return books["title"].iloc[books_indices]

title = input("Enter the title of your favorite book: ")
print("Top 5 similar books: ")
print(get_recommendations(title))