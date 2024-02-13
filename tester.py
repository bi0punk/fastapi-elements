import requests
import random

# URL base de la API (ajustar según sea necesario)
BASE_URL = "http://127.0.0.1:8000"

def test_get_elements_by_id(element_id):
    """Prueba el endpoint /elements para obtener elementos por su ID."""
    url = f"{BASE_URL}/elements?id={element_id}"
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Elemento encontrado para ID {element_id}: {response.json()}")
    elif response.status_code == 404:
        print(f"Elemento con ID {element_id} no encontrado.")
    else:
        print(f"Error {response.status_code} para ID {element_id}")

def generate_random_ids_and_test(n):
    """Genera y prueba n IDs al azar para el endpoint /elements."""
    for _ in range(n):
        # Genera un ID al azar en un rango definido (ajusta según tus datos)
        random_id = random.randint(1, 116)  # Ajusta el rango según la base de datos
        test_get_elements_by_id(random_id)

if __name__ == "__main__":
    # Solicita al usuario el número de veces que desea realizar la consulta
    try:
        n_tests = int(input("Ingrese la cantidad de veces que desea consultar la API: "))
        generate_random_ids_and_test(n_tests)
    except ValueError:
        print("Por favor, ingrese un número válido.")
