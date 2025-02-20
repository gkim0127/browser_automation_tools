import asyncio
from playwright.async_api import async_playwright
import json
import pathlib

async def save_session_data(page, cookies_path, local_storage_path, session_storage_path):
    # Save cookies
    cookies = await page.context.cookies()
    with open(cookies_path, "w") as json_file:
        json.dump(cookies, json_file)
    print("Cookies saved.")

    # Save localStorage
    local_storage = await page.evaluate('window.localStorage')  # Get the entire localStorage
    with open(local_storage_path, "w") as json_file:
        json.dump(local_storage, json_file)
    print("LocalStorage saved.")

    # Save sessionStorage
    session_storage = await page.evaluate('window.sessionStorage')  # Get the entire sessionStorage
    with open(session_storage_path, "w") as json_file:
        json.dump(session_storage, json_file)
    print("SessionStorage saved.")

async def load_session_data(page, cookies_path, local_storage_path, session_storage_path):
    # Load cookies
    if cookies_path.exists():
        with open(cookies_path, "r") as json_file:
            cookies = json.load(json_file)
            await page.context.add_cookies(cookies)
        print("Cookies loaded.")

    # Load localStorage
    if local_storage_path.exists():
        with open(local_storage_path, "r") as json_file:
            local_storage = json.load(json_file)
            await page.evaluate(f'window.localStorage.clear()')  # Clear existing localStorage
            for key, value in local_storage.items():
                await page.evaluate(f'window.localStorage.setItem("{key}", "{value}")')
        print("LocalStorage loaded.")

    # Load sessionStorage
    if session_storage_path.exists():
        with open(session_storage_path, "r") as json_file:
            session_storage = json.load(json_file)
            await page.evaluate(f'window.sessionStorage.clear()')  # Clear existing sessionStorage
            for key, value in session_storage.items():
                await page.evaluate(f'window.sessionStorage.setItem("{key}", "{value}")')
        print("SessionStorage loaded.")

async def main():
    async with async_playwright() as p:
        # Launch the browser with more permissions
        browser = await p.chromium.launch(headless=False, slow_mo=50)
        
        # Create a new browser context
        context = await browser.new_context()

        # Create a new page within the context
        page = await context.new_page()

        # Paths to the session data files
        cookies_path = pathlib.Path(__file__).parent.resolve() / "cookies.json"
        local_storage_path = pathlib.Path(__file__).parent.resolve() / "local_storage.json"
        session_storage_path = pathlib.Path(__file__).parent.resolve() / "session_storage.json"

        # Load session data if the files exist
        await load_session_data(page, cookies_path, local_storage_path, session_storage_path)

        # Navigate to the website
        await page.goto("https://www.koreanair.com/?hl=ko")

        # Wait for the page to load completely
        await page.wait_for_load_state("domcontentloaded")

        # Check if logged in by looking for a profile or user element
        try:
            profile_element = page.locator("text=My Profile")  
            is_logged_in = await profile_element.is_visible()
            if is_logged_in:
                print("Successfully logged in with cookies and session data.")
            else:
                print("Not logged in with cookies and session data. Proceeding to login.")
                # Perform login steps if not logged in
                await page.get_by_role("button", name="동의합니다").click()  # Cookie consent
                print("Cookie consent clicked.")
                await page.get_by_role("button", name="로그인", exact=True).click(force=True)
                print("Login button clicked.")
                await page.get_by_role("textbox", name="아이디").fill("")
                await page.get_by_role("textbox", name="비밀번호").fill("")
                await page.locator("button.login__submit-act").click()
                print("Login submitted.")
                await page.get_by_role("button", name="90일 후에 변경").click()
                print("Clicked on '90일 후에 변경'.")

                # Save session data after login
                await save_session_data(page, cookies_path, local_storage_path, session_storage_path)

        except Exception as e:
            print(f"Error checking login status: {e}")

        # Wait for a while to observe the result
        await page.wait_for_timeout(10000)

        # Close the browser
        await browser.close()

# Run the script
asyncio.run(main())
