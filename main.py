import pandas as pd
from fastapi import FastAPI

app = FastAPI()

data_file = "data.csv"
stands = []

def load_stands():
    global stands
    try:
        df = pd.read_csv(data_file)
        stands = df.to_dict(orient="records")
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        stands = []

@app.on_event("startup")
def startup_event():
    load_stands()

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de los stands de JoJo"}

@app.get("/stands")
def get_stands():
    return stands

@app.get("/stands/{stand_id}")
def get_stand(stand_id: int):
    stand = next((s for s in stands if s["Id"] == stand_id), None)
    return stand or {"error": "Stand no encontrado"}

@app.post("/reload")
def reload_stands():
    load_stands()
    return {"message": "Datos recargados"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
