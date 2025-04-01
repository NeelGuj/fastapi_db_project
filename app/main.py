from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

'''
# we can also write from .routers import post, user
# we can also write from .database import engine, get_db
1. Relative Import: Since main.py and the routers directory are in the same package (app), you use a relative import to import post and user from the routers module:
from .routers import post, user
2. Absolute Import: If you wanted to use an absolute import, you would need to specify the full path from the top-level package:
from app.routers import post, user
'''

# models.Base.metadata.create_all(bind=engine)  # Uncomment it when you use only sqlalchemy and not alembic
# The create_all() method creates the tables in the database based on the models you've defined.
# The bind parameter is the database engine to use to connect to the database.


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")     # This is the root route and it will execute when we write {{URL}} in the postman.
def root():
    return {"message": "Hello World"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

