from playwright import async_api
from playwright.async_api import async_playwright

from playwright_stealth import Stealth


async def test_cli_args_are_patched_correctly(hooked_async_browser):
    page = await hooked_async_browser.new_page()

    console_messages = []

    def collect_log_message(msg: async_api.ConsoleMessage):
        console_messages.append(msg.text)

    page.on("console", collect_log_message)

    await page.goto("http://example.org")
    webdriver_js_was_patched = not any(map(lambda x: "not patching navigator.webdriver" in x, console_messages))
    languages_js_was_patched = not any(map(lambda x: "not patching navigator.languages" in x, console_messages))
    # iff browser is chromium, we should patch the CLI args
    if hooked_async_browser.browser_type == "chromium":
        assert not webdriver_js_was_patched
        assert not languages_js_was_patched
    else:
        assert webdriver_js_was_patched
        assert languages_js_was_patched


async def test_init_scripts_respected():
    async with Stealth().use_async(async_playwright()) as ctx:
        # only chromium cli args are instrumented, so that's the only we check
        await ctx.chromium.launch()
