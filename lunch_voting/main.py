from fastapi import FastAPI

from routers import menu, restaurant, user, vote

# Initialize the FastAPI application
app = FastAPI()


app.include_router(menu.router)
app.include_router(restaurant.router)
app.include_router(user.router)
app.include_router(vote.router)


# A simple root endpoint to verify the app is running
@app.get("/")
async def root():
    return {"message": "Hello World"}
