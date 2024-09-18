import pytest
from playwright import async_api
from playwright.async_api import async_playwright

from playwright_stealth import Stealth


@pytest.fixture(params=["chromium", "firefox", "webkit"])
async def hooked_async_browser(request) -> async_api.Browser:
    async with Stealth().use_async(async_playwright()) as ctx:
        browser = await ctx[request.param].launch()
        yield browser