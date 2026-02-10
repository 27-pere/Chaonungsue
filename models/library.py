class Library:
    def __init__(self):
        self.books = {}

    # ADD
    def add_book(self, book):
        self.books[book.book_id] = book

    # GET
    def get_book(self, book_id):
        return self.books.get(book_id)

    # DELETE
    def delete_book(self, book_id):
        if book_id in self.books:
            del self.books[book_id]

    # UPDATE
    def update_book(self, book_id, new_title):
        if book_id in self.books:
            self.books[book_id].update_title(new_title)