# My CapStone

This app was built with all the knowlege i gained through Bottage.
I made this social media app for my capstone for Bottage Course for anyone that would likes to do vlogs, blogs.
This was really challenging for me but was really fun to build. At this moment this app only allows you to make a user create, edit, and delete blogs. visit other users profiles.

# Link to my frontend git repo

[React](https://github.com/DanGoss4394/my_capstone_frontend)

# Packages I Used An The Doc links

- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
- [Flask Marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/)
- [Marshmallow-sqlalchemy](https://marshmallow-sqlalchemy.readthedocs.io/en/latest/)
- [Jinja](https://jinja.palletsprojects.com/en/2.11.x/)
- [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/en/latest/)

## Venv:

**Create Virtual Environment:**

> Wherever you run this command it will create a `venv` folder. If you want the folder to be called something different change the second `venv`.

```
# Mac
$ python3 -m venv venv
# PC
$ python -m venv venv
```

**Activate The Virtual Environment:**

```
# Mac
$ source venv/bin/activate
(venv) $ _
# Windows
$ venv\Scripts\activate
(venv) $ _
```

**Installing Packages:**

```
(venv) $ pip install package-name
```

**Requirements File**
If you ever need to regenerate your environment on another machine, you are going to have trouble remembering what packages you had to install, so the generally accepted practice is to write a `requirements.txt` file in the root folder of your project listing all the dependencies, along with their versions. Producing this list is actually easy:

```
(venv) $ pip freeze > requirements.txt
```

The `pip freeze` command will dump all the packages that are installed on your virtual environment in the correct format for the `requirements.txt` file. Now, if you need to create the same virtual environment on another machine, instead of installing packages one by one, you can run:

```
(venv) $ pip install -r requirements.txt
```

# Database creation

To get a database started up use the following code.

First you need to enter a python repil. Enter `python` into the console to start a repil.

After that enter the following command to create the database.

```
>>>from YOUR_APP import db
>>>db.create_all()
```

#
