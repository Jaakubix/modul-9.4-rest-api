import json

class Books:
    def __init__(self):
        try:
            with open("books.json", "r") as f:
                self.books = json.load(f)
        except FileExistsError:
            self.books = []

    def all(self):
        return self.books
    
    def get(self, id):
        return self.books[id-1]

    def create(self, data):
        self.books.append(data)
        self.save_all()

    def save_all(self):
        with open('books.json', "w") as f:
            json.dump(self.books, f)

    def update(self, id, data):
        book = self.get(id)
        if book:
            index = self.books.index(book)
            self.books[index] = data
            return True
        return False
    def delete(self, id):
        book = self.get(id)
        if book:
            self.books.remove(book)
            self.save_all()
            return True
        return False

books = Books()