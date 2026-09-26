# Alzikrayat — Photo Sharing Application
#
##### Alhadi Hassan Mohamadein Hussein
##### Software Engineer

Custom MVC + 3-Tier web application. 
Flask is used only as an HTTP listener; 
regex Router, and every query is raw parameterized SQL.

## Run

```bash
pip install -r requirements.txt
python run.py            # http://localhost:5000
```

Runs on SQLite out of the box (zero setup). For MySQL:

```bash
mysql -u root -p < schema.sql
# in app/config.py set DB_DRIVER = "mysql" and fill the credentials
```

## Architecture

 MVC Component:

 Views              :  `app/views/templates/`, `app/static/` (Bootstrap 5, JS validation) 
Controllers + Router: `app/core/router.py`, `app/controllers/` 
 Models + SQL        : `app/models/`, `app/core/database.py` 







| 3-Tier Layer :

| Presentation   :      `app/views/templates/`, `app/static/` (Bootstrap 5, JS validation) 
| Application    :         `app/core/router.py`, `app/controllers/` 
| Data         :          `app/models/`, `app/core/database.py` 

## Routes (`app/routes.py`)

| Method | Path | Action |
|---|---|---|
| GET  | `/` | Landing page + statistics |
| GET  | `/about` | About Us |
| GET/POST | `/register` | Registration |
| GET/POST | `/login` | Login (+ last-login cookie) |
| GET  | `/logout` | Destroy session |
| GET  | `/photos?style=grid3\|grid4\|list` | Gallery with display styles |
| GET  | `/photo/new` | Upload form (auth) |
| POST | `/photo/store` | Save file + metadata (auth) |
| GET  | `/photo/{id:int}` | Detail view + comments |
| POST | `/photo/{id:int}/delete` | Delete (ownership checked) |
| POST | `/photo/{id:int}/comment` | Add comment (auth) |

