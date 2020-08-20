# fastapi-test-project
# how to run
7. Open terminal 1 and cd to root
8. in terminal 1 run `docker-compose up`
1. Open terminal 2 and cd to root
2. in terminal 2 run `pip install virtualenv`
3. in terminal 2 run `virtualenv venv`
4. in terminal 2 run `source venv/bin/activate`
5. in terminal 2 run `pip install -r requirements.txt`
6. in terminal 2 run `alembic upgrade head`
7. in terminal 2 run `uvicorn api.main:app`
9. Open terminal 3 and cd to root
4. in terminal 3 run `source venv/bin/activate`
9. in terminal 3 run `python bot/bot.py`
