import uvicorn as uvicorn
from fastapi import FastAPI
from app.functionlogic import create_router, get_router
from proj2.handlers import user_router


app = FastAPI(title="Best project in the world!!")

app.include_router(create_router)
app.include_router(user_router)
app.include_router(get_router)
#app.include_router(delete_router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)