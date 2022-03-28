**Main technologies**
 - [FastAPI](https://fastapi.tiangolo.com/)
 - [TortoiseORM](https://fastapi.tiangolo.com/) and [Aerich](https://github.com/tortoise/aerich/blob/dev/README.md) as a database migrations tool
 
**ENVIRONMENT VARIABLES:**

Create file ```.env``` with following environmental variables:

Postgres Configs:
- DB_USER
- DB_PASS
- DB_HOST
- DB_NAME

JWT Auth Configs:
- JWT_SECRET
- ACCESS_TOKEN_EXP_MINUTES
- REFRESH_TOKEN_EXP_HOURS

Email Configs:
- EMAIL_HOST_USER
- EMAIL_HOST_PASSWORD

**Start project**

Install dependencies:
```shell
poetry install
```
Migrate database:
```shell
aerich upgrade
```
Run project:
```shell
python run.py
```