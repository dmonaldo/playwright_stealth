import pytest
from playwright import async_api
from playwright.async_api import async_playwright

from playwright_stealth.stealth import Stealth


@pytest.mark.parametrize("browser_type", ["chromium", "firefox", "webkit"])
async def test_payload_executes_successfully(browser_type: str):
    # we test this because exceptions won't propagate with page.add_init_scripts, but will with page.evaluate
    async with async_playwright() as p:
        browser = await getattr(p, browser_type).launch()
        page = await browser.new_page()
        await page.goto("http://example.org")
        await page.evaluate(Stealth().script_payload)


async def test_navigator_webdriver(hooked_async_browser):
    for page in [await hooked_async_browser.new_page(), await (await hooked_async_browser.new_context()).new_page()]:
        await page.goto("http://example.org")
        assert await page.evaluate("navigator.webdriver") is False


@pytest.mark.parametrize("browser_type", ["chromium", "firefox", "webkit"])
async def test_cli_args_are_patched_correctly(browser_type: str):
    async with Stealth(script_logging=True).use_async(async_playwright()) as ctx:
        browser = await getattr(ctx, browser_type).launch()
        page = await browser.new_page()

        console_messages = []

        def collect_log_message(msg: async_api.ConsoleMessage):
            console_messages.append(msg.text)

        page.on("console", collect_log_message)

        await page.goto("http://example.org")
        assert any(map(lambda x: "not patching navigator.webdriver" in x, console_messages))
        assert any(map(lambda x: "not patching navigator.languages" in x, console_messages))
