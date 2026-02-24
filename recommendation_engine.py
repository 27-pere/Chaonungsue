class RecommendationEngine:
    def __init__(self, dataFrame):
        self.books = dataFrame
    def recommend_by_category(self, category, top_n=16):
        filtered = self.books[
            self.books["category"].str.contains(category, case=False, na=False)
        ]

        if filtered.empty:
            return[]
        return filtered.head(top_n).to_dict(orient="records")
    def recommend_high_rated(self, min_rating=8):
        high_rated = self.books[self.books["rating"] >= min_rating]
        return high_rated.to_dict(orient="record")