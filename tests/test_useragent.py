import pytest
from playwright.async_api import async_playwright

from playwright_stealth.stealth import StealthConfig

# todo: for every browser, for every connection method

async def test_navigator_webdriver():
    async with async_playwright() as p:
        StealthConfig().hook_context_async(p)
        browser = await p.chromium.launch()
        page = await browser.new_page()
        assert await page.evaluate("navigator.webdriver") is False
        other_context = await browser.new_context()
        other_page = await other_context.new_page()
        assert await other_page.evaluate("navigator.webdriver") is False
