"""
 * @2022-03-02 17:04:24
 * @Author       : mahf
 * @LastEditTime : 2022-04-21 12:54:24
 * @FilePath     : /epicgames-claimer/browser.py
 * @Copyright 2022 mahf, All Rights Reserved.
"""
import argparse
import asyncio
# import datetime
import json
import os
import signal
# import sys
import time
# from getpass import getpass
from json.decoder import JSONDecodeError
from typing import Callable, Dict, List, Optional, Tuple, Union
from urllib.parse import urlparse
from loguru import logger

# import schedule
from pyppeteer import launch, launcher
from pyppeteer.element_handle import ElementHandle
from pyppeteer.frame_manager import Frame
from pyppeteer.network_manager import Request
from pyppeteer.page import Page
import pyppeteer.errors

__version__ = "1.0.0"


class Browser(object):
    '''模拟浏览器'''

    def __init__(
        self,
        data_dir: Optional[str] = None,
        headless: bool = True,
        sandbox: bool = False,
        chromium_path: Optional[str] = None,
        #        claimer_notifications: Notifications = None,
        timeout: int = 180000,
        debug: bool = False,
        cookies: str = None,
        browser_args: List[str] = ["--disable-infobars",
                                   "--blink-settings=imagesEnabled=false", "--no-first-run", "--disable-gpu"],
        push_when_owned_all=False,
        save_cookie=True
    ) -> None:
        logger.add('./logs/runtime_{time}.log', retention=10, encoding='utf-8')
        logger.debug("初始化浏览器")
        self.browser = None
        self.data_dir = data_dir
        self.screenshot_dir = os.path.join(self.data_dir,'screenshots')
        self.headless = headless
        self.browser_args = browser_args
        self.sandbox = sandbox
        if not self.sandbox:
            self.browser_args.append("--no-sandbox")
        self.chromium_path = chromium_path
        if "win" in launcher.current_platform() and self.chromium_path is None:
            if os.path.exists("chrome-win32"):
                self.chromium_path = "chrome-win32/chrome.exe"
            elif os.path.exists("chrome-win"):
                self.chromium_path = "chrome-win/chrome.exe"
        self._loop = asyncio.get_event_loop()
        self.browser_opened = False
