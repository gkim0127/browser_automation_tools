import asyncio
from playwright.async_api import async_playwright
import json
import pathlib


# save cookie
async def save_session_data(page,cookies_path):
    cookies = await page.context.cookies()
    with open(cookies_path, "w") as json_file:
        json.dump(cookies, json_file)
    print("Cookies saved.")

# load cookie
async def load_session_data(page,cookies_path):
    if cookies_path.exists():
        with open(cookies_path,"r") as json_file:
            cookies = json.load(json_file)
            await page.context.add_cookies(cookies)
        print("Cookies loaded")

# login
async def perform_login(page):

    #cookie confirmation
    #await page.get_by_role("button",name="동의합니다").click()
    print("confirm clicked")
    await page.get_by_role("textbox",name="아이디").fill("")
    await page.get_by_role("textbox",name="비밀번호").fill("")
    await page.get_by_role("textbox", name="아이디  필수 입력").press("Tab")
    await page.get_by_role("textbox", name="비밀번호 필수 입력").fill("")

    await page.get_by_role("main").get_by_role("button", name="로그인", exact=True).click()
    await page.get_by_role("button", name="일 후에 변경").click()

    print("login completed")

# actions after login

async def select_details(page):
        
    await page.get_by_role("button",name="마일리지 예매").click()
    #await page.get_by_role("radio", name="편도").check()
    #await page.get_by_label("편도").click()

    await page.get_by_role("group", name="여정 타입").locator("div").nth(2).click()

    # 출발지

    await page.get_by_role("button", name="출발지 TAE 대구").click(force=True)
    await page.wait_for_timeout(500)
    print("timeoutdone1")
    await page.keyboard.type('ICN')
    await page.get_by_role("combobox", name="도시 및 공항 검색").press("ArrowDown")
    await page.get_by_role("combobox", name="도시 및 공항 검색").press("Enter")
    
    # 도착지
    await page.get_by_role("button", name="To  도착지").click()
    await page.wait_for_timeout(500)
    print("timeoutdone2")
    await page.keyboard.type('BKK')
    await page.get_by_role("combobox", name="도시 및 공항 검색").press("ArrowDown")
    await page.get_by_role("combobox", name="도시 및 공항 검색").press("Enter")
    
    # 가는날 오는날 
    await page.get_by_role("button", name="출발일  가는 날").click()
    await page.get_by_role("button", name="다음 2달").click()
    await page.get_by_role("button", name="다음 2달").click()
    await page.get_by_role("button", name="다음 2달").click()
    await page.get_by_role("button", name="다음 2달").click()
    await page.get_by_role("button", name="다음 2달").click()
    await page.get_by_role("button", name="다음 2달").click()

    print("seleting date")
    await page.locator("#month202602").get_by_text("2", exact=True).click(force=True)
    #await page.locator("#month202602").get_by_text("2", exact=True).press("Enter")
    print("date selected")

    # 탑승객 
    print("selecting passengers")
    await page.get_by_role("button", name="탑승객  KIM YOUNG JUN").click()
    await page.get_by_text("KONG MIKYUNG").click()
    await page.get_by_role("button", name="선택", exact=True).click()
    print("selected passengers")
    

    #await page.wait_for_selector('#departureBtnf5b6e158eff27f2f920f6b10f5d7ed10', state='visible')
    #await page.click('#departureBtnf5b6e158eff27f2f920f6b10f5d7ed10')

    # search button
    await page.get_by_role("button",name="항공편 검색").click()
    print("search clicked")

    # 비행기 선택
    # select by rows cols 
    #label = page.locator('label[for="flight-bonus00"]').filter(has_text="일반석40,000 마일")

    # Select the last one 항상 마지막꺼 선택
    count = await page.locator("label").filter(has_text="일반석40,000 마일").count()
    label = page.locator("label").filter(has_text="일반석40,000 마일").nth(count - 1)
    await label.click()
    print("cabin selected")
    await page.get_by_role("button", name="다음").click()
    print("confirmation page loading")

    # 결제 전 동의창
    await page.get_by_label("성인 1").get_by_role("button", name="확인").click()
    print("김영준 확인")
    await page.get_by_label("성인 2").get_by_role("button", name="확인").wait_for(state="visible")
    #await page.wait_for_timeout(1000)
    await page.get_by_label("성인 2").get_by_role("button", name="확인").click()
    print("공미경 확인")

    await page.get_by_role("checkbox", name="아래 모든 탑승객에게 상기 연락처를 동일하게 입력합니다").click(force=True)
    print("checkbox completed")
    await page.get_by_label("연락처 정보").get_by_role("button",name="확인").click()

    await page.locator('#btn-resv-agree-1').click(force=True)
    await page.get_by_role("button", name="아래로 스크롤").click()
    await page.get_by_role("button", name="확인").click()
    print("first agreement done")
    await page.locator("#btn-resv-agree-3").click(force=True)
    await page.get_by_role("button", name="아래로 스크롤").click()
    await page.get_by_role("button", name="아래로 스크롤").click()
    await page.get_by_role("button", name="확인").click()
    await page.get_by_role("button", name="적용").click()
    print("second agreement done")

    await page.get_by_role("button", name="결제하기").click()
    print("payment")
    #await page.get_by_role("button", name="앱카드 결제").click()
    


    



async def main():
    async with async_playwright() as p:

        new_browser = await p.firefox.launch(headless=False,slow_mo=500)
        new_page = await new_browser.new_page(locale="ko-KR")

        # loading cookie
        cookies_path = pathlib.Path(__file__).parent.resolve() / "cookies.json"
        await load_session_data(new_page, cookies_path)

        await new_page.goto("https://www.koreanair.com/login?returnUrl=%2F")
        #await page.wait_for_timeout(1000000)
        await new_page.wait_for_load_state("domcontentloaded")
        # check if logged in
        login_flag =  new_page.locator("text=마이페이지")
        is_logged_in = await login_flag.is_visible()
        print("checking if logged in")
        

        if is_logged_in: 
            print("is logged in")
            print("selecting details")
            await select_details(new_page)
        
        else: 
            print("not logged in")
            print("loggin in now")
            await perform_login(new_page)
            await save_session_data(new_page,cookies_path)
            await select_details(new_page)
        

        await new_page.wait_for_timeout(100000)
asyncio.run(main()) 