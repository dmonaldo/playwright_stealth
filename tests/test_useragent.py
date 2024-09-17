from playwright.async_api import async_playwright

from playwright_stealth.stealth import StealthConfig


async def test_navigator_webdriver():
    async with async_playwright() as p:
        StealthConfig().hook_context_async(p)
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://google.ca")
        assert await page.evaluate("navigator.webdriver") == False
        