#       self.claimer_notifications = claimer_notifications if claimer_notifications != None else Notifications()
        self.timeout = timeout
        self.debug = debug
        self.cookies = cookies
        self.save_cookie = save_cookie
        self.push_when_owned_all = push_when_owned_all
        self.page = None  # 默认页
        self.open_browser()
        self.add_quit_signal()

    async def _headless_stealth_async(self, page=None):
        """
        设置无头浏览器 用于隐藏自动化特征
        Args:
            self (None):
            page : 要设置的窗口(网页)
        Returns:
            (None):
        Examples
        Note:
        """
        logger.info("set headless configure")
        if page:
            self.page = page
        original_user_agent = await self.page.evaluate("navigator.userAgent")
        user_agent = original_user_agent.replace("Headless", "")
        await self.page.evaluateOnNewDocument("() => {Object.defineProperty(navigator, 'webdriver', {get: () => false})}")
        await self.page.evaluateOnNewDocument("window.chrome = {'loadTimes': {}, 'csi': {}, 'app': {'isInstalled': false, 'getDetails': {}, 'getIsInstalled': {}, 'installState': {}, 'runningState': {}, 'InstallState': {'DISABLED': 'disabled', 'INSTALLED': 'installed', 'NOT_INSTALLED': 'not_installed'}, 'RunningState': {'CANNOT_RUN': 'cannot_run', 'READY_TO_RUN': 'ready_to_run', 'RUNNING': 'running'}}, 'webstore': {'onDownloadProgress': {'addListener': {}, 'removeListener': {}, 'hasListener': {}, 'hasListeners': {}, 'dispatch': {}}, 'onInstallStageChanged': {'addListener': {}, 'removeListener': {}, 'hasListener': {}, 'hasListeners': {}, 'dispatch': {}}, 'install': {}, 'ErrorCode': {'ABORTED': 'aborted', 'BLACKLISTED': 'blacklisted', 'BLOCKED_BY_POLICY': 'blockedByPolicy', 'ICON_ERROR': 'iconError', 'INSTALL_IN_PROGRESS': 'installInProgress', 'INVALID_ID': 'invalidId', 'INVALID_MANIFEST': 'invalidManifest', 'INVALID_WEBSTORE_RESPONSE': 'invalidWebstoreResponse', 'LAUNCH_FEATURE_DISABLED': 'launchFeatureDisabled', 'LAUNCH_IN_PROGRESS': 'launchInProgress', 'LAUNCH_UNSUPPORTED_EXTENSION_TYPE': 'launchUnsupportedExtensionType', 'MISSING_DEPENDENCIES': 'missingDependencies', 'NOT_PERMITTED': 'notPermitted', 'OTHER_ERROR': 'otherError', 'REQUIREMENT_VIOLATIONS': 'requirementViolations', 'USER_CANCELED': 'userCanceled', 'WEBSTORE_REQUEST_ERROR': 'webstoreRequestError'}, 'InstallStage': {'DOWNLOADING': 'downloading', 'INSTALLING': 'installing'}}}")
        await self.page.evaluateOnNewDocument("() => {Reflect.defineProperty(navigator.connection,'rtt', {get: () => 200, enumerable: true})}")
        await self.page.evaluateOnNewDocument("() => {Object.defineProperty(navigator, 'plugins', {get: () => [{'description': 'Portable Document Format', 'filename': 'internal-pdf-viewer', 'length': 1, 'name': 'Chrome PDF Plugin'}, {'description': '', 'filename': 'mhjfbmdgcfjbbpaeojofohoefgiehjai', 'length': 1, 'name': 'Chromium PDF Viewer'}, {'description': '', 'filename': 'internal-nacl-plugin', 'length': 2, 'name': 'Native Client'}]})}")
        await self.page.evaluateOnNewDocument("() => {const newProto = navigator.__proto__; delete newProto.webdriver; navigator.__proto__ = newProto}")
        await self.page.evaluateOnNewDocument("const getParameter = WebGLRenderingContext.getParameter; WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'Intel Open Source Technology Center';}; if (parameter === 37446) {return 'Mesa DRI Intel(R) Ivybridge Mobile ';}; return getParameter(parameter);}")
        await self.page.evaluateOnNewDocument("() => {Reflect.defineProperty(navigator, 'mimeTypes', {get: () => [{type: 'application/pdf', suffixes: 'pdf', description: '', enabledPlugin: Plugin}, {type: 'application/x-google-chrome-pdf', suffixes: 'pdf', description: 'Portable Document Format', enabledPlugin: Plugin}, {type: 'application/x-nacl', suffixes: '', description: 'Native Client Executable', enabledPlugin: Plugin}, {type: 'application/x-pnacl', suffixes: '', description: 'Portable Native Client Executable', enabledPlugin: Plugin}]})}")
        await self.page.evaluateOnNewDocument("() => {const p = {'defaultRequest': null, 'receiver': null}; Reflect.defineProperty(navigator, 'presentation', {get: () => p})}")
        await self.page.setExtraHTTPHeaders({"Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"})
        await self.page.setUserAgent(user_agent)

    async def _open_browser_async(self) -> None:
        """
        打开浏览器
        Args:
            self (None):
        Returns:
            (None):
        Examples
        Note:
        """
        logger.info("打开浏览器")
        if not self.browser_opened:
            self.browser = await launch(
                options={"args": self.browser_args, "headless": self.headless},
                userDataDir=None if self.data_dir is None else os.path.abspath(
                    self.data_dir),
                executablePath=self.chromium_path,
                defaultViewport={"width": 1366, "height": 768},
                autoClose=False
            )
            self.page = (await self.browser.pages())[0]
            # await self.page.setViewport({"width": 1366, "height": 1000})
            # Async callback functions aren't possible to use (Refer to https://github.com/pyppeteer/pyppeteer/issues/220).
            # await self.page.setRequestInterception(True)
            # self.page.on('request', self._intercept_request_async)
            if self.headless:
                await self._headless_stealth_async()
            self.browser_opened = True
            if self.cookies:
                await self._load_cookies_async(self.cookies)
            # if self.data_dir is not None:
            #     cookies_path = os.path.join(self.data_dir, "cookies.json")
            #     if os.path.exists(cookies_path):
            #         await self._load_cookies_async(cookies_path)
            #         os.remove(cookies_path)
        # await self._refresh_cookies_async()

    async def _refresh_cookies_async(self) -> None:
        """
        刷新cookies        待修改
        Args:
            self (None):
        Returns:
            (None):
        Examples
        Note:
        """
        await self._navigate_async("https://www.epicgames.com/store/en-US/")

    async def _intercept_request_async(self, request: Request) -> None:
        """
        拦截请求           待研究
        Args:
            self (None):
            request (Request):
        Returns:
            (None):
        Examples
        Note:
        """
        if request.resourceType in ["image", "media", "font"]:
            await request.abort()
        else:
            await request.continue_()

    def _get_domain(self, url: str) -> str:
        """
            获取主域名
        Args:
            self (None):
            url (str):
        Returns:
            (None):
        Examples
        Note:
        """
        url = urlparse(url).netloc
        if not url :
            logger.warning('url 是空的')
            return
        url =  url[::-1]
        tmp_str = url.split('.',2)
        domain = tmp_str[1][::-1]
        logger.debug(f'获取主域名 {domain}')
        return domain

    async def _close_browser_async(self):
        """
        关闭浏览器
        Args:
            self (None):
        Returns:
            (None):
        Examples
        Note:
        """
        logger.info("开始关闭浏览器")
        if self.browser_opened:
            if self.save_cookie:
                pages = await self.browser.pages()
                for page in pages:
                    domain = self._get_domain(page.url)
                    if domain is None :
                        continue
                    cookie_path = os.path.join(
                        self.data_dir, 'cookies', domain+'.json')
                    await self._save_cookies_async(cookie_path, page)

            await self.browser.close()
            self.browser_opened = False
        logger.info("浏览器已关闭")

    async def _type_async(self, selector: str, text: str,  page: Page = None, sleep: Union[int, float] = 0) -> None:
        """
        在匹配选择器的元素上键入文本
        Args:
            self (None):
            selector (str):
            text (str):
            page (Page):
            sleep (Union):
        Returns:
            (None):
        Examples
        Note:
        """
        logger.debug(f"键入文本\n{selector}\n{text}")
        if page is None:
            page = self.page
        try:
            await page.waitForSelector(selector)
            await asyncio.sleep(sleep)
            await page.type(selector, text)
        except pyppeteer.errors.TimeoutError:
            logger.warning(f"没有找到选择器 {selector}")

    async def _click_async(self, selector: str, page: Page = None, sleep: Union[int, float] = 2, timeout: int = 30000) -> None:
        """
        点击选择器选择的地方
        Args:
            self (None):
            selector (str):
            page (Page):
            sleep (Union):
            timeout (int):
        Returns:
            (None):
        Examples
        Note:
        """
        logger.debug(f"点击\n{selector}")
        if page is None:
            page = self.page
        try:
            await page.waitForSelector(selector, options={"timeout": timeout})
            await asyncio.sleep(sleep)
            await page.click(selector)
        except pyppeteer.errors.TimeoutError:
            logger.warning(f"没有找到选择器 {selector}")

    async def _get_text_async(self, selector: str, page: Page = None,timeout=10000) -> str:
        """
        返回选择器选择的第一个元素的文本
        Args:
            self (None):
            selector (str):
            page (Page):
        Returns:
            str :
        Examples
        Note: 看代码返回是 dict  text ==> json ==>dict
        """
        if page is None:
            page = self.page
        await page.waitForSelector(selector, options={"timeout": timeout}) 
        ret = await (await (await page.querySelector(selector)).getProperty("textContent")).jsonValue()
        logger.debug(f"获取元素文本\n{selector}\n{ret}")
        return ret

    @logger.catch
    async def _get_texts_async(self, selector: str, page: Page = None) -> List[str]:
        """
        返回选择器选择的多个元素的文本
        Args:
            self (None):
            selector (str):
            page (Page):
        Returns:
            List[str]:
        Examples
        Note:
        """
        if page is None:
            page = self.page
        texts = []
        await page.waitForSelector(selector)
        for element in await page.querySelectorAll(selector):
            texts.append(await (await element.getProperty("textContent")).jsonValue())
        logger.debug(f"获取多个文本\n{selector}\n{texts}")
        return texts

    async def _get_element_text_async(self, element: ElementHandle) -> str:
        """
        返回元素的文本
        Args:
            self (None):
            element (ElementHandle):
        Returns:
            (None):
        Examples
        Note:
        """
        
        ret = await (await element.getProperty("textContent")).jsonValue()
        logger.debug(f"获取元素文本\n{element}\n{ret}")
        return ret

    async def _get_property_async(self, selector: str, proper: str, page: Page = None) -> str:
        """
        返回选择元素属性的值               
        Args:
            self (None):
            selector (str):
            property (str):
        Returns:
            (None):
        Examples
        Note:
        """
        if page is None:
            page = self.page
        await page.waitForSelector(selector, options={"timeout": self.timeout})
        ret =  await page.evaluate("document.querySelector('{}').getAttribute('{}')".format(selector, proper))
        logger.debug(f"获取元素属性\n{selector}\n{proper}\n{ret}")
        return ret

    async def _get_links_async(self, selector: str, filter_selector: str, filter_value: str, page: Page = None) -> List[str]:
        """
        获取选择器选择的元素的内容  这里是url
        Args:
            self (None):
            selector (str):
            filter_selector (str):
            filter_value (str):
        Returns:
            (None):
        Examples
        Note:
        """
        if page is None:
            page = self.page
        links = []
        try:
            await page.waitForSelector(selector)
            elements = await page.querySelectorAll(selector)
            judgement_texts = await self._get_texts_async(filter_selector, page)
        except pyppeteer.errors.TimeoutError:
            return []
        for element, judgement_text in zip(elements, judgement_texts):
            if judgement_text == filter_value:
                link = await (await element.getProperty("href")).jsonValue()
                links.append(link)
        logger.debug(f"获取链接\n{selector}\n{links}")
        return links

    @logger.catch
    async def _find_async(self, selectors: Union[str, List[str]], page: Page = None, timeout: int = None) -> Union[bool, int]:
        """
        寻找某个元素
        Args:
            self (None):
            selectors (Union):
            page (Page):
            timeout (int):
        Returns:
            (None):
        Examples
        Note: 当 selectors是 list 返回找到的第一个元素的下标
        """
        logger.debug(f"寻找元素\n{selectors}")
        if page is None:
            page = self.page
        if isinstance(selectors, str):
            try:
                if timeout is None:
                    timeout = 1000
                await page.waitForSelector(selectors, options={"timeout": timeout})
                return True
            except pyppeteer.errors.TimeoutError:
                return False
        elif isinstance(selectors, list):
            if timeout is None:
                timeout = 300000
            for _ in range(int(timeout / 1000 / len(selectors))):
                for i, item in enumerate(selectors):
                    if await self._find_async(item, page, timeout=1000):
                        return i
            return -1
        else:
            raise ValueError

    async def _try_click_async(self, selector: str, page: Page = None, sleep: Union[int, float] = 2) -> bool:
        """
        等待几秒 然后点击
        Args:
            self (None):
            selector (str):
            sleep (Union):
            float (None):
            frame (Frame):
        Returns:
            (None):
        Examples
        Note:
        """
        logger.debug(f"等待{sleep}秒点击{selector}")
        if page is None:
            page = self.page
        try:
            await asyncio.sleep(sleep)
            await page.click(selector)
            return True
        except pyppeteer.errors.PageError:
            return False

    async def _get_elements_async(self, selector: str, page: Page = None) -> Union[List[ElementHandle], None]:
        """
        获取元素
        Args:
            self (None):
            selector (str):
        Returns:
            (None):
        Examples
        Note:
        """
        logger.debug(f"获取元素{selector}")
        if page is None:
            page = self.page
        try:
            await page.waitForSelector(selector)
            return await page.querySelectorAll(selector)
        except pyppeteer.errors.TimeoutError:
            return None

    async def _wait_for_text_change_async(self, selector: str, text: str, page: Page = None) -> None:
        """
        等待文本改变
        Args:
            self (None):
            selector (str):
            text (str):
        Returns:
            (None):
        Examples
        Note:
        """
        logger.debug(f"等待文本改变\n{selector}\n{text}")
        if page is None:
            page = self.page
        if await self._get_text_async(selector, page) != text:
            return
        for _ in range(int(self.timeout / 1000)):
            await asyncio.sleep(1)
            if await self._get_text_async(selector, page) != text:
                return
        raise TimeoutError("Waiting for \"{}\" text content change failed: timeout {}ms exceeds".format(
            selector, self.timeout))

    async def _wait_for_element_text_change_async(self, element: ElementHandle, text: str) -> None:
        """
                等待文本改变
        Args:
            self (None):
            element (ElementHandle):
            text (str):
            page (Page):
        Returns:
            (None):
        Examples
        Note:
        """
        logger.debug(f"等待文本改变\n{element}\n{text}")
        if await self._get_element_text_async(element) != text:
            return
        for _ in range(int(self.timeout / 1000)):
            await asyncio.sleep(1)
            if await self._get_element_text_async(element) != text:
                return
        raise TimeoutError("Waiting for element \"{}\" text content change failed: timeout {}ms exceeds".format(
            element, self.timeout))

    async def _navigate_async(self, url: str, page: Page = None, needcookie: bool = False, timeout: int = 30000, reload: bool = True) -> Page:
        """
        访问某个网页
        Args:
            self (None):
            url (str):
            page (Page): None时会创建新页面  默认页面传入  self.page
            needcookie (bool):
            timeout (int):
            reload (bool):
        Returns:
            (Page):
        Examples
        Note:
        """
        if page is None:
            logger.info(f"打开新页面 {url}")
            page = await self.browser.newPage()
            if self.headless:
                await self._headless_stealth_async()
            if needcookie:
                domain = self._get_domain(url)
                cookie_path = os.path.join(
                    self.data_dir, "cookies", domain+'.json')
                logger.info(f"需要载入cookie\ncookie_path : {cookie_path}")
                if os.path.exists(cookie_path):
                    await self._load_cookies_async(cookie_path, page)
            try:
                await page.goto(url, options={"timeout": timeout})
            except (pyppeteer.errors.PageError,pyppeteer.errors.TimeoutError) as error:
                await page.close()
                logger.warning("基本页面打开失败 colse page")
                raise error
            return page
        if page.url == url and not reload:
            return page
        await page.goto(url, options={"timeout": timeout})
        return page

    async def _get_json_async(self, url: str, arguments: Dict[str, str] = None, page: Page = None) -> dict:
        """
        获取访问地址返回的json
        Args:
            self (None):
            url (str):
            arguments (Dict):
            page (Page):
        Returns:
            (None):
        Examples
        Note:
        """
        logger.debug(f"获取json {url}")
        if page is None:
            page = self.page
        response_text = await self._get_async(url, arguments, page)
        try:
            response_json = json.loads(response_text)
        except JSONDecodeError:
            response_text_partial = response_text if len(
                response_text) <= 96 else response_text[0:96]
            raise ValueError("Epic Games returnes content that cannot be resolved. Response: {} ...".format(
                response_text_partial)) from JSONDecodeError
        return response_json

    @logger.catch
    def _quit(self, signum=None, frame=None) -> None:
        """
                退出程序
        Args:
            self (None):
            signum (None):
            frame (None):
        Returns:
            (None):
        Examples
        Note:
        """
        self.close_browser()
        exit(1)

    def _screenshot(self, path: str, page: Page = None) -> None:
        """
                截图
        Args:
            self (None):
            path (str):
        Returns:
            (None):
        Examples
        Note:
        """
        if page is None:
            page = self.page
        return self._loop.run_until_complete(page.screenshot({"path": path}))
        #page.screenshot({"path": path})

    async def _post_json_async(self, url: str, data: str, page: Page = None, host: str = "www.epicgames.com", sleep: Union[int, float] = 2):
        """
                在浏览器上执行js-function  用于发送post json请求
        Args:
            self (None):
            url (str):
            data (str):
            host (str):
            sleep (Union):
            float (None):
        Returns:
            (None):
        Examples
        Note:
        """
        if page is None:
            page = self.page
        await asyncio.sleep(sleep)
        if not host in page.url:
            await self._navigate_async("https://{}".format(host), page=page)
        response = await page.evaluate("""
            xmlhttp = new XMLHttpRequest();
            xmlhttp.open("POST", "{}", true);
            xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
            xmlhttp.send('{}');
            xmlhttp.responseText;
        """.format(url, data))
        return response

    async def _post_async(self, url: str, data: dict, page: Page = None, host: str = "www.epicgames.com", sleep: Union[int, float] = 2) -> str:
        """
                发送post请求
        Args:
            self (None):
            url (str):
            data (dict):
            host (str):
            sleep (Union):
            float (None):
        Returns:
            (None):
        Examples
        Note:
        """
        if page is None:
            page = self.page
        await asyncio.sleep(sleep)
        if not host in page.url:
            await self._navigate_async("https://{}".format(host), page=page)
        evaluate_form = "var form = new FormData();\n"
        for key, value in data.items():
            evaluate_form += "form.append(`{}`, `{}`);\n".format(key, value)
        response = await page.evaluate(evaluate_form + """
            var form = new FormData();
            xmlhttp = new XMLHttpRequest();
            xmlhttp.open("POST", `{}`, true);
            xmlhttp.send(form);
            xmlhttp.responseText;
        """.format(url))
        return response

    async def _get_async(self, url: str, arguments: Dict[str, str] = None, page: Page = None, sleep: Union[int, float] = 2):
        """
                发送get请求
        Args:
            self (None):
            url (str):
            arguments (Dict):
            str (None):
            sleep (Union):
            float (None):
        Returns:
            (None):
        Examples
        Note:
        """
        if page is None:
            page = self.page
        args = ""
        if arguments is not None:
            args = "?"
            for key, value in arguments.items():
                args += "{}={}&".format(key, value)
            args = args.rstrip("&")
        await self._navigate_async(url + args, page=page)
        response_text = await self._get_text_async("body", page)
        await asyncio.sleep(sleep)
        return response_text

    async def _screenshot_async(self, path: str, page: Page = None) -> None:
        """
                截图 协程
        Args:
            self (None):
            path (str):
        Returns:
            (None):
        Examples
        Note:
        """
        if page is None:
            page = self.page
        await page.screenshot({"path": path})

    def add_quit_signal(self):
        signal.signal(signal.SIGINT, self._quit)
        signal.signal(signal.SIGTERM, self._quit)
        if "SIGBREAK" in dir(signal):
            signal.signal(signal.SIGBREAK, self._quit)

    @logger.catch
    async def _try_get_webpage_content_async(self, page: Page = None) -> Optional[str]:
        """
                尝试获取 web 内容
        Args:
            self (None):
        Returns:
            (None):
        Examples
        Note:
        """
        if page is None:
            page = self.page

        if self.browser_opened:
            webpage_content = await self._get_text_async('body', page)
            return webpage_content

    @classmethod
    def _async_auto_retry(cls, retries: int, error_message: str, callback: callable=None, raise_error: bool = True) -> None:
        """
                异步重试 装饰器
        Args:
            self (None):
            retries (int):
            error_message (str):
            callback (callable): 失败之后的回调函数
            raise_error (bool):
        Returns:
            (None):
        Examples
        Note:
        """
        def retry(func: Callable) -> Callable:
            async def wrapper(*arg, **kw):
                for i in range(retries):
                    try:
                        await func(*arg, **kw)
                        break
                    except Exception as error:
                        if i < retries - 1:
                            logger.warning(f"{error}")
                        else:
                            logger.warning(f"{error_message}\n{error}")
                            # 这里可以增加发送到微信
                            if callback:
                                callback()

                            if raise_error:
                                raise error
            return wrapper
        return retry

    async def _load_cookies_async(self, path: str, page=None) -> None:
        """
                读取cookies并载入
        Args:
            self (None):
            path (str):
        Returns:
            (None):
        Examples
        Note:
        """
        logger.debug(f"载入cookie \npath : {path}")
        if not os.path.exists(path):
            return
        if page is None:
            page = self.page
        with open(path, "r", encoding="utf-8") as cookies_file:
            cookies = cookies_file.read()
            try:
                for cookie in json.loads(cookies):
                    await page.setCookie(cookie)
            except (JSONDecodeError,TypeError):
                logger.warning("cookies 文件是无效的")

    async def _save_cookies_async(self, path: str, page=None) -> None:
        """
                存储cookies
        Args:
            self (None):
            path (str):
            page (None): 等于 None 说明是 默认页面 page 就是 self.page
        Returns:
            (None):
        Examples
        Note:
        """
        if page is None or page is self.page:
            if self.cookies is None:
                if not self.save_cookie:
                    return
            else:
                page = self.page
                path = self.cookies
        logger.debug(
            f"存储cookie\npath : {path}")
        try:
            cookie_dir = os.path.dirname(path)
            if cookie_dir != "" and not os.path.exists(cookie_dir):
                os.mkdir(cookie_dir)
            with open(path, "w", encoding="utf-8") as cookies_file:
                # await self.page.cookies()
                cookies = await page.cookies()
                cookies_file.write(json.dumps(
                    cookies, separators=(",", ": "), indent=4))
        except OSError as error:
            logger.debug(f"触发 异常{error}")

    async def _sleep_async(self, second: int):
        """
                异步暂停
        Args:
            self (None):
            second (int):
        Returns:
            (None):
        Examples
        Note:
        """
        await asyncio.sleep(second)

    def sleep(self, second: int) -> None:
        return self._loop.run_until_complete(self._sleep_async(second))

    def open_browser(self) -> None:
        return self._loop.run_until_complete(self._open_browser_async())

    def close_browser(self) -> None:
        self._loop.run_until_complete(self._close_browser_async())
        self._loop.close()

    # def scheduled_run(self, at: str, interactive: bool = True, email: str = None, password: str = None, verification_code: str = None, retries: int = 3) -> None:
    #     self.add_quit_signal()
    #     schedule.every().day.at(at).do(self.run_once, interactive,
    #                                    email, password, verification_code, retries)
    #     while True:
    #         schedule.run_pending()
    #         time.sleep(1)

    def load_cookies(self, path: str) -> None:
        return self._loop.run_until_complete(self._load_cookies_async(path))

    def save_cookies(self, path: str) -> None:
        return self._loop.run_until_complete(self._save_cookies_async(path))

    def navigate(self, url: str, timeout: int = 30000, page: Page = None, needcookie: bool = False, reload: bool = True):
        return self._loop.run_until_complete(self._navigate_async(url, page, needcookie,timeout, reload))

    def input_text(self, selector: str, text: str, sleep: Union[int, float] = 0):
        return self._loop.run_until_complete(self._type_async(selector, text, sleep))

    def find(self, selector: str, timeout: int = None, frame: Frame = None) -> bool:
        return self._loop.run_until_complete(self._find_async(selector, timeout, frame))

    async def test_baidu(self):
        page = await self._navigate_async("https://pterclub.com", needcookie=True)
        # await self._type_async("#kw", "我爱罗", page)
        # await self._click_async("#su", page, timeout=10000)
        # await self._find_async("k", page, timeout=3000)
        ret = await self._get_text_async("span > a b :empty",page)
        await self._screenshot_async("./data/ll.png")

    async def test_wait(self):
        # list_task=[asyncio.create_task(self._navigate_async(url)) for url in ["https:www.baidu.com","https://www.google.com","https://www.python.org","https://www.cloudflare.com"]]
        list_task = [asyncio.create_task(self.test_baidu())]

        await asyncio.wait(list_task)

    def test_wait_async(self):
        return self._loop.run_until_complete(self.test_wait())

    def virtual_console(self) -> None:
        print("You can input JavaScript commands here for testing. Type exit and press Enter to quit.")
        while True:
            try:
                command = input("> ")
            except EOFError:
                break
            if command == "exit":
                break
            try:
                result = self._loop.run_until_complete(
                    self.page.evaluate(command))
                print(result)
            except Exception as error:
                print(f"{error}")


