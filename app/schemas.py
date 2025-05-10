from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional

# The below class was Post(BaseModel) before but we have changed it to PostCreate(BaseModel) to differentiate between the Post model and the PostCreate pydantic model.
class PostCreate(BaseModel):  # It is used to validate the data that we receive in the request body. 
    title: str
    content: str
    published: bool= True  # If the published field is not provided in the create request body, then it will be set to True by default.

class PostUpdate(BaseModel):  
    title: str
    content: str
    published: bool= True

class PostPatch(BaseModel):   # to validate patch request data
    title: str = None
    content: str = None
    published: bool = None 


#  Response model for users model
# We have shifter UserOut() on top of PostResponse() because of owner=UserOut.
class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes= True   # or orm_mode= True


# This is the pydantic model for response to the user.
# It will define how and what the data at response will look like

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    owner_id: int
    owner: UserOut   # we are returning a post's owner information in form of pydantic model UserOut based on the relationship with User Class.

    class Config:
        from_attributes= True   # or orm_mode= True
        
# orm_mode=True produce some warning at terminal but program runs fine.
# 'orm_mode' has been renamed to 'from_attributes'
#   warnings.warn(message, UserWarning)
'''Setting orm_mode = True tells Pydantic to treat the SQLAlchemy model (Object) as a dictionary-like object, which makes serialization(to convert into JSON) possible
However, this is only applied to individual objects, not to lists of objects which is the case in get("/posts). You need to ensure that when you're returning a list of Post objects, FastAPI can handle this correctly.
By setting the response_model to List[schemas.PostResponse], FastAPI will iterate over the list of Post objects and convert each one into a PostResponse Pydantic model. 
The orm_mode = True configuration in the PostResponse model ensures that FastAPI knows how to convert the SQLAlchemy Post objects into dictionaries for JSON serialization.
'''

class PostOut(BaseModel):   # response for get all posts with votes.
    Post: PostResponse
    votes: int

    class Config:
        from_attributes= True


class UserCreate(BaseModel):
    email: EmailStr
    password: str

#  Response model for users model
class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes= True   # or orm_mode= True

#login authenticaton
# class UserLogin(BaseModel):
#     email: EmailStr
#     password: str  
# not needed because we used user_credentials: OAuth2PasswordRequestForm = Depends() in def login()

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

# schema for the data that we embed in the access token
class TokenData(BaseModel):
    id: Optional[int] = None



class Vote(BaseModel):
    post_id: int
    dir: int

    @field_validator('dir')
    def check_binary_value(cls, value):
        if value not in [0, 1]:  # Ensure the value is either 0 or 1
            raise ValueError('dir must be either 0 or 1')
        return value
