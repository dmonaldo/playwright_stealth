from playwright import async_api


class AsyncHookedBrowserType(async_api.BrowserType):
    pass

class AsyncHookedPlaywright(async_api.Playwright):
    chromium: AsyncHookedBrowserType
    firefox: AsyncHookedBrowserType
    webkit: AsyncHookedBrowserType
