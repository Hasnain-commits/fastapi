from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    print("Hello World!")