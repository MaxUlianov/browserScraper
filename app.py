from fastapi import FastAPI
from browsing import get_full_page

app = FastAPI()


@app.get("/browse/{url}")
def browse_page(url: str):
    item = 'london'
    url = f'https://openweathermap.org/find?q={item}'

    return get_full_page(url)