def get_args(run_by_main_script: bool = False) -> argparse.Namespace:
    def update_args_from_env(args: argparse.Namespace) -> argparse.Namespace:
        for key in args.__dict__.keys():
            env = os.environ.get(key.upper())
            if env is not None:
                if isinstance(args.__dict__[key],int):
                    args.__setattr__(key, int(env))
                elif isinstance(args.__dict__[key],bool):
                    if env == "true":
                        args.__setattr__(key, True)
                    elif env == "false":
                        args.__setattr__(key, False)
                else:
                    args.__setattr__(key, env)
        return args

    parser = argparse.ArgumentParser(
        description="Claim weekly free games from Epic Games Store.")
    parser.add_argument("-n", "--no-headless",
                        action="store_true", help="run the browser with GUI")
    parser.add_argument("-c", "--chromium-path", type=str,
                        help="set path to browser executable")
    parser.add_argument("-r", "--run-at", type=str,
                        help="set daily check and claim time, format to HH:MM, default to the current time")
    parser.add_argument("-o", "--once", action="store_true",
                        help="claim once then exit")
    if run_by_main_script:
        parser.add_argument("-a", "--auto-update",
                            action="store_true", help="enable auto update")
        parser.add_argument("--cron", type=str, help="set cron expression")
    if not run_by_main_script:
        parser.add_argument("-e", "--external-schedule",
                            action="store_true", help="run in external schedule mode")
    parser.add_argument("-u", "--email", "--username",
                        type=str, help="set username/email")
    parser.add_argument("-p", "--password", type=str, help="set password")
    parser.add_argument("-t", "--verification-code", type=str,
                        help="set verification code (2FA)")
    parser.add_argument("--cookies", type=str, help="set path to cookies file")
    parser.add_argument("-l", "--login", action="store_true",
                        help="create logged-in user data and quit")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="enable debug mode")
    parser.add_argument("-dt", "--debug-timeout", type=int,
                        default=180000, help="set timeout in milliseconds")
    parser.add_argument("-dr", "--debug-retries", type=int,
                        default=3, help="set the number of retries")
    parser.add_argument("-dp", "--debug-push-test", action="store_true",
                        help="Push a notification for testing and quit")
    parser.add_argument("-ds", "--debug-show-args", action="store_true",
                        help="Push a notification for testing and quit")
    parser.add_argument("--push-lang", type=str, default="zh",
                        help="set notifications language")
    parser.add_argument("-ps", "--push-serverchan-sendkey",
                        type=str, help="set ServerChan sendkey")
    parser.add_argument("-pbu", "--push-bark-url", type=str,
                        default="https://api.day.app/push", help="set Bark server address")
    parser.add_argument("-pbk", "--push-bark-device-key",
                        type=str, help="set Bark device key")
    parser.add_argument("-ptt", "--push-telegram-bot-token",
                        type=str, help="set Telegram bot token")
    parser.add_argument("-pti", "--push-telegram-chat-id",
                        type=str, help="set Telegram chat ID")
    parser.add_argument("-pwx", "--push-wechat-qywx-am",
                        type=str, help="set WeChat QYWX")
    parser.add_argument("-pda", "--push-dingtalk-access-token",
                        type=str, help="set DingTalk access token")
    parser.add_argument("-pds", "--push-dingtalk-secret",
                        type=str, help="set DingTalk secret")
    parser.add_argument("-ns", "--no-startup-notification", action="store_true",
                        help="disable pushing a notification at startup")
    parser.add_argument("--push-when-owned-all", action="store_true",
                        help="push a notification when all available weekly free games are already in the library")
    parser.add_argument("-v", "--version", action="version",
                        version=__version__, help="print version information and quit")
    args = parser.parse_args()
    args = update_args_from_env(args)
    global local_texts
    if args.push_lang:
        local_texts = eval("texts." + args.push_lang)
    localtime = time.localtime()
    if run_by_main_script:
        if args.cron is None:
            if args.run_at == None:
                args.cron = "{0:02d} {1:02d} * * *".format(
                    localtime.tm_min, localtime.tm_hour)
            else:
                hour, minute = args.run_at.split(":")
                args.cron = "{0} {1} * * *".format(minute, hour)
    if args.run_at == None:
        args.run_at = "{0:02d}:{1:02d}".format(
            localtime.tm_hour, localtime.tm_min)
    if args.email != None and args.password == None:
        raise ValueError("Must input both username and password.")
    if args.email == None and args.password != None:
        raise ValueError("Must input both username and password.")
    args.interactive = True if args.email == None else False
    args.data_dir = "User_Data/Default" if args.interactive else "User_Data/{}".format(
        args.email)
    if args.debug_push_test:
        # test_notifications = Notifications(serverchan_sendkey=args.push_serverchan_sendkey, bark_push_url=args.push_bark_url,
        #                                    bark_device_key=args.push_bark_device_key, telegram_bot_token=args.push_telegram_bot_token, telegram_chat_id=args.push_telegram_chat_id)
        # test_notifications.notify(
        #     local_texts.NOTIFICATION_TITLE_TEST, local_texts.NOTIFICATION_CONTENT_TEST)
        exit()
    if args.debug_show_args:
        print(args)
        exit()
    if args.login:
        # login("User_Data/Default/cookies.json")
        exit()
    return args


if __name__ == "__main__":
    browser = Browser(data_dir="./data", cookies="./data/cookies/baidu.json", save_cookie=True, headless=False, sandbox=True, browser_args=[
                      "--disable-infobars", "--no-first-run"], chromium_path=r'E:\Tools\chrome-win32\chrome.exe')
    # browser.navigate("https://www.baidu.com",page=browser.page)
    # browser.navigate("https://www.google.com",needcookie=True)
    # browser.input_text("#kw", "我喜欢你")
    # browser.find("#sud", timeout=3000)

    # browser.test_wait_async()
    # browser.close_browser()
    # browser.sleep(5)