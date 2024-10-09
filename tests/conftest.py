import pytest
from playwright import async_api, sync_api
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright

from playwright_stealth import Stealth

script_logging = True


@pytest.fixture(params=["chromium", "firefox"])
async def hooked_async_browser(request) -> async_api.Browser:
    async with Stealth(script_logging=script_logging).use_async(async_playwright()) as ctx:
        browser = await ctx[request.param].launch()
        yield browser


@pytest.fixture(params=["chromium", "firefox"])
def hooked_sync_browser(request) -> sync_api.Browser:
    with Stealth(script_logging=script_logging).use_sync(sync_playwright()) as ctx:
        browser = ctx[request.param].launch()
        yield browser
