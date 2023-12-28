# 1. DRF-train-project
This project was created for educational purposes to demonstrate the skills acquired during training
# Features:
JWT authenticated

Admin panel /admin/

Documentation at api/doc/swagger or api/doc/redoc

Managing orders and tickets

CRUD for all models in project

Custom endpoint to upload images for train

Filtering Journeys by start_date, end_date, source and destination (you can read more in doc)

Tickets available feature on jorneys list

# 2. Setup django project on different platforms
Starting a Django project from a GitHub repository on different platforms involves a few general steps. Here's a step-by-step guide that you can follow for Windows, macOS, and Linux:


Prerequisites:
Git: Make sure Git is installed on your system. You can download it from https://git-scm.com/.

Python: Install Python on your system. You can download it from https://www.python.org/downloads/.

Steps:
1. Clone the Repository:
Open your terminal or command prompt and navigate to the directory where you want to create your Django project.


```
https://github.com/okien1/Restaurant-kitchen-pet-project.git

```

2. Create a Virtual Environment (Optional but Recommended):
Navigate into the project directory and create a virtual environment. Virtual environments help isolate dependencies for different projects.

Activate the virtual environment on Windows:
```
cd repository
python -m venv venv
venv\Scripts\activate
```
On macOS/Linux:

```
source venv/bin/activate
```
3. Install Dependencies:
Install the project dependencies using pip:

```
pip install -r requirements.txt
```


4. Configure Database:
Configure your database settings in the settings.py file.

```
python manage.py makemigrations
python manage.py migrate
```
5. Run the Development Server:
```
python manage.py runserver
```
The development server should now be running. Open a web browser and go to http://127.0.0.1:8000/ to see your Django application.

Generate a new secret key for the project and update the SECRET_KEY setting in settings.py.

# 3. Run preloaded data
 run
 ```
python manage.py loaddata train_data.json
python manage.py loaddata user_data.json
```
 to load data from fixture to database.

 # 4. Run project via docker

 Docker must be installed on the computer/server before running

 Run folliwing commands:
 ```
docker-compose build
docker-compose up
```
After this, a DRF application and an application with a postgres database will be created on Docker, and pre-prepared data will be placed in the database. To test the functionality of the application, you need to follow the link http://127.0.0.1:8000/api/user/token and enter the following values: 

email admin@admin.com 

password admin
 
