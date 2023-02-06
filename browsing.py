from playwright.sync_api import sync_playwright


def get_full_page(url: str):
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        page.goto(url)

        page.wait_for_selector("div#forecast_list_ul")
        print(page.content())

        contents = page.content()

    return contents


if __name__ == '__main__':
    c = get_full_page('london')
    with open('page.html', 'w') as file:
        print(c, file=file)
