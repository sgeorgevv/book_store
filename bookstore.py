import sqlite3 as sq

# creating the Database and the library
try:
    connection = sq.connect("ebookstore.db")

    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE books(
                    ID integer primary key,
                    Title text,
                    Author text,
                    Qty integer
                                )""")
except sq.OperationalError:
    pass

# adding pre-existing books
try:
    cursor.execute("""INSERT INTO books VALUES
     (3001, "A Tale of Two Cities", "Charles Dickens", 30),
     (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
     (3003, "The Lion, the Witch and the Wardrobe", "C. S. Lewis", 25),
     (3004, "The Lord of the Rings", "J.R.R Tolkien", 37),
     (3005, "Alice in Wonderland", "Lewis Carroll", 12)""")
except sq.IntegrityError:
    pass


# create a class for new books:

class Book:
    def __init__(self, ID, title, qty, author):
        self.id = ID
        self.title = title
        self.qty = qty
        self.author = author

    def add_book(self):
        cursor.execute(f"""INSERT INTO books VALUES ({self.id}, "{self.title}", "{self.author}", {self.qty})""")


# create functions to alter the database as necessary

def del_book(ID):
    cursor.execute(f"""DELETE FROM books WHERE ID = {ID} """)


def find_book(value):
    cursor.execute(f"""SELECT * FROM books WHERE ID = {int(value)} or Title = "{value}" or Author = "{value}" """)
    print(cursor.fetchall())


def update(attr, value, ID):
    cursor.execute(f"""UPDATE books SET "{attr}" = "{value}" WHERE ID = {ID} """)


book_table = []
cursor.execute(f"""SELECT * FROM books""")
book_table.append(cursor.fetchall())


# create function to view all books
def view_all():
    global book_table
    for i in range(len(book_table[0])):
        print(book_table[0][i])


on = True
while on is True:
    user_choice = input("Please select the number that corresponds to the following options:\n"
                        "1. Enter book\n"
                        "2. Update book\n"
                        "3. Delete book\n"
                        "4. Search books\n"
                        "5. View all books\n"
                        "0. Exit\n")

    if user_choice == "1":
        try:
            ID = int(input("Please input unique ID number. If you need to return to the main menu, input a letter:  "))
            for i in range(len(book_table[0])):
                while book_table[0][i][0] == ID:
                    print("ID already exists")
                    ID = int(input("Please input unique ID number: "))
        except ValueError:
            pass
        else:
            title = input("Please input title: ")
            author = input("Please input author: ")
            qty = int(input("Please input quantity: "))
            new_book = Book(ID, title, qty, author)
            new_book.add_book()
        book_table = []
        cursor.execute(f"""SELECT * FROM books""")
        book_table.append(cursor.fetchall())
        connection.commit()

    elif user_choice == "2":
        _ = True
        ID = int(input("Please input the ID of the book you want to update: "))
        while _ is True:
            attr = input("Please input which attribute you want to change:"
                         "1. Title\n"
                         "2. Author\n"
                         "3. Quantity\n")
            if attr == "3":
                attr = "Qty"
                value = int(input("Please input new value: "))
                _ = False
            elif attr == "1":
                attr = "Title"
                value = input("Please input new Title: ")
                _ = False
            elif attr == "2":
                attr = "Author"
                value = input("Please input new Author: ")
                _ = False
            else:
                "Please only input 1, 2, or 3."
        update(attr=attr, value=value, ID=ID)
        book_table = []
        cursor.execute(f"""SELECT * FROM books""")
        book_table.append(cursor.fetchall())
        connection.commit()

    elif user_choice == "3":
        ID = int(input("Please input the ID of the book you want to delete: "))
        del_book(ID)
        book_table = []
        cursor.execute(f"""SELECT * FROM books""")
        book_table.append(cursor.fetchall())
        connection.commit()

    elif user_choice == "4":
        value = input("Please type an ID, author, or title: ")
        find_book(value)
        connection.commit()

    elif user_choice == "5":
        view_all()

    elif user_choice == "0":
        connection.close()
        exit("Goodbye!")

    else:
        print("Please only input a number from the following menu:")
