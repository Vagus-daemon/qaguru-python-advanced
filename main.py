from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def main():
    return "Hello world"


#@app.get("/status")
#def main():
#    return "{status:ok}"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
