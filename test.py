import requests

response = requests.get(
    'http://localhost:5000/models',
    json={
'modelsIds': {            'Model1': [1, 2, 3],
            'Model2': [4, 5, 6],
            'Model3': [7, 8, 9],
}    }
)

print(response)
print(response.json())