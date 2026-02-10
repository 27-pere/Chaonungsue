class Rental:
    def __init__(self, library, user):
        self.library = library
        self.user = user
        self.rented_books = {}

    def can_rent(self):
        return len(self.rented_books) < self.user.membership.rent_limit()

    def rent(self, book_id):
        if not self.can_rent():
            return False

        book = self.library.get_book(book_id)

        if book and book.rent():
            self.rented_books[book_id] = book
            return True
        return False

    def return_book(self, book_id):
        book = self.rented_books.pop(book_id, None)
        if book:
            book.return_book()
            return True
        return False