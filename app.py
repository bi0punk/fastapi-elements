from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sqlite3

app = FastAPI()

# Modelo Pydantic para los elementos
class Element(BaseModel):
    name: str
    atomic_number: int
    symbol: str
    mass: float
    exact_mass: float
    ionization: float
    electron_affinity: float
    electronegativity: float
    covalent_radius: float
    van_der_waals_radius: float
    melting_point: float
    boiling_point: float
    family: str

# Función para obtener elementos de la base de datos
def get_elements(element_id: int) -> List[Element]:
    try:
        connection = sqlite3.connect('elements.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Elements WHERE NumeroAtomico = ?;', (element_id,))
        results = cursor.fetchall()
        elements = []
        for row in results:
            element = Element(
                name=row[0], 
                atomic_number=row[1],
                symbol=row[2],
                mass=row[3],
                exact_mass=row[4],
                ionization=row[5],
                electron_affinity=row[6],
                electronegativity=row[7],
                covalent_radius=row[8],
                van_der_waals_radius=row[9],
                melting_point=row[10],
                boiling_point=row[11],
                family=row[12]
            )
            elements.append(element)
        return elements
    finally:
        connection.close()

# Ruta para obtener elementos por ID
@app.get('/elements', response_model=List[Element])
async def get_elements_by_id(id: Optional[int] = None):
    if id is not None:
        elements = get_elements(id)
        if not elements:
            raise HTTPException(status_code=404, detail="Element not found")
        return elements
    else:
        raise HTTPException(status_code=400, detail="Parameter 'id' not provided")
