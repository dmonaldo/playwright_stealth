from playwright_stealth import Stealth

# playwright_stealth

Transplanted from [puppeteer-extra-plugin-stealth](https://github.com/berstend/puppeteer-extra/tree/master/packages/puppeteer-extra-plugin-stealth), with some improvements. Don't expect this to bypass anything but the simplest of bot detection methods. Consider this a proof-of-concept starting point. Anyone serious about anti-bot detections wouldn't be publishing their methods :)

## Install

```
$ pip install playwright-stealth
```

## Example Usage

```python
import asyncio

from playwright.async_api import async_playwright
from playwright_stealth import Stealth


async def main():
    # This is the recommended usage. All pages created will have stealth applied:
    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        print("from new_page: ", await page.evaluate("navigator.webdriver"))
        different_context = await browser.new_context()
        page_from_different_context = await different_context.new_page()
        print("from new_context: ", await page_from_different_context.evaluate("navigator.webdriver"))

    # Specifying config options and applying evasions to an entire context:
    custom_hardware_concurrency = 32
    stealth = Stealth(
        navigator_hardware_concurrency=custom_hardware_concurrency,
        init_scripts_only=True
    )
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        await stealth.apply_stealth_async(context)
        page_1 = await context.new_page()
        concurrency_on_page_1_mocked = await page_1.evaluate("navigator.hardwareConcurrency") == custom_hardware_concurrency
        print("manually applied stealth applied to page 1:", concurrency_on_page_1_mocked)
        page_2 = await context.new_page()
        concurrency_on_page_2_mocked = await page_2.evaluate("navigator.hardwareConcurrency") == custom_hardware_concurrency
        print("manually applied stealth applied to page 2:", concurrency_on_page_2_mocked)


asyncio.run(main())
```
A set of 
## Test results

### playwright with stealth

![playwright without stealth](./images/example_with_stealth.png)

### playwright without stealth

![playwright with stealth](./images/example_without_stealth.png)
