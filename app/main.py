from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from .routes import auth, books
from .dependency  import get_current_user

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Injecting get_current_user for /auth/me
auth.router.routes[2].dependant.dependencies[0].dependency = get_current_user

app.include_router(auth.router)
app.include_router(books.router)
