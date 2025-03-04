from playwright.sync_api import sync_playwright, Playwright

playwright = sync_playwright().start()

chromium = playwright.chromium
browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
default_context = browser.contexts[0]
page = default_context.pages[0]
page.get_by_role("button",name="로그인").click(force=True)
print("confirm clicked")