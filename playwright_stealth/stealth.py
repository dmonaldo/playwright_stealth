# -*- coding: utf-8 -*-
import inspect
import json
import re
import warnings
from collections.abc import Callable
from copy import deepcopy
from pathlib import Path
from typing import Dict, List, Union, Any

from playwright import async_api, sync_api

from playwright_stealth.context_managers import AsyncWrappingContextManager, SyncWrappingContextManager


def from_file(name) -> str:
    return (Path(__file__).parent / "js" / name).read_text()


SCRIPTS: Dict[str, str] = {
    "generate_magic_arrays": from_file("generate.magic.arrays.js"),
    "utils": from_file("utils.js"),
    "chrome_app": from_file("mitigations/chrome.app.js"),
    "chrome_csi": from_file("mitigations/chrome.csi.js"),
    "chrome_hairline": from_file("mitigations/chrome.hairline.js"),
    "chrome_load_times": from_file("mitigations/chrome.load.times.js"),
    "chrome_runtime": from_file("mitigations/chrome.runtime.js"),
    "iframe_content_window": from_file("mitigations/iframe.contentWindow.js"),
    "media_codecs": from_file("mitigations/media.codecs.js"),
    "navigator_hardware_concurrency": from_file("mitigations/navigator.hardwareConcurrency.js"),
    "navigator_languages": from_file("mitigations/navigator.languages.js"),
    "navigator_permissions": from_file("mitigations/navigator.permissions.js"),
    "navigator_platform": from_file("mitigations/navigator.platform.js"),
    "navigator_plugins": from_file("mitigations/navigator.plugins.js"),
    "navigator_user_agent": from_file("mitigations/navigator.userAgent.js"),
    "navigator_vendor": from_file("mitigations/navigator.vendor.js"),
    "navigator_webdriver": from_file("mitigations/navigator.webdriver.js"),
    "webgl_vendor": from_file("mitigations/webgl.vendor.js"),
}

from typing import Tuple, Optional


