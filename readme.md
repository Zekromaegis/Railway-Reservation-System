# Setup Instructions
The Setup instructions assumes that,
- the name of database is "railway_miniproject".
- django's username and password is "django_railways" and "railways".
- To change the above assumptions, you will need to change the database/username/password in "Database\setup.sql" and "RailReserve\db_config.cnf".

1. Open command prompt on project's root.
2. Setup a Python Virtual Enviroment ( https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments ) and activate it. (Optional but Recommended)
3. Install all the requirements by running command "python -m pip install -r requirements.txt"
4. Run "Database\setup.sql" on your MySQL Workbench / Command Prompt.
5. cd to RailReserve folder. "cd RailReserve".
6. Run "python manage.py makemigrations".
7. Run "python manage.py migrate".
8. Run "Database\setup2.sql" on your MySQL Workbench / Command Prompt.
9. Import "Database\tables\\*" to their respective Tables in your database. ( https://www.mysqltutorial.org/import-csv-file-mysql-table/ ).
10. Run "python manage.py createsuperuser".
11. Run "python manage.py runserver".
12. The Django server should start on localhost. Open the localhost in a Web Browser. The site is located on {server}/railways/