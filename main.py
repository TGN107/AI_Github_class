
import json
import csv
from pathlib import Path
from datetime import datetime


# ==========================================
# 1. LIBRARY DIRECTORY SETUP
# ==========================================

BASE_DIR = Path("Library_Management_System")

BOOK_DIR = BASE_DIR / "Books"
MEMBER_DIR = BASE_DIR / "Members"
REPORT_DIR = BASE_DIR / "Reports"
BACKUP_DIR = BASE_DIR / "Backup"

for folder in [BOOK_DIR, MEMBER_DIR, REPORT_DIR, BACKUP_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

BOOK_FILE = BOOK_DIR / "books.json"
MEMBER_FILE = MEMBER_DIR / "members.json"
ISSUE_FILE = BOOK_DIR / "issued_books.json"


# ==========================================
# 2. ABSTRACT PERSON CLASS
# ==========================================

class Person:

    def __init__(self, person_id, name, email):
        self.person_id = person_id
        self.name = name
        self.email = email

    def display_details(self):
        raise NotImplementedError


# ==========================================
# 3. MEMBER CLASS
# ==========================================

class Member(Person):

    def __init__(self, person_id, name, email):
        super().__init__(person_id, name, email)

    def display_details(self):
        print("-" * 40)
        print("Member ID:", self.person_id)
        print("Name:", self.name)
        print("Email:", self.email)
        print("-" * 40)

    def to_dict(self):
        return {
            "id": self.person_id,
            "name": self.name,
            "email": self.email
        }


# ==========================================
# 4. BOOK CLASS
# ==========================================

class Book:

    def __init__(self, book_id, title, author, category, quantity):

        self.book_id = book_id
        self.title = title
        self.author = author
        self.category = category
        self.quantity = quantity
        self.available = quantity

    def display_book(self):

        print("-" * 45)
        print("Book ID:", self.book_id)
        print("Title:", self.title)
        print("Author:", self.author)
        print("Category:", self.category)
        print("Total Copies:", self.quantity)
        print("Available Copies:", self.available)
        print("-" * 45)

    def to_dict(self):

        return {
            "id": self.book_id,
            "title": self.title,
            "author": self.author,
            "category": self.category,
            "quantity": self.quantity,
            "available": self.available
        }


# ==========================================
# 5. LIBRARY CLASS
# ==========================================

class Library:

    def __init__(self):

        self.books = {}
        self.members = {}
        self.issued_books = {}

        self.load_data()

    # ======================================
    # LOAD DATA FROM JSON
    # ======================================

    def load_json(self, file_path):

        if file_path.exists():

            try:
                with file_path.open("r", encoding="utf-8") as file:
                    return json.load(file)

            except (json.JSONDecodeError, OSError):
                print("Could not read:", file_path)
                return {}

        return {}

    def load_data(self):

        books_data = self.load_json(BOOK_FILE)
        members_data = self.load_json(MEMBER_FILE)
        issued_data = self.load_json(ISSUE_FILE)

        for book_id, data in books_data.items():

            self.books[book_id] = Book(
                data["id"],
                data["title"],
                data["author"],
                data["category"],
                data["quantity"]
            )

            self.books[book_id].available = data["available"]

        for member_id, data in members_data.items():

            self.members[member_id] = Member(
                data["id"],
                data["name"],
                data["email"]
            )

        self.issued_books = issued_data

    # ======================================
    # SAVE DATA TO JSON
    # ======================================

    def save_data(self):

        books_data = {
            book_id: book.to_dict()
            for book_id, book in self.books.items()
        }

        members_data = {
            member_id: member.to_dict()
            for member_id, member in self.members.items()
        }

        with BOOK_FILE.open("w", encoding="utf-8") as file:
            json.dump(books_data, file, indent=4)

        with MEMBER_FILE.open("w", encoding="utf-8") as file:
            json.dump(members_data, file, indent=4)

        with ISSUE_FILE.open("w", encoding="utf-8") as file:
            json.dump(self.issued_books, file, indent=4)

    # ======================================
    # ADD BOOK
    # ======================================

    def add_book(self):

        print("\nADD NEW BOOK")

        book_id = input("Enter Book ID: ").strip()

        if not book_id:
            print("Book ID cannot be empty!")
            return

        if book_id in self.books:
            print("Book already exists!")
            return

        title = input("Enter Book Title: ").strip()
        author = input("Enter Author: ").strip()
        category = input("Enter Category: ").strip()

        try:
            quantity = int(input("Enter Quantity: "))

            if quantity <= 0:
                print("Quantity must be positive!")
                return

        except ValueError:
            print("Please enter a valid number!")
            return

        if not all([title, author, category]):
            print("Book details cannot be empty!")
            return

        book = Book(
            book_id,
            title,
            author,
            category,
            quantity
        )

        self.books[book_id] = book

        self.save_data()

        print("Book added successfully!")

    # ======================================
    # REGISTER MEMBER
    # ======================================

    def add_member(self):

        print("\nREGISTER NEW MEMBER")

        member_id = input("Enter Member ID: ").strip()

        if not member_id:
            print("Member ID cannot be empty!")
            return

        if member_id in self.members:
            print("Member already registered!")
            return

        name = input("Enter Name: ").strip()
        email = input("Enter Email: ").strip()

        if not name or not email:
            print("Name and email are required!")
            return

        member = Member(
            member_id,
            name,
            email
        )

        self.members[member_id] = member

        self.save_data()

        print("Member registered successfully!")

    # ======================================
    # DISPLAY ALL BOOKS
    # ======================================

    def display_books(self):

        print("\nALL LIBRARY BOOKS")

        if not self.books:
            print("No books available!")
            return

        for book in self.books.values():
            book.display_book()

    # ======================================
    # DISPLAY ALL MEMBERS
    # ======================================

    def display_members(self):

        print("\nALL REGISTERED MEMBERS")

        if not self.members:
            print("No members registered!")
            return

        for member in self.members.values():
            member.display_details()

    # ======================================
    # SEARCH BOOK
    # ======================================

    def search_book(self):

        search = input(
            "Enter book title or author: "
        ).strip().lower()

        found = False

        for book in self.books.values():

            if (
                search in book.title.lower()
                or search in book.author.lower()
            ):

                book.display_book()
                found = True

        if not found:
            print("No matching book found!")

    # ======================================
    # ISSUE BOOK
    # ======================================

    def issue_book(self):

        print("\nISSUE BOOK")

        book_id = input("Enter Book ID: ").strip()
        member_id = input("Enter Member ID: ").strip()

        if book_id not in self.books:
            print("Book does not exist!")
            return

        if member_id not in self.members:
            print("Member does not exist!")
            return

        book = self.books[book_id]

        if book.available <= 0:
            print("No copies available!")
            return

        if book_id in self.issued_books:
            if member_id in self.issued_books[book_id]:
                print("This member already has this book!")
                return

        book.available -= 1

        if book_id not in self.issued_books:
            self.issued_books[book_id] = {}

        self.issued_books[book_id][member_id] = {
            "issue_date": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        self.save_data()

        print("Book issued successfully!")
        print("Book:", book.title)
        print("Member:", self.members[member_id].name)

    # ======================================
    # RETURN BOOK
    # ======================================

    def return_book(self):

        print("\nRETURN BOOK")

        book_id = input("Enter Book ID: ").strip()
        member_id = input("Enter Member ID: ").strip()

        if book_id not in self.books:
            print("Book not found!")
            return

        if member_id not in self.issued_books:
            print("This member has no issued books!")
            return

        if book_id not in self.issued_books:
            print("This book is not currently issued!")
            return

        if member_id not in self.issued_books[book_id]:
            print("This book was not issued to this member!")
            return

        del self.issued_books[book_id][member_id]

        if not self.issued_books[book_id]:
            del self.issued_books[book_id]

        self.books[book_id].available += 1

        self.save_data()

        print("Book returned successfully!")

    # ======================================
    # DELETE BOOK
    # ======================================

    def delete_book(self):

        book_id = input("Enter Book ID to delete: ").strip()

        if book_id not in self.books:
            print("Book not found!")
            return

        if book_id in self.issued_books:
            print("Cannot delete a book that is currently issued!")
            return

        del self.books[book_id]

        self.save_data()

        print("Book deleted successfully!")

    # ======================================
    # DISPLAY ISSUED BOOKS
    # ======================================

    def display_issued_books(self):

        print("\nISSUED BOOKS")

        if not self.issued_books:
            print("No books currently issued!")
            return

        for book_id, member_records in self.issued_books.items():

            book = self.books[book_id]

            for member_id, details in member_records.items():

                print("-" * 40)
                print("Book:", book.title)
                print("Book ID:", book_id)
                print("Member:", self.members[member_id].name)
                print("Member ID:", member_id)
                print("Issue Date:", details["issue_date"])

    # ======================================
    # LIBRARY STATISTICS
    # ======================================

    def statistics(self):

        total_books = sum(
            book.quantity
            for book in self.books.values()
        )

        available_books = sum(
            book.available
            for book in self.books.values()
        )

        borrowed_books = total_books - available_books

        print("\nLIBRARY STATISTICS")
        print("-" * 40)

        print("Different Book Titles:", len(self.books))
        print("Total Book Copies:", total_books)
        print("Available Copies:", available_books)
        print("Borrowed Copies:", borrowed_books)
        print("Registered Members:", len(self.members))

    # ======================================
    # EXPORT BOOKS TO CSV
    # ======================================

    def export_csv(self):

        csv_file = REPORT_DIR / "library_books.csv"

        with csv_file.open(
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "Book ID",
                "Title",
                "Author",
                "Category",
                "Quantity",
                "Available"
            ])

            for book in self.books.values():

                writer.writerow([
                    book.book_id,
                    book.title,
                    book.author,
                    book.category,
                    book.quantity,
                    book.available
                ])

        print("CSV report exported:", csv_file.resolve())

    # ======================================
    # BACKUP LIBRARY DATA
    # ======================================

    def backup_data(self):

        files = [
            BOOK_FILE,
            MEMBER_FILE,
            ISSUE_FILE
        ]

        for file_path in files:

            if file_path.exists():

                backup_path = BACKUP_DIR / file_path.name

                shutil.copy2(
                    file_path,
                    backup_path
                )

        print("Library backup completed!")

    # ======================================
    # DISPLAY DIRECTORY CONTENTS
    # ======================================

    def show_files(self):

        print("\nLIBRARY PROJECT FILES")

        for path in BASE_DIR.rglob("*"):

            if path.is_file():

                print(
                    "FILE:",
                    path.name,
                    "| SIZE:",
                    path.stat().st_size,
                    "bytes"
                )

            elif path.is_dir():

                print("FOLDER:", path.name)


# ==========================================
# 6. MAIN MENU
# ==========================================

def main():

    library = Library()

    while True:

        print("\n")
        print("=" * 45)
        print("       LIBRARY MANAGEMENT SYSTEM")
        print("=" * 45)

        print("1.  Add Book")
        print("2.  Register Member")
        print("3.  Display All Books")
        print("4.  Display All Members")
        print("5.  Search Book")
        print("6.  Issue Book")
        print("7.  Return Book")
        print("8.  Delete Book")
        print("9.  Display Issued Books")
        print("10. Library Statistics")
        print("11. Export Books to CSV")
        print("12. Backup Library")
        print("13. Show All Files and Folders")
        print("14. Exit")

        print("=" * 45)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            library.add_book()

        elif choice == "2":
            library.add_member()

        elif choice == "3":
            library.display_books()

        elif choice == "4":
            library.display_members()

        elif choice == "5":
            library.search_book()

        elif choice == "6":
            library.issue_book()

        elif choice == "7":
            library.return_book()

        elif choice == "8":
            library.delete_book()

        elif choice == "9":
            library.display_issued_books()

        elif choice == "10":
            library.statistics()

        elif choice == "11":
            library.export_csv()

        elif choice == "12":
            library.backup_data()

        elif choice == "13":
            library.show_files()

        elif choice == "14":

            library.save_data()

            print("Thank you for using Library Management System!")
            break

        else:
            print("Invalid choice! Please try again.")


# ==========================================
# 7. RUN PROGRAM
# ==========================================

if __name__ == "__main__":
    main()
