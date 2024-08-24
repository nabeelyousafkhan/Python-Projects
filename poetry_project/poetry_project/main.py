from fastapi import FastAPI

app = FastAPI(title="Hello World API", 
    version="0.0.1",
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development Server"
        }
        ])

@app.get("/")

def get_root():
    return {'message': 'This is Root'}

@app.get("/Items")
def get_Items():
    return {'message': 'This is Item'}

