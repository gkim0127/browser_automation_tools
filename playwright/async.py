import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False,slow_mo=50)
        page = await browser.new_page()
        await page.goto("https://www.koreanair.com/login?returnUrl=%2F")
        #await page.wait_for_timeout(1000000)

        #cookie confirmation
        await page.get_by_role("button",name="동의합니다").click()
        print("confirm clicked")
        
        # #login button
        # await page.get_by_text("로그인").click()
        # print("Login button clicked")
        

        #Fill in ID and password

        await page.get_by_role("textbox",name="아이디").fill("")
        await page.get_by_role("textbox",name="비밀번호").fill("")
        await page.get_by_role("textbox", name="아이디  필수 입력").press("Tab")
        await page.get_by_role("textbox", name="비밀번호 필수 입력").fill("")

        await page.get_by_role("main").get_by_role("button", name="로그인", exact=True).click()
        await page.get_by_role("button", name="일 후에 변경").click()
        
        # simultaneously fill both in
        # await asyncio.gather (
        #     page.get_by_role("textbox",name="아이디").fill("kyjma1"),
        #     page.get_by_role("textbox",name="비밀번호").fill("kmk006091!")
        # )
        
        await page.get_by_role("button",name="마일리지 예매").click()
        #await page.get_by_text("편도").click()

        #출발지
        await page.get_by_role("button", name="출발지 TAE 대구").click()
        await page.get_by_role("combobox", name="도시 및 공항 검색").fill("ICN")
        await page.get_by_role("combobox", name="도시 및 공항 검색").press("Enter")
        #도착지
        await page.get_by_role("button", name="To 도착지").click()
        await page.get_by_role("combobox", name="도시 및 공항 검색").fill("BKK")
        await page.get_by_role("combobox", name="도시 및 공항 검색").press("Enter")
        # 가는날 오는날 
        await page.get_by_role("button", name="출발일  가는 날 오는 날").click()
        await page.get_by_role("button", name="다음 2달").click()
        await page.get_by_role("button", name="다음 2달").click()
        await page.get_by_role("button", name="다음 2달").click()
        await page.get_by_role("button", name="다음 2달").click()
        await page.get_by_role("button", name="다음 2달").click()
        await page.locator("#month202602").get_by_text("1", exact=True).click()




        #await page.wait_for_selector('#departureBtnf5b6e158eff27f2f920f6b10f5d7ed10', state='visible')
        #await page.click('#departureBtnf5b6e158eff27f2f920f6b10f5d7ed10')
        print("departure clicked")
        


        # # search button
        # await page.get_by_role("button",name="항공편 검색").click()
        # print("search clicked")

        await page.wait_for_timeout(100000)
asyncio.run(main()) 