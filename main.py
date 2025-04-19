import uvicorn as uvicorn
from fastapi import FastAPI
from app.functionlogic import get_router
from proj2.handlers import user_router
from registr.auth import login_router
from registr.logic_user import create_reg_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Best project in the world!!")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.1.72:1500"]
)


app.include_router(create_reg_router)
app.include_router(user_router)
app.include_router(get_router)
app.include_router(login_router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True, host="0.0.0.0", port=8000)