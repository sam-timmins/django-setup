# Install Django

```
pip3 install django
```

## Create the project
```
django-admin startproject ___project_name___ .
```

## Run the server
```
python3 manage.py runserver
```
Click the Open Browser button. The project is created.


# URLs

Django projects are organized into small components called apps.
You can think of an app as a reusable self-contained collection of code.
That can be passed around from project to project in order to speed up development time.

Example:

To create an app called todo
```
python3 manage.py startapp todo
```

In the directory, creat a 'templates' folder in the todo app, within the 'templates' folder create a folder with the same name as the app. In this instance 'todo' then create the todo_list.py and add some html.

* todo (app name)
    * templates
        * todo
            * todo_list.html

In ```views.py``` within the app folder create a basic return of the todo_list.html

```py
from django.shortcuts import render

# Create your views here.
def get_todo_list(request):
    return render(request, 'todo/todo_list.html')
```

Within the main django folder, go to ```settings.py``` import the madule from the ```views.py```  file in the todo app.

```py
from todo.views import get_todo_list
```

and create the path
```py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', get_todo_list, name='get_todo_list')
]
```

In the terminal check to make sure its working
```
python3 manage.py runserver
```

# Migrations and Admin

* Converts python code to SQL code that can be executed on the database
```
python3 manage.py makemigrations
```

* Show built in apps
```
python3 manage.py showmigrations
```

* Sets up basic requirments
```
python3 manage.py migrate
```

* In order to log in and look at the table in the database
```
python3 manage.py createsuperuser
```

* Enter a username, password and re-enter password

* To login as the superuser, launch the project again
```
python3 manage.py runserver
```
and login using the details just created