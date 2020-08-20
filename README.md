# fastapi-test-project
# how to run
1. Open terminal 1 and cd to root
2. in terminal 1 run `docker-compose up`
3. Open terminal 2 and cd to root
4. in terminal 2 run `virtualenv venv && source venv/bin/activate && pip install -r requirements.txt && alembic upgrade head && uvicorn api.main:app`
5. Open terminal 3 and cd to root
6. in terminal 3 run `source venv/bin/activate && python bot/bot.py`
7. go to http://localhost:8081/ and use the credentials from docker-compose.yml to login and view the database