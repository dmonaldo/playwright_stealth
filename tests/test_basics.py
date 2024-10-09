import asyncio
import logging

import pytest
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright

from playwright_stealth.stealth import Stealth


@pytest.mark.parametrize("browser_type", ["chromium", "firefox"])
async def test_async_smoketest(browser_type: str):
    # we test this because exceptions won't propagate with page.add_init_scripts, but will with page.evaluate
    async with async_playwright() as p:
        browser = await getattr(p, browser_type).launch()
        page = await browser.new_page()
        await page.goto("http://example.org")
        await page.evaluate(Stealth().script_payload)


@pytest.mark.parametrize("browser_type", ["chromium", "firefox"])
def test_sync_smoketest(browser_type: str):
    with sync_playwright() as p:
        browser = getattr(p, browser_type).launch()
        page = browser.new_page()
        page.goto("http://example.org")
        page.evaluate(Stealth().script_payload)


async def test_async_navigator_webdriver_smoketest(hooked_async_browser):
    for page in [await hooked_async_browser.new_page(), await (await hooked_async_browser.new_context()).new_page()]:
        logging.getLogger(__name__).warning("hello")
        page.on("console", lambda x: logging.getLogger(__name__).warning(x.text))
        await page.goto("http://example.org")
        await asyncio.sleep(1)
        assert await page.evaluate("navigator.webdriver") is False


def test_sync_navigator_webdriver_smoketest(hooked_sync_browser):
    for page in [hooked_sync_browser.new_page(), hooked_sync_browser.new_context().new_page()]:
        page.goto("http://example.org")
        assert page.evaluate("navigator.webdriver") is False
