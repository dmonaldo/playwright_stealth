import pytest
from playwright import async_api
from playwright.async_api import async_playwright

from playwright_stealth import StealthConfig


@pytest.fixture(params=["chromium", "firefox", "webkit"])
async def hooked_async_browser(request) -> async_api.Browser:
    async with async_playwright() as ctx:
        StealthConfig().hook_context_async(ctx)
        browser = await ctx[request.param].launch()
        yield browser