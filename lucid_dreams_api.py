from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
import cachetools

app = FastAPI()

# Simulated database to store user data, posts, and tokens
db_users = {}
db_posts = {}
cache = cachetools.LRUCache(maxsize=1000)

# Pydantic schemas for input and output validation
class User(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    token: str

class Post(BaseModel):
    text: str

class PostID(BaseModel):
    post_id: str

class ErrorResponse(BaseModel):
    detail: str

# Function to generate a random token (for demonstration purposes)
def generate_token():
    import secrets
    return secrets.token_hex(32)

# Function to check if a token is valid
def is_token_valid(token: str):
    return token in db_users.values()

# Function to check if a user exists and return their token
def get_user_token(email: str, password: str):
    user = db_users.get(email)
    print(db_users)
    if user and user['password'] == password:
        return user['token']
    return None

# Dependency to get the user's token from the header
def get_token(authorization: str = Depends(lambda x: None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token is missing or invalid")
    token = authorization.split(" ")[-1]
    if not is_token_valid(token):
        raise HTTPException(status_code=401, detail="Token is missing or invalid")
    return token

# Signup endpoint
@app.post("/signup", response_model=Token)
def signup(user: User):
    token = generate_token()
    db_users[user.email] = {'password': user.password, 'token': token}
    print("signup function called")
    print(db_users)
    return {'token': token}

# Login endpoint
@app.post("/login", response_model=Token)
def login(user: User):
    print("login function called")
    token = get_user_token(user.email, user.password)
    if not token:
        raise HTTPException(status_code=401, detail="Login failed")
    return {'token': token}

# AddPost endpoint
@app.post("/addPost", response_model=PostID)
def add_post(post: Post, token: str = Depends(get_token)):
    # Check and limit payload size (1MB)
    if len(post.text.encode('utf-8')) > 1024 * 1024:
        raise HTTPException(status_code=400, detail="Payload size exceeds 1MB limit")
    
    # Generate a post ID (for demonstration purposes)
    post_id = generate_token()[:8]
    
    # Save the post in memory
    db_posts[post_id] = {'text': post.text, 'token': token}
    
    return {'post_id': post_id}

# GetPosts endpoint with response caching
@app.get("/getPosts", response_model=list[Post], tags=["posts"])
def get_posts(token: str = Depends(get_token)):
    # Check if cached data exists
    cached_data = cache.get(token)
    if cached_data:
        return cached_data

    # Fetch user's posts from memory
    posts = [{'text': post['text']} for post in db_posts.values() if post['token'] == token]
    
    # Cache the data for 5 minutes
    cache[token] = posts

    return posts

# DeletePost endpoint
@app.delete("/deletePost", response_model=PostID)
def delete_post(post_id: str, token: str = Depends(get_token)):
    post = db_posts.get(post_id)
    if not post or post['token'] != token:
        raise HTTPException(status_code=403, detail="Permission denied")
    del db_posts[post_id]
    # Invalidate cache for this user's posts
    cache.pop(token, None)
    return {'post_id': post_id}
    
    
# bfb82bc9d54c2c7fdc81ac14848de770d942a7e488c768357876c9472af0288f