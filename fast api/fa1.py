from fastapi import FastAPI
 
app = FastAPI()
 
@app.get("/")
def userlog():
    return{"message":"my first api"}
 
@app.get("/user")
def userdetail(name:str):
    return{"my name": name}
 
@app.post("/detail")
def demo(name: str, age:int):
    return{"name": name, "age": age}