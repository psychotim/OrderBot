[Detailed feature showcase](https://www.youtube.com/watch?v=q6_tcOqOviQ)
-------------
DIRECTORY STRUCTURE
-------------------
```

src/
    db/
      migrations/    alembic migrations
      models/        db models
      queries/       db queries

    keyboards/
      admin_kb/          admin panel buuttons
      client_kb/         client panel buttons
      basic.py           admin&client stuff
    routers/
      admin_logic/       routers for admin
      client_logic/      routers for client
            commands/    start/help commands
            fsm/         states
      basic.py           admin&client stuff

    __main__.py       entry point
     
```

## ENV_FILE
First of all rename your `.env.dist` to `.env`
```

DB_HOST=yourdbhost  # optional
DB_PORT=yourdbport # optional
DB_USER=yoourdbuser # optional
DB_NAME=mysuperdb
DB_PASS=yourdbpassword # optional

TOKEN=bottoken
SUDO_ID=personalid
NOTICE_ID=personalid # optional

```

## What's new in Master-bot version2(Orderbot) ? 
1. some features have been improved or removed(if they weren't needed)
2. Migrated from sqlite to PostgresSQL using SQLAlchemy
3. Added Alembic
4. Upgrade structure
5. New feature: deleting a date from the database after registration
6. added Docker-compose

## Download
```
git clone https://github.com/psychotim/OrderBot.git
```
## Installation
```
pip install -r requirements.txt
make migrate
python -m src
```
## Docker
```
docker compose up -d
```
