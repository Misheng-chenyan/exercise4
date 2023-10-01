import sqlite3

# 连接到数据库
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

def create_tables():
    # 创建Books表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Books (
            BookID TEXT PRIMARY KEY,
            Title TEXT,
            Author TEXT,
            ISBN TEXT,
            Status TEXT
        )
    ''')
    # 创建Users表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            UserID TEXT PRIMARY KEY,
            Name TEXT,
            Email TEXT
        )
    ''')
    # 创建Reservations表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Reservations (
            ReservationID TEXT PRIMARY KEY,
            BookID TEXT,
            UserID TEXT,
            ReservationDate TEXT
        )
    ''')
    conn.commit()

def add_book():
    BookID = input("Enter BookID: ")
    Title = input("Enter Title: ")
    Author = input("Enter Author: ")
    ISBN = input("Enter ISBN: ")
    Status = input("Enter Status: ")

    cursor.execute("INSERT INTO Books (BookID, Title, Author, ISBN, Status) VALUES (?, ?, ?, ?, ?)",
                   (BookID, Title, Author, ISBN, Status))
    conn.commit()
    print("Book added successfully!")

def find_book_detail(search_term):
    cursor.execute("SELECT * FROM Books WHERE BookID=? OR Title=?", (search_term, search_term))
    book = cursor.fetchone()

    if book:
        print("BookID:", book[0])
        print("Title:", book[1])
        print("Author:", book[2])
        print("ISBN:", book[3])
        print("Status:", book[4])

        cursor.execute("SELECT * FROM Reservations WHERE BookID=?", (book[0],))
        reservations = cursor.fetchall()

        if reservations:
            print("Reservations:")
            for reservation in reservations:
                print("ReservationID:", reservation[0])
                print("UserID:", reservation[2])
                print("ReservationDate:", reservation[3])
        else:
            print("No reservations for this book.")
    else:
        print("Book not found.")

def find_reservation_status(search_term):
    if search_term.startswith("LB"):  # BookID
        cursor.execute("SELECT * FROM Books WHERE BookID=?", (search_term,))
        book = cursor.fetchone()
        if book:
            print("BookID:", book[0])
            print("Title:", book[1])
            print("Status:", book[4])

            cursor.execute("SELECT * FROM Reservations WHERE BookID=?", (book[0],))
            reservations = cursor.fetchall()

            if reservations:
                print("Reservations:")
                for reservation in reservations:
                    print("ReservationID:", reservation[0])
                    print("UserID:", reservation[2])
                    print("ReservationDate:", reservation[3])
            else:
                print("No reservations for this book.")
        else:
            print("Book not found.")
    elif search_term.startswith("LU"):  # UserID
        cursor.execute("SELECT * FROM Reservations WHERE UserID=?", (search_term,))
        reservations = cursor.fetchall()
        if reservations:
            print("Reservations for User", search_term)
            for reservation in reservations:
                cursor.execute("SELECT * FROM Books WHERE BookID=?", (reservation[1],))
                book = cursor.fetchone()
                print("ReservationID:", reservation[0])
                print("BookID:", reservation[1])
                print("Book Title:", book[1])
                print("Status:", book[4])
                print("ReservationDate:", reservation[3])
        else:
            print("No reservations found for User", search_term)
    elif search_term.startswith("LR"):  # ReservationID
        cursor.execute("SELECT * FROM Reservations WHERE ReservationID=?", (search_term,))
        reservation = cursor.fetchone()
        if reservation:
            cursor.execute("SELECT * FROM Books WHERE BookID=?", (reservation[1],))
            book = cursor.fetchone()
            print("ReservationID:", reservation[0])
            print("BookID:", reservation[1])
            print("Book Title:", book[1])
            print("UserID:", reservation[2])
            print("ReservationDate:", reservation[3])
        else:
            print("Reservation not found.")
    else:  # Title
        cursor.execute("SELECT * FROM Books WHERE Title=?", (search_term,))
        book = cursor.fetchone()
        if book:
            print("BookID:", book[0])
            print("Title:", book[1])
            print("Author:", book[2])
            print("ISBN:", book[3])
            print("Status:", book[4])
        else:
            print("Book not found.")

def find_all_books():
    cursor.execute("SELECT * FROM Books")
    books = cursor.fetchall()
    for book in books:
        print("BookID:", book[0])
        print("Title:", book[1])
        print("Author:", book[2])
        print("ISBN:", book[3])
        print("Status:", book[4])

        cursor.execute("SELECT * FROM Reservations WHERE BookID=?", (book[0],))
        reservations = cursor.fetchall()

        if reservations:
            print("Reservations:")
            for reservation in reservations:
                print("ReservationID:", reservation[0])
                print("UserID:", reservation[2])
                print("ReservationDate:", reservation[3])
        else:
            print("No reservations for this book.")

def update_book_details(BookID, new_title, new_author, new_isbn):
    cursor.execute("UPDATE Books SET Title=?, Author=?, ISBN=? WHERE BookID=?", (new_title, new_author, new_isbn, BookID))
    conn.commit()
    print("Book details updated successfully!")

def delete_book(BookID):
    cursor.execute("DELETE FROM Books WHERE BookID=?", (BookID,))
    cursor.execute("DELETE FROM Reservations WHERE BookID=?", (BookID,))
    conn.commit()
    print("Book deleted successfully!")

# 创建表格
create_tables()

while True:
    print("\nLibrary Management System Menu:")
    print("1. Add a new book")
    print("2. Find a book by BookID, Title, UserID, or ReservationID")
    print("3. Find all books")
    print("4. Update book details")
    print("5. Delete a book")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_book()
    elif choice == "2":
        search_term = input("Enter BookID, Title, UserID, or ReservationID: ")
        find_reservation_status(search_term)
    elif choice == "3":
        find_all_books()
    elif choice == "4":
        BookID = input("Enter BookID: ")
        new_title = input("Enter new Title: ")
        new_author = input("Enter new Author: ")
        new_isbn = input("Enter new ISBN: ")
        update_book_details(BookID, new_title, new_author, new_isbn)
    elif choice == "5":
        BookID = input("Enter BookID: ")
        delete_book(BookID)
    elif choice == "6":
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")

# 关闭数据库连接
conn.close()
