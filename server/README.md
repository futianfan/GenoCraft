## ✨ How to use the code

> **Step #1** - Clone the project

```bash
$ git clone https://github.com/futianfan/GenoCraft.git
$ cd GenoCraft-main/server
```

<br />

> **Step #2** - create virtual environment using python3 and activate it (keep it outside our project directory)

```bash
$ # Virtualenv modules installation (Unix based systems)
$ virtualenv env
$ source env/bin/activate
$
$ # Virtualenv modules installation (Windows based systems)
$ # virtualenv env
$ # .\env\Scripts\activate
```

<br />

> **Step #3** - Install dependencies in virtualenv

```bash
$ pip install -r requirements.txt
```

<br />

> **Step #4** - setup `flask` command for our app

```bash
$ export FLASK_APP=run.py
$ export FLASK_ENV=development
```

For **Windows-based** systems

```powershell
$ (Windows CMD) set FLASK_APP=run.py
$ (Windows CMD) set FLASK_ENV=development
$
$ (Powershell) $env:FLASK_APP = ".\run.py"
$ (Powershell) $env:FLASK_ENV = "development"
```

<br />

> **Step #5** - Create a new `.env` file using sample `env.sample`

The meaning of each variable can be found below:

- `DEBUG`: if `True` the app runs in develoment mode
    - For production value `False` should be used
- `SECRET_KEY`: used in assets management
- `GITHUB_CLIENT_ID`: For GitHub social login
- `GITHUB_SECRET_KEY`: For GitHub social login

<br />

> **Step #6** - start test APIs server at `localhost:5000`

```bash
$ flask run
```

Use the API via `POSTMAN` or Swagger Dashboard.