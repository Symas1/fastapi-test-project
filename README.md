# fastapi-test-project
# how to run
7. Open terminal 1 and cd to root
8. in terminal 1 run `docker-compose up`
1. Open terminal 2 and cd to root
3. in terminal 2 run `virtualenv venv && source venv/bin/activate && pip install -r requirements.txt && alembic upgrade head && uvicorn api.main:app`
9. Open terminal 3 and cd to root
4. in terminal 3 run `source venv/bin/activate && python bot/bot.py`
