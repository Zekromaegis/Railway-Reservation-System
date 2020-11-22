# Railway Reservation System

Railway Reservation System is a Django - MySQL based system with a Website frontend to facilitate automatic, validated and error free purchase, reservation and transaction of train tickets. It also allows users to search for and view details about Trains and their Routes.

## Setup Instructions

### Assumptions
The Setup instructions assumes that,
- the name of database is "railway_miniproject".
- django's username and password is "django_railways" and "railways".
- To change the above assumptions, you will need to change the database/username/password in "Database\setup.sql" and "RailReserve\db_config.cnf".

### Steps
1. Open command prompt on project's root.
2. Setup a Python Virtual Enviroment ( https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments ) and activate it. (Optional but Recommended)
3. Install all the requirements by running command "python -m pip install -r requirements.txt"
4. Run "Database\setup.sql" on your MySQL Workbench / Command Prompt.
5. cd to RailReserve folder. "cd RailReserve".
6. Run "python manage.py makemigrations".
7. Run "python manage.py migrate".
8. Run "Database\setup2.sql" on your MySQL Workbench / Command Prompt.
9. Import "Database\tables\\*" to their respective Tables in your database. ( https://www.mysqltutorial.org/import-csv-file-mysql-table/ ).
10. Do One of the Following,
    - Run "Database\setup3.sql" to create example Train Status' for today and next 10 days. (Better as an example. Allows you to book tickets for today and next 10 days only. To book more tickets, setup an event as per "Database\setup4.sql" or manually call t_status_creator in your MySQL Workbench / Command Prompt.)
    - Run "Database\setup4.sql" to create example Train Status' for today and an event to add new status daily.
11. Run "python manage.py createsuperuser".
12. Run "python manage.py runserver".
13. The Django server should start on localhost. Open the localhost in a Web Browser. The site is located on {server address}/railways/