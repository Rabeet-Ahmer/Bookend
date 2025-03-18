import pymongo
import inquirer
from rich.console import Console
from rich.prompt import Prompt

# MongoDB Connection
MONGO_URI = "mongodb+srv://Rabeet:9UeP7g8ILtM2wVdX@cluster0.j81k9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(MONGO_URI)
db = client["book_manager"]
collection = db["books"]

console = Console()

# Add a book
def add_book():
    title = Prompt.ask("[bold red]Enter book title: [/bold red]")
    author = Prompt.ask("[bold blue]Enter author name: [/bold blue]")
    collection.insert_one({"title": title, "author": author})
    console.print(f"[green]📚 Book '{title}' by {author} added![green]")

# List all books
def list_books():
    books = collection.find()
    if collection.count_documents({}) == 0:
        print("📖 No books found.")
        return
    for i, book in enumerate(books, start=1):
        print(f"{i}. {book['title']} by {book['author']}")

# Search for a book by title
def search_book():
    title = input("Enter book title to search: ")
    books = collection.find({"title": {"$regex": title, "$options": "i"}})
    results = list(books)
    if not results:
        print(f"🔍 No books found with title '{title}'.")
    else:
        for book in results:
            print(f"✅ Found: {book['title']} by {book['author']}")

# Remove a book by title
def remove_book():
    title = input("Enter book title to remove: ")
    result = collection.delete_one({"title": {"$regex": title, "$options": "i"}})
    if result.deleted_count == 0:
        print(f"❌ Book '{title}' not found.")
    else:
        print(f"🗑️ Book '{title}' removed!")


def main():
    print("📚 Welcome to Book Manager! 📚")
    while True:
        questions = [
            inquirer.List(
                "action",
                message="📚 Choose an action",
                choices=["Add Book", "List Books", "Search Book", "Remove Book", "Exit"],
            )
        ]
        answers = inquirer.prompt(questions)
        action = answers["action"]

        if action == "Add Book":
            add_book()
        elif action == "List Books":
            list_books()
        elif action == "Search Book":
            search_book()
        elif action == "Remove Book":
            remove_book()
        elif action == "Exit":
            print("👋 Exiting Book Manager. Goodbye!")
            break

if __name__ == "__main__":
    main()
