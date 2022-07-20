create
curl -X POST http://127.0.0.1:8000/auth/users/ --data 'username=djoser&password=alpine12'

try login without creds
curl -LX GET http://127.0.0.1:8000/auth/users/me/


curl -X POST http://127.0.0.1:8000/auth/token/login/ --data 'username=djoser&password=alpine12'


curl -X POST http://127.0.0.1:8000/auth/users/ --data 'username=djoser2&password=alpine12'