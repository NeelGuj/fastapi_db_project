from passlib.context import CryptContext

# the version of passlib is latest but bcrypt is 4.0.1 because of some warning at terminal.

pwd_context= CryptContext(schemes=["bcrypt"], deprecated="auto")  # for password hasing

# function to hash the password during creating user
def hash(password: str):
    return pwd_context.hash(password)

# function to verify the password during user login
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
