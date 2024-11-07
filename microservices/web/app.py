from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers import auth
from middlewares.TokenValidationMiddleware import TokenValidationMiddleware
from middlewares.ExceptionHandlingMiddleware import ExceptionHandlingMiddleware
from utils.constants import USER_SESSION_KEY

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include auth router
app.include_router(auth.router, prefix="/auth")

# Add middleware
app.add_middleware(TokenValidationMiddleware)
app.add_middleware(ExceptionHandlingMiddleware)

@app.get("/")
async def read_root(request: Request):
    cookies = request.cookies
    return templates.TemplateResponse("index.html", {"request": request, "cookies": cookies})

@app.get("/protected")
async def protected(request: Request):
    user_session = request.cookies.get(USER_SESSION_KEY)
    return templates.TemplateResponse(
        "protected.html", {"request": request, "user_session": user_session}
    )

@app.get("/dag")
async def dag(request: Request):
    return templates.TemplateResponse("dag.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8888, reload=True)
