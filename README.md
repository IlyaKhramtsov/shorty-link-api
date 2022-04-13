# shorty-link-api

### Description
shorty-link-api - is a web service for shortening URLs.

## Registration and authentication endpoints

### /auth/users/
New user registration.

Method: `POST`

Arguments:

- `username`
- `password`
- `email`

Example: 
```bash
curl --data "username=new_user&password=yourpassword&email=user@mail.com" http://127.0.0.1:8000/auth/users/
```
Response:
```json
{
  "email":"user@mail.com",
  "username":"new_user",
  "id":1
}
```
### /auth/jwt/create/

Creating a JSON Web Token (JWT).

Method: `POST`

Arguments:

- `username`
- `password`
- `email`

Example: 
```bash
curl --data "username=new_user&password=yourpassword&email=user@mail.com" http://127.0.0.1:8000/auth/jwt/create/
```
Response:
```json
{
  "refresh":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY0OTg3ODgyOCwianRpIjoiMDUyNDRjNTQ5ZGFjNGUzOTlhYTdkODZlOGFlOTNhYjYiLCJ1c2VyX2lkIjo0fQ.fTSNW91hE3a3iNuDGIzPBIIKs6cwrYKjxCFtXeAccpw",
  "access":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ5NzkyNzI4LCJqdGkiOiI5MzU4MzUwZjA4ZTQ0NDJiYTAzOTNjYmVmMWQyNmNmYiIsInVzZXJfaWQiOjR9.sIrfCNLa_r-mIXsFreEWq2JR1HAGf9abrf-0k3Z6xZA"
}
```
### /auth/jwt/refresh/

Getting a new JWT after the lifetime of the previously generated one has expired.

Method: `POST`

Arguments:

- `refresh`: The token that was previously obtained along with the access token.

Example: 
```bash
curl --data "refresh=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY0OTg3ODgyOCwianRpIjoiMDUyNDRjNTQ5ZGFjNGUzOTlhYTdkODZlOGFlOTNhYjYiLCJ1c2VyX2lkIjo0fQ.fTSNW91hE3a3iNuDGIzPBIIKs6cwrYKjxCFtXeAccpw" http://127.0.0.1:8000/auth/jwt/refresh/
```
Response:
```json
{
  "access":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ5NzkzNjY1LCJqdGkiOiIwMDAyMGUwMzQyODQ0NDIxODYzZjA1YWRjNGJkYWM3MCIsInVzZXJfaWQiOjR9.-JJzmdKgKTyjVZG2rzoOguSfUr1UfowQs8ms00MxVDc"
}
```

## API Endpoints

All API calls will commence with the base URL, `/api/v1/`.

### /api/v1/shortener/
Getting a list of all shortened links.

Method: `GET`

Example:
```bash
$ curl http://127.0.0.1:8000/api/v1/shortener/
```

Response:

```json
[
  {
    "id":  2,
    "short_url": "http://127.0.0.1:8000/NO1UmLk8tG",
    "link": "https://yandex.ru/",
    "short_id" :"NO1UmLk8tG",
    "created": "2022-04-10T15:58:17.559856Z"
  },
  {
    "id":  1,
    "short_url": "http://127.0.0.1:8000/google",
    "link": "https://google.com/",
    "short_id" :"google",
    "created": "2022-04-10T15:54:14.194478Z"
  }
]
```

### /api/v1/shortener/
Creating a shortened URL.

Method: `POST`

Arguments:

-   `link`: the URL to shorten (e.g `https://google.com`)
-   `short_id` (optional): a custom ending for the short URL. If left empty, a short id will be generated automatically.

The `link` argument must be URL encoded.

Response: A JSON representation of the shortened URL.

Example: 
```bash
$ curl -H "Accept: application/json" \
       -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ5NzkzNjY1LCJqdGkiOiIwMDAyMGUwMzQyODQ0NDIxODYzZjA1YWRjNGJkYWM3MCIsInVzZXJfaWQiOjR9.-JJzmdKgKTyjVZG2rzoOguSfUr1UfowQs8ms00MxVDc" \
       -d "link=http://www.yahoo.com/" \ 
       http://127.0.0.1:8000/api/v1/shortener/
```
Response:
```json
{
  "id":3,
  "short_url":"http://127.0.0.1:8000/IEO37A0ZLu",
  "link":"http://www.yahoo.com/",
  "short_id":"IEO37A0ZLu",
  "created":"2022-04-12T20:04:32.627494Z"
}
```