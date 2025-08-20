import requests

headers = {
    
    "Authorization": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwiZXhwIjoxNzU1Nzg2NTUwfQ.Et6n8aYb2IHfy-iIz-uAfV8aXX8-z79HdJO2LuguTNM"
    
    }


request = requests.get("http://127.0.0.1:8000/auth/refresh", headers=headers)
print(request)
print(request.json)

