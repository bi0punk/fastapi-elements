from fastapi import FastAPI, HTTPException, Depends, Security, status
from fastapi.responses import HTMLResponse
from fastapi.security.api_key import APIKeyQuery, APIKeyHeader, APIKey
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
        cursor.execute('SELECT * FROM Elements WHERE AtomicNumber = ?;', (element_id,))
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

# Configuración de la API Key
API_KEY = "tu_api_key_secreta"
API_KEY_NAME = "access_token"
api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
):
    if api_key_query == API_KEY:
        return api_key_query
    elif api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

# Ruta protegida para obtener elementos por ID
@app.get('/elements', response_model=List[Element])
async def get_elements_by_id(id: Optional[int] = None, api_key: APIKey = Depends(get_api_key)):
    if id is not None:
        elements = get_elements(id)
        if not elements:
            raise HTTPException(status_code=404, detail="Element not found")
        return elements
    else:
        raise HTTPException(status_code=400, detail="Parameter 'id' not provided")

# Ruta de consulta (opcionalmente protegida por API Key)
@app.get("/consulta", response_class=HTMLResponse)
async def consulta(api_key: APIKey = Depends(get_api_key)):  # Si deseas requerir API Key para esta ruta
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Consulta de Elementos</title>
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    </head>
    <body>
        <div class="container">
            <h1>Consulta de Elementos Químicos</h1>
            <div class="form-group">
                <label for="elementId">Número Atómico:</label>
                <input type="number" id="elementId" class="form-control">
            </div>
            <button onclick="consultarElemento()" class="btn btn-primary">Consultar</button>
            <div id="resultado" class="mt-3"></div>
        </div>
        <script>
    function consultarElemento() {
        var id = document.getElementById("elementId").value;
        fetch('/elements?id=' + id)
            .then(response => response.json())
            .then(data => {
                var markdown = data.map(element => \`## \${element.name} (\${element.symbol})\n- Atomic Number: \${element.atomic_number}\n- Mass: \${element.mass}\n- Electronegativity: \${element.electronegativity}\`).join("\\n\\n");
                document.getElementById('resultado').innerHTML = marked(markdown);
            })
            .catch(error => {
                document.getElementById('resultado').innerHTML = "Elemento no encontrado o error en la consulta";
            });
    }
</script>

    </body>
    </html>
    """
    return html_content
