from fastapi import FastAPI, Security, HTTPException, Depends, Request
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from starlette.status import HTTP_403_FORBIDDEN
import logging

from browsing import get_full_page
from config import API_KEY, API_KEY_NAME, ADMIN_KEY, ADMIN_KEY_NAME


api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)

admin_key_query = APIKeyQuery(name=ADMIN_KEY_NAME, auto_error=False)
admin_key_header = APIKeyHeader(name=ADMIN_KEY_NAME, auto_error=False)


app = FastAPI()


def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
    api_key_cookie: str = Security(api_key_cookie),
):

    if api_key_query == API_KEY:
        return api_key_query
    elif api_key_header == API_KEY:
        return api_key_header
    elif api_key_cookie == API_KEY:
        return api_key_cookie
    else:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid credentials // Max Ulianov 2023")


def get_admin_key(
    admin_key_query: str = Security(admin_key_query),
    admin_key_header: str = Security(admin_key_header)
):
    if admin_key_query == ADMIN_KEY:
        return admin_key_query
    elif admin_key_header == ADMIN_KEY:
        return admin_key_header
    else:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Permission denied // Max Ulianov 2023")


@app.get("/browse")
def browse_page(request: Request, api_key: APIKey = Depends(get_api_key)):
    if request.headers.get('link') is None:
        return None

    url = request.headers.get('link')
    logging.info(f'Received url for parsing: {url}')
    return get_full_page(url)


@app.get("/logs")
def get_logs(admin_key: APIKey = Depends(get_admin_key)):
    try:
        with open('logfile.log', 'r') as logfile:
            logs = logfile.read()
    except FileNotFoundError as e:
        logs = repr(e)

    return logs


@app.get("/page")
def page(admin_key: APIKey = Depends(get_admin_key)):
    with open('page.html', 'r') as pagefile:
        return pagefile.read()
