import uvicorn as uvicorn
from fastapi import FastAPI
from presentation.routes.links import router as links_handler

app = FastAPI()
app.include_router(links_handler, tags=['link'])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


