# Task 10: Library Management System
# Approach: Book class, Member base class with multilevel inheritance for tiers
# (Basic -> Premium -> VIP), method overriding for fine logic, dunder methods
# for display and comparison, abc for abstract methods.

from abc import ABC, abstractmethod
from datetime import datetime, timedelta

# ---- Book Class ----
class Book:
    def __init__(self, title, author, book_id):
        self.title = title
        self.author = author
        self.book_id = book_id
        self.is_available = True

    def __str__(self):
        status = "Available" if self.is_available else "Borrowed"
        return f"[{self.book_id}] '{self.title}' by {self.author} ({status})"

    def __repr__(self):
        return f"Book(id={self.book_id}, title='{self.title}')"

    def __eq__(self, other):
        return isinstance(other, Book) and self.book_id == other.book_id


# ---- Base Member Class (Abstract) ----
class Member(ABC):
    total_members = 0

    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []   # list of (book, borrow_date)
        Member.total_members += 1

    @property
    @abstractmethod
    def max_books(self):
        pass

    @abstractmethod
    def calculate_fine(self, days_overdue):
        pass

    def borrow_book(self, book):
        if not book.is_available:
            print(f"  [!] '{book.title}' is not available.")
            return False

        if len(self.borrowed_books) >= self.max_books:
            print(f"  [!] {self.name} has reached borrow limit ({self.max_books} books).")
            return False

        book.is_available = False
        borrow_date = datetime.now()
        self.borrowed_books.append((book, borrow_date))
        print(f"  [OK] {self.name} borrowed '{book.title}'")
        return True

    def return_book(self, book, days_held=None):
        # find the book in borrowed list
        entry = None
        for b, bdate in self.borrowed_books:
            if b == book:
                entry = (b, bdate)
                break

        if not entry:
            print(f"  [!] {self.name} did not borrow '{book.title}'")
            return

        borrowed_book, bdate = entry
        if days_held is None:
            days_held = (datetime.now() - bdate).days

        due_date_days = 14  # 2 weeks allowed
        days_overdue = max(0, days_held - due_date_days)

        fine = self.calculate_fine(days_overdue) if days_overdue > 0 else 0

        borrowed_book.is_available = True
        self.borrowed_books.remove(entry)

        if fine > 0:
            print(f"  [RETURN] '{borrowed_book.title}' returned by {self.name} | Overdue: {days_overdue} days | Fine: Rs. {fine}")
        else:
            print(f"  [RETURN] '{borrowed_book.title}' returned by {self.name} | On time, no fine.")

    def __str__(self):
        return f"{self.__class__.__name__}[{self.member_id}] - {self.name} | Books: {len(self.borrowed_books)}/{self.max_books}"

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', id='{self.member_id}')"

    def __len__(self):
        return len(self.borrowed_books)

    def __lt__(self, other):
        return len(self.borrowed_books) < len(other.borrowed_books)


# ---- Basic Member (single inheritance from Member) ----
class BasicMember(Member):
    @property
    def max_books(self):
        return 2

    def calculate_fine(self, days_overdue):
        return days_overdue * 20  # Rs. 20 per day


# ---- Premium Member (multilevel: Member -> BasicMember -> PremiumMember) ----
class PremiumMember(BasicMember):
    @property
    def max_books(self):
        return 5

    def calculate_fine(self, days_overdue):
        # 50% discount on fines
        base_fine = super().calculate_fine(days_overdue)
        return base_fine * 0.5


# ---- VIP Member (multilevel: Member -> BasicMember -> PremiumMember -> VIPMember) ----
class VIPMember(PremiumMember):
    @property
    def max_books(self):
        return 10

    def calculate_fine(self, days_overdue):
        # VIP gets grace period of 3 days
        adjusted = max(0, days_overdue - 3)
        return adjusted * 5 if adjusted > 0 else 0


# ---- Library Class ----
class Library:
    def __init__(self, name):
        self.name = name
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def __getitem__(self, index):
        return self.books[index]

    def __len__(self):
        return len(self.books)

    def __iter__(self):
        return iter(self.books)

    def show_all_books(self):
        print(f"\n  Library: {self.name} | Total Books: {len(self)}")
        for book in self:
            print(f"    {book}")


# ---- Demo ----
print("=" * 58)
print("        LIBRARY MANAGEMENT SYSTEM")
print("=" * 58)

# create library and books
lib = Library("City Central Library")
books = [
    Book("Clean Code", "Robert Martin", "B001"),
    Book("Python Crash Course", "Eric Matthes", "B002"),
    Book("The Pragmatic Programmer", "Hunt & Thomas", "B003"),
    Book("Design Patterns", "Gang of Four", "B004"),
    Book("Fluent Python", "Luciano Ramalho", "B005"),
]
for b in books:
    lib.add_book(b)

lib.show_all_books()

# create members
ali   = BasicMember("Ali Hassan", "M001")
sara  = PremiumMember("Sara Khan", "M002")
bilal = VIPMember("Bilal Ahmed", "M003")

print(f"\n{'='*40}")
print("Members:")
print(f"  {ali}")
print(f"  {sara}")
print(f"  {bilal}")

# borrowing
print(f"\n{'='*40}")
print("Borrowing books:")
ali.borrow_book(books[0])
ali.borrow_book(books[1])
ali.borrow_book(books[2])   # should fail (limit=2)

sara.borrow_book(books[2])
sara.borrow_book(books[3])
sara.borrow_book(books[4])

bilal.borrow_book(books[0])   # already borrowed by ali

# returning with overdue
print(f"\n{'='*40}")
print("Returning books:")
ali.return_book(books[0], days_held=10)    # on time
ali.return_book(books[1], days_held=20)    # 6 days overdue -> Rs. 120 fine

sara.return_book(books[2], days_held=25)   # 11 days overdue -> Rs. 110 (50% discount)
bilal.borrow_book(books[0])               # now available
bilal.return_book(books[0], days_held=20)  # 6 days overdue, but VIP grace = Rs. 15

# dunder demos
print(f"\n{'='*40}")
print("Dunder method demos:")
print(f"  len(ali) = {len(ali)} books borrowed")
print(f"  len(sara) = {len(sara)} books borrowed")
print(f"  ali < sara (fewer books): {ali < sara}")
print(f"  Book lookup: lib[0] -> {lib[0]}")

print(f"\nTotal members registered: {Member.total_members}")
