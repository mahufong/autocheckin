"""
 * @2022-04-18 16:35:05
 * @Author       : mahf
 * @LastEditTime : 2022-04-21 13:12:07
 * @FilePath     : /epicgames-claimer/ptcheckin.py
 * @Copyright 2022 mahf, All Rights Reserved.
"""

import asyncio
import os
from urllib import parse

from loguru import logger
import pyppeteer.errors

import captcha
import config_yaml
from browser import Browser


class PtSite(object):
    """
    pt站信息类
    """

    def __init__(self, name: str, **kwarg):
        self.__name = name
        self.__url = kwarg.get('login_url')
        self.__user = kwarg.get('user', None)
        self.__passwd = kwarg.get('passwd', None)
        self.__captcha = kwarg.get('captcha', False)
        self.__checkin = kwarg.get('checkin', False)

    @property
    def name(self):
        return self.__name

    @property
    def url(self):
        return self.__url

    @property
    def user(self):
        return self.__user

    @property
    def passwd(self):
        return self.__passwd

    @property
    def captcha(self):
        return self.__captcha

    @property
    def checkin(self):
        return self.__checkin


class MyPageError(Exception):
    """页面异常类 包含那个page异常"""

    def __init__(self, message, page):
        super().__init__(message,page)
        self.message = message
        self.page = page


class Ptcheckin(Browser):
    """
    pt签到
    """

    def __init__(self, **kwargs):
        kwargs['timeout'] = 60000    # 默认超时设置60秒
        kwargs['data_dir'] = "./data"
        kwargs['save_cookie'] = True
        kwargs['headless'] = False
        kwargs['headless'] = False
        kwargs['sandbox'] = True
        kwargs['browser_args'] = ["--disable-infobars", "--no-first-run"]
        super().__init__(**kwargs)
        self.sem = asyncio.Semaphore(3)
        self.ptsite_list = []
        ptsite_tmp = config_yaml.read_yaml_file('./ptconfig.yaml')
        for item in ptsite_tmp:
            # need = false 则不签到
            if not ptsite_tmp[item].get("need",True) :
                continue
            tmp = dict(ptsite_tmp[item])
            self.ptsite_list.append(PtSite(item, **tmp))
            logger.info(f"pt 站点 {item}")

    async def _is_logined(self, page) -> bool:
        try:
            ret = await self._get_text_async("span.nowrap > a > b", page,30000)
            if ret == 'mahufong':
                return True
            return False
        except pyppeteer.errors.TimeoutError:
            return False

    @Browser._async_auto_retry(3, "some pt site check in failed",raise_error=False)
    async def _login(self, pt_data: PtSite):
        async with self.sem:
            page = None
            try:
                page = await self._navigate_async(pt_data.url, needcookie=True)
                if await self._is_logined(page):
                    logger.info(f"{pt_data.name} 已经登陆")
                    if pt_data.checkin:
                        logger.info(f"{pt_data.name} 开始签到")
                        await self._click_async("#do-attendance", page)
                else:
                    logger.info(f"{pt_data.name} 还没有登录 开始登录")
                    await self._type_async('[name=username]', pt_data.user, page)
                    await self._type_async('[name=password]',  pt_data.passwd, page)
                    if pt_data.captcha:
                        captcha_url = await self._get_property_async('[alt=CAPTCHA]', 'src', page)
                        # 获取验证码 相对地址  转换为绝对地址
                        captcha_url = parse.urljoin(pt_data.url, captcha_url)
                        logger.info(f"captcha url {captcha_url}")
                        cpt = await captcha.captchaSolver(captcha_url)
                        await self._type_async('[name=imagestring]', cpt['code'], page)

                    await self._click_async('[value=登录]', page)
                    if not await self._is_logined(page):
                        raise pyppeteer.errors.TimeoutError("登陆失败")
            except Exception as error:
                # 当出现异常时 关闭页面 重新抛出异常 触发重试
                if not page is None:
                    await page.screenshot(f"{self.screenshot_dir}/{pt_data.name}.png")
                    await page.close()
                raise MyPageError(f"{pt_data.name} 签到失败", page) from error
            domain = self._get_domain(page.url)
            cookie_path = os.path.join(
                self.data_dir, 'cookies', domain+'.json')
            await self._save_cookies_async(cookie_path, page)
            await page.close()

    def login(self):
        tasks = [self._loop.create_task(self._login(ptdata))
                 for ptdata in self.ptsite_list]
        self._loop.run_until_complete(asyncio.wait(tasks))
        self.close_browser()


if __name__ == '__main__':
    pt = Ptcheckin(chromium_path=r'E:\Tools\chrome-win32\chrome.exe')
    pt.login()
