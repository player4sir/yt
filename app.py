from flask import Flask, request
from playwright.async_api import async_playwright

app = Flask(__name__)

class Ytb:
    async def run(self, ids):
        try:
            async with async_playwright() as pw:
                browser = await pw.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto("https://ytmp3s.nu/")

                url_input = await page.query_selector('input[name="url"]')
                await url_input.fill(f"https://music.youtube.com/watch?v={ids}")

                submit_button = await page.query_selector('input[type="submit"]')
                await submit_button.click()

                download_btn = await page.wait_for_selector(
                    'body > form > div:nth-child(2) > a:nth-child(1)', timeout=5000
                )
                download_link = None
                if download_btn is not None:
                    download_link = await download_btn.get_attribute("href")

                await browser.close()

            return download_link
        except Exception as e:
            print(f"An error occurred: {e}")
            return {"error": "An error occurred"}

@app.route('/api', methods=['GET'])
async def get_download_link():
    ids = request.args.get('id')
    dw = Ytb()
    download_link = await dw.run(ids)
    return {"link": download_link} if "http" in download_link else {"error": "Timeout"}

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=False)
