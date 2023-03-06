import uvicorn
from celery import Celery
from fastapi import FastAPI

app = FastAPI()

celery = Celery(
    __name__,
    broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/0"
)


@celery.task(serializer='json')
def divide_task(x, y):
    import time
    time.sleep(5)
    return x / y


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/task")
async def start_task(x: int, y: int):
    task = divide_task.delay(x, y)
    return task.id


@app.get("/task")
async def get_task_result(task_id: str):
    task = divide_task.delay(1, 2)
    return task.id


if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='localhost')
