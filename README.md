# fast-api-author-books
Use my requirements.txt placed in root directory
My Python version is 3.7.9


To run this project open a terminal window in Books-Author-System folder and run command
uvicorn main:auth_book_app --reload

To run tests all you need to do is open a terminal window in Books-Author-System folder and run command.
pytest
FakeDb is setup for test sessions using pytest

# Side Notes
The code could be more optimized by creating a CRUD parent class and creating child classes for author and books.
Test can be improved by adding a method that doesnot commit any chang in case of test db.

You can interact with APIs at http://127.0.0.1:8000/docs