class Stealth:
    """
    Playwright stealth configuration that applies stealth strategies to playwright page objects.
    The stealth strategies are contained in ./js package and are basic javascript scripts that are executed
    on every page.goto() called.
    Note:
        All init scripts are combined by playwright into one script and then executed this means
        the scripts should not have conflicting constants/variables etc. !
        This also means scripts can be extended by overriding enabled_scripts generator:
        ```
        @property
        def enabled_scripts():
            yield 'console.log("first script")'
            yield from super().enabled_scripts()
            yield 'console.log("last script")'
        ```
    """

    def __init__(
            self,
            navigator_webdriver: bool = True,
            webgl_vendor: bool = True,
            chrome_app: bool = True,
            chrome_csi: bool = True,
            chrome_load_times: bool = True,
            chrome_runtime: bool = False,
            iframe_content_window: bool = True,
            media_codecs: bool = True,
            navigator_hardware_concurrency: bool = True,
            navigator_languages: bool = True,
            navigator_permissions: bool = True,
            navigator_platform: bool = True,
            navigator_plugins: bool = True,
            navigator_user_agent: bool = True,
            navigator_vendor: bool = True,
            hairline: bool = True,
            webgl_vendor_override: str = "Intel Inc.",
            webgl_renderer_override: str = "Intel Iris OpenGL Engine",
            navigator_vendor_override: str = "Google Inc.",
            navigator_user_agent_override: Optional[str] = None,
            navigator_platform_override: Optional[str] = None,
            navigator_languages_override: Tuple[str, str] = ("en-US", "en"),
            chrome_runtime_run_on_insecure_origins: bool = False,
            init_scripts_only: bool = False,
            script_logging: bool = False,
    ):
        # scripts to load
        self.navigator_webdriver: bool = navigator_webdriver
        self.webgl_vendor: bool = webgl_vendor
        self.chrome_app: bool = chrome_app
        self.chrome_csi: bool = chrome_csi
        self.chrome_load_times: bool = chrome_load_times
        self.chrome_runtime: bool = chrome_runtime
        self.iframe_content_window: bool = iframe_content_window
        self.media_codecs: bool = media_codecs
        self.navigator_hardware_concurrency: int = navigator_hardware_concurrency
        self.navigator_languages: bool = navigator_languages
        self.navigator_permissions: bool = navigator_permissions
        self.navigator_platform: bool = navigator_platform
        self.navigator_plugins: bool = navigator_plugins
        self.navigator_user_agent: bool = navigator_user_agent
        self.navigator_vendor: bool = navigator_vendor
        self.hairline: bool = hairline

        # options
        self.webgl_vendor_override: str = webgl_vendor_override
        self.webgl_renderer_override: str = webgl_renderer_override
        self.navigator_vendor_override: str = navigator_vendor_override
        self.navigator_user_agent_override: Optional[str] = navigator_user_agent_override
        self.navigator_platform_override: Optional[str] = navigator_platform_override
        self.navigator_languages_override: Tuple[str, str] = navigator_languages_override
        self.chrome_runtime_run_on_insecure_origins: Optional[bool] = chrome_runtime_run_on_insecure_origins
        self.init_scripts_only: bool = init_scripts_only
        self.script_logging = script_logging

    @property
    def script_payload(self) -> str:
        """
        Returns:
            enabled scripts in an immediately invoked function expression
        """
        return "(() => {\n" + "\n".join(self.enabled_scripts) + "\n})();"

    @property
    def options_payload(self) -> str:
        opts = {
            "chrome_runtime_run_on_insecure_origins": self.chrome_runtime_run_on_insecure_origins,
            "navigator_hardware_concurrency": self.navigator_hardware_concurrency,
            "navigator_languages_override": self.navigator_languages_override,
            "navigator_platform": self.navigator_platform_override,
            "navigator_user_agent": self.navigator_user_agent_override,
            "navigator_vendor": self.navigator_vendor_override,
            "webgl_renderer": self.webgl_renderer_override,
            "webgl_vendor": self.webgl_vendor_override,
            "script_logging": self.script_logging,
        }
        return f"const opts = {json.dumps(opts)};"

    @property
    def enabled_scripts(self):
        yield self.options_payload
        # init utils and generate_magic_arrays helper
        yield SCRIPTS["utils"]
        yield SCRIPTS["generate_magic_arrays"]

        if self.chrome_app:
            yield SCRIPTS["chrome_app"]
        if self.chrome_csi:
            yield SCRIPTS["chrome_csi"]
        if self.hairline:
            yield SCRIPTS["chrome_hairline"]
        if self.chrome_load_times:
            yield SCRIPTS["chrome_load_times"]
        if self.chrome_runtime:
            yield SCRIPTS["chrome_runtime"]
        if self.iframe_content_window:
            yield SCRIPTS["iframe_content_window"]
        if self.media_codecs:
            yield SCRIPTS["media_codecs"]
        if self.navigator_languages:
            yield SCRIPTS["navigator_languages"]
        if self.navigator_permissions:
            yield SCRIPTS["navigator_permissions"]
        if self.navigator_platform:
            yield SCRIPTS["navigator_platform"]
        if self.navigator_plugins:
            yield SCRIPTS["navigator_plugins"]
        if self.navigator_user_agent:
            yield SCRIPTS["navigator_user_agent"]
        if self.navigator_vendor:
            yield SCRIPTS["navigator_vendor"]
        if self.navigator_webdriver:
            yield SCRIPTS["navigator_webdriver"]
        if self.webgl_vendor:
            yield SCRIPTS["webgl_vendor"]

    def use_async(self, ctx: async_api.PlaywrightContextManager) -> AsyncWrappingContextManager:
        """
        Instruments the playwright context manager.
        Any browser connected to or any page created with any method from
        the patched context should have stealth mitigations applied automatically.

        async with Stealth().use_async(async_playwright()) as p:
            ...
        """
        return AsyncWrappingContextManager(self, ctx)

    def use_sync(self, ctx: sync_api.PlaywrightContextManager) -> SyncWrappingContextManager:
        """
        Instruments the playwright context manager.
        Any browser connected to or any page created with any method from
        the patched context should have stealth mitigations applied automatically.

        with Stealth().use_sync(sync_playwright()) as p:
            ...
        """
        return SyncWrappingContextManager(self, ctx)

    async def apply_stealth_async(self, page_or_context: Union[async_api.Page, async_api.BrowserContext]) -> None:
        await page_or_context.add_init_script(self.script_payload)

    def stealth_sync(self, page_or_context: Union[sync_api.Page, sync_api.BrowserContext]) -> None:
        page_or_context.add_init_script(self.script_payload)

    def _kwargs_with_patched_cli_arg(self, method: Callable, packed_kwargs: Dict[str, Any], chromium_mode: bool) -> \
            Dict[str, Any]:
        signature = inspect.signature(method).parameters
        args_parameter = signature.get("args")

        # deep just in case
        new_kwargs = deepcopy(packed_kwargs)
        if args_parameter is not None:
            if chromium_mode and not self.init_scripts_only:
                new_cli_args = new_kwargs.get("args", args_parameter.default)
                if self.navigator_webdriver:
                    new_cli_args = self._patch_blink_features_cli_args(new_cli_args or [])
                if self.navigator_languages:
                    languages_cli_flag = f"--accept-lang={','.join(self.navigator_languages_override)}"
                    new_cli_args = self._patch_cli_arg(new_cli_args or [], languages_cli_flag)
                new_kwargs["args"] = new_cli_args
        return new_kwargs

    def hook_playwright_context(self, ctx: Union[async_api.Playwright, sync_api.Playwright]) -> None:
        """
        Given a Playwright context object, hooks all the browser type object methods that return a Browser object.
        Can be used with sync and async methods contexts
        """
        for browser_type in (ctx.chromium, ctx.firefox, ctx.webkit):
            for name, method in inspect.getmembers(browser_type, predicate=inspect.ismethod):
                if method.__annotations__.get('return') in ("Browser", "BrowserContext"):
                    chromium_mode = browser_type.name == "chromium"
                    method = self._generate_hooked_method_that_returns_browser(method, chromium_mode)
                    setattr(browser_type, name, method)

    def _generate_hooked_method_that_returns_browser(self, method: Callable, chromium_mode: bool):
        async def async_hooked_method(*args, **kwargs):
            browser_or_context = await method(*args, **self._kwargs_with_patched_cli_arg(method, kwargs, chromium_mode))
            if isinstance(browser_or_context, async_api.BrowserContext):
                context: async_api.BrowserContext = browser_or_context
                context.new_page = self._generate_hooked_new_page(context.new_page)
            elif isinstance(browser_or_context, async_api.Browser):
                browser: async_api.Browser = browser_or_context
                browser.new_page = self._generate_hooked_new_page(browser.new_page)
                browser.new_context = self._generate_hooked_new_context(browser.new_context)
            else:
                raise TypeError(f"unexpected type from function (bug): {method.__name__} returned {browser_or_context}")

            return browser_or_context

        async def sync_hooked_method(*args, **kwargs):
            browser_or_context = method(*args, **self._kwargs_with_patched_cli_arg(method, kwargs, chromium_mode))
            if isinstance(browser_or_context, sync_api.BrowserContext):
                context: async_api.BrowserContext = browser_or_context
                context.new_page = self._generate_hooked_new_page(context.new_page)
            elif isinstance(browser_or_context, sync_api.Browser):
                browser: async_api.Browser = browser_or_context
                browser.new_page = self._generate_hooked_new_page(browser.new_page)
                browser.new_context = self._generate_hooked_new_context(browser.new_context)
            else:
                raise TypeError(f"unexpected type from function (bug): {method.__name__} returned {browser_or_context}")

        if inspect.iscoroutinefunction(method):
            return async_hooked_method
        return sync_hooked_method

    def _generate_hooked_new_context(self, new_context_method: Callable) -> Callable:
        async def hooked_new_context_async(*args, **kwargs):
            context = await new_context_method(*args, **kwargs)
            context.new_page = self._generate_hooked_new_page(context.new_page)
            return context

        def hooked_browser_method_sync(*args, **kwargs):
            context = new_context_method(*args, **kwargs)
            context.new_page = self._generate_hooked_new_page(context.new_page)
            return context

        if inspect.iscoroutinefunction(new_context_method):
            return hooked_new_context_async
        return hooked_browser_method_sync

    def _generate_hooked_new_page(self, new_page_method: Callable) -> Callable:
        """
        Returns a hooked method (async or sync) for new_page or new_context.
        *args and **kwargs even though these methods may not take any number of arguments,
        we want to preserve accurate stack traces when caller passes args improperly
        """

        async def hooked_browser_method_async(*args, **kwargs):
            page_or_context = await new_page_method(*args, **kwargs)
            await self.apply_stealth_async(page_or_context)
            return page_or_context

        def hooked_browser_method_sync(*args, **kwargs):
            page_or_context = new_page_method(*args, **kwargs)
            self.stealth_sync(page_or_context)
            return page_or_context

        if inspect.iscoroutinefunction(new_page_method):
            return hooked_browser_method_async
        return hooked_browser_method_sync

    @staticmethod
    def _patch_blink_features_cli_args(existing_args: Optional[List[str]]) -> List[str]:
        """Patches CLI args list to disable AutomationControlled blink feature, while preserving other args"""
        new_args = []
        disable_blink_features_prefix = "--disable-blink-features="
        automation_controlled_feature_name = "AutomationControlled"
        for arg in existing_args or []:
            stripped_arg = arg.strip()
            if stripped_arg.startswith(disable_blink_features_prefix):
                if automation_controlled_feature_name not in stripped_arg:
                    stripped_arg += f",{automation_controlled_feature_name}"
                new_args.append(stripped_arg)
            else:
                new_args.append(arg)
        else:  # no break
            # no blink features disabled, no need to be careful how we modify the command line
            new_args.append(f"{disable_blink_features_prefix}{automation_controlled_feature_name}")
        return new_args

    @staticmethod
    def _patch_cli_arg(existing_args: List[str], flag: str) -> List[str]:
        """Patches CLI args list with any arg, warns if the user passed their own value in themselves"""
        new_args = []
        switch_name = re.search("(.*)=?", flag).group(1)
        for arg in existing_args:
            stripped_arg = arg.strip()
            if stripped_arg.startswith(switch_name):
                warnings.warn("playwright-stealth is trying to modify a flag you have set yourself already."
                              f"Either disable the mitigation or don't specify this flag manually {flag=}"
                              f"to avoid this warning. playwright-stealth has overridden your flag")
                new_args.append(flag)
                break
            else:
                new_args.append(arg)
        else:  # no break
            # none of the existing switches overlap with the one we're trying to set
            new_args.append(flag)
        return new_args
