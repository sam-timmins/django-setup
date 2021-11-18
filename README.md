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


# Create Modules
Navigate to the ```modules.py``` file in the app, in this case todo
```py
class Item(models.Model):
    # name will be a text field that has a max length of 50 characters
    # null prevents items being created without a name
    # blank = false makes it a required field on forms
    name = models.CharField(max_length=50, null=False, blank=False)
     # done will be a boolean field with default set to not done (False)
    done = models.BooleanField(null=False, blank=False, default=False)

```

Before creating the model, check to make sure it is creating the correct model in the terminal
```
python3 manage.py makemigrations --dry-run
```
If all is ok
```
python3 manage.py makemigrations
```

Check to see if there is an unapplied migration
```
python3 manage.py showmigrations
```
Check to make sure the migration will be correct
```
python3 manage.py migrate --plan
```
If all is ok
```
python3 manage.py migrate
```

Expose the table to the admin by registering the module. Go to the app's ```admin.py``` file and import the class from the models file and register it
```py
from .models import Item

admin.site.register(Item)
```

Go back to ```models.py``` and change the way the item is displayed in the admin login
```py
class Item(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    done = models.BooleanField(null=False, blank=False, default=False)

    # This sets the item to be it's name
    def __str__(self):
        return self.name
```

# Rendering Data

Within the app, open the ```views.py``` file and import the models

```py
from django.shortcuts import render
from .models import Item


# Create your views here.
def get_todo_list(request):
    items = Item.objects.all()
    context = {
        'items' : items
    }
    return render(request, 'todo/todo_list.html', context)
```

This creates complete communication between users on the front and database on the backend, use {{ }} and {% %} in the templates html file to access the database.

```html
    <table>
        {% for item in items %}
            <tr>
                {% if item.done %}
                <!-- Create a strike through row if the item is done -->
                    <td><strike>{{ item.name }}</strike></td>
                {% else %}
                <!-- Create a row if the item is not done -->
                    <td>{{ item.name }}</td>
                {% endif %}
            </tr>
            <!-- If the data base is empty create a row explaining -->
            {% empty %}
            <tr>
                <td>You have nothing to do</td>
            </tr>
        {% endfor %}
    </table>
```

# Forms
```html
<form action="add" method="POST">
                # Always add this when posting data from Django
                {% csrf_token %}
                <div class="mb-3">
                    <label for="id_name" class="form-label">Name: </label>
                    <input type="text" class="form-control" id="id_name" name="item_name" placeholder="task name">
                </div>
                <div class="form-check form-switch">
                    <input class="form-check-input" type="checkbox" role="switch" id="id_done" name="id_done">
                    <label class="form-check-label" for="id_done">Done: </label>
                </div>
                <button type="submit" class="btn btn-outline-danger">Add Item</button>
            </form>
```

## Create form directly in the modal
* Create a file in the app called ```forms.py```

```py
from django import forms
from .models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'done']
```

* in ```views.py```
```py
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('get_todo_list')
    form = ItemForm()
    context = {
        'form' : form
    }
    
    return render(request, 'todo/add_item.html', context)
```


# Testing

Create a test file for each file needed to be tested.
* ````forms.py````
* ````test_forms.py````

In the test file
```py
from django.test import TestCase

# Create your tests here.
class TestDjango(TestCase):

    def test_it_works(self):
        self.assertEqual(1,0)
```

Run only the test_forms file in the terminal 
```
python3 manage.py test todo.test_forms
```

Run only the TestItemFor class in the test_forms file in the terminal 
```
python3 manage.py test todo.test_forms.TestItemFor
```

Run only the test_item_name_is_required test in the TestItemFor class in the test_forms file in the terminal 
```
python3 manage.py test todo.test_forms.TestItemFor.test_item_name_is_required
```

* . = Test Passed
* F = Test Failed
* E = Error (terminal gives reason why)


## Coverage of code that is tested
* Install coverage in the terminal
```
pip3 install coverage
```

* Run coverage
```
coverage run --source=app_name manage.py test
```

* Create a report
```
coverage report
```

* Create an interactive html report, this create a htmlcov folder in the root directory
```
coverage html
```
* Within the folder there is an index.html, to view this
```
python3 -m http.server
```

### After changes
* Run coverage
```
coverage html
```
```
coverage run --source=app_name manage.py test
```
```
python3 -m http.server
```

# Deployment
* Install Postgres
```
pip3 install psycopg2
```

* Install gunicorn
```
pip3 install gunicorn
```

* Create a requirements file for Heroku to know what packages to install
```
pip3 freeze --local > requirements.txt
```

* Log into heroku in the terminal
```
heroku login -i
```

* Create an app name
```
 heroku apps:create application_name --region eu
```

* Check to make sure it is there
```
heroku apps
```

## Create a database in heroku
* Navigate to the app from [heroku.com](www.heroku.com) and open the 'Resources' tab.
* Search for 'Heroku Postgres', select it and click 'submit Order'
* Check it is there by going to the 'Settings' tab and in the config vars, the  DATABASE_URL should be there.

## Connect to the database in heroku
* Install dj-database
```
pip3 install dj-database-url
```
```
pip3 freeze --local > requirements.txt
```
```
heroku config
```
Go to ```settings.py``` file and scroll down to the DATABASE section.

Import the dj_database_url
```py
import dj_database_url
```
```py
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': dj_database_url.parse('THE URL FROM THE HEROKU CONFIG STAGE')
}
```

* Migrate the models to the new database
```py
python3 manage.py migrate
```

* Push to GihHub
* Enter below
```
 heroku config:set DISABLE_COLLECTSTATIC=1
```
* Push to heroku master
```
git push heroku main
```
* The url will be shown followed by 'deployed to Heroku'

If it shows an application error, enter below to see the errr codes.
```
heroku logs --tail
```
* On initial setup we need to start gunicorn, create a Procfile in the root directory.
* With in the Procfile add the following code to tell gunicorn to run using the wsgi module
```
web: gunicorn django_todo.wsgi:applicati
```
* Commit and then push to heroku main
```
git push heroku main
```

* Add host name of the heroku app in ```settings.py```
```py
ALLOWED_HOSTS = ['URL MINUS THE HTTPS GOES HERE']
```