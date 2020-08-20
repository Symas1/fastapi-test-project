from fastapi import FastAPI

import api.endpoints

app = FastAPI()
app.include_router(api.endpoints.ROUTER)

if __name__ == "__main__":
    # TODO: DELETE
    import uvicorn

    uvicorn.run('api.main:app', host="0.0.0.0", port=8000, reload=True)
