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
