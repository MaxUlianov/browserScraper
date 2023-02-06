from fastapi import FastAPI, Security, HTTPException, Depends
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from starlette.status import HTTP_403_FORBIDDEN

from browsing import get_full_page
from config import API_KEY, API_KEY_NAME, COOKIE_DOMAIN


api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)

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
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid credentials")


@app.get("/browse/{url}")
def browse_page(url: str, api_key: APIKey = Depends(get_api_key)):
    item = 'london'
    url = f'https://openweathermap.org/find?q={item}'

    return get_full_page(url)


@app.get("/logs")
def get_logs(api_key: APIKey = Depends(get_api_key)):
    try:
        with open('logfile.log', 'r') as logfile:
            logs = logfile.read()
    except FileNotFoundError as e:
        logs = repr(e)

    return logs


@app.get("/page")
def page(api_key: APIKey = Depends(get_api_key)):
    with open('page.html', 'r') as pagefile:
        return pagefile.read()
