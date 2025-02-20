import asyncio
from playwright.async_api import async_playwright
import json
import pathlib

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False,slow_mo=50)
        page = await browser.new_page()
        await page.goto("https://www.koreanair.com/?hl=ko")
        #await page.wait_for_timeout(1000000)

        # cookie confirmation
        await page.get_by_role("button",name="동의합니다").click()
        print("confirm clicked")
        
        #login button
        await page.get_by_role("button",name="로그인", exact=True).click(force=True)
        print("Login button clicked")
        

        #Fill in ID and password

        await page.get_by_role("textbox",name="아이디").fill("")
        await page.get_by_role("textbox",name="비밀번호").fill("")
        await page.locator("button.login__submit-act").click()
        await page.get_by_role("button",name="90일 후에 변경").click()
        
        # # Save storage state into the file.
        # storage = await context.storage_state(path="state.json")

        # # Create a new context with the saved storage state.
        # context = await browser.new_context(storage_state="state.json")

        with open("{0}/{1}".format(pathlib.Path(__file__).parent.resolve(), "CCcookies.json"), "w") as json_file:
                json.dump(await page.context.cookies(), json_file)


        await page.wait_for_timeout(100000)
asyncio.run(main()) 