class Book:
    def __init__(self, book_id, title):
        self.book_id = book_id
        self.title = title
        self.available = True
    
    def borrow(self):
        if self.available:
            self.available = False
            return "Success"
        return "Book unavailable"

    def return_book(self):
        self.available = True 
