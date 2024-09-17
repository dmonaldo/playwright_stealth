import pytest
from playwright.async_api import async_playwright

from playwright_stealth.stealth import StealthConfig

@pytest.mark.parametrize("browser_type", ["chromium", "firefox", "webkit"])
async def test_payload_executes_successfully(browser_type: str):
    async with async_playwright() as p:
        browser = await getattr(p, browser_type).launch()
        page = await browser.new_page()
        await page.evaluate(StealthConfig().script_payload)


async def test_navigator_webdriver(hooked_async_browser):
    assert await (await hooked_async_browser.new_page()).evaluate("navigator.webdriver") is False
    assert await (await (await hooked_async_browser.new_context()).new_page()).evaluate("navigator.webdriver") is False

# async def test_navigator_languages(hooked_async_browser):
#     assert await (await hooked_async_browser.new_page()).evaluate("navigator.webdriver") is False
#     assert await (await (await hooked_async_browser.new_context()).new_page()).evaluate("navigator.webdriver") is False


