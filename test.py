"""
 * @2021-12-31 16:19:33
 * @Author       : mahf
 * @LastEditTime : 2022-01-25 17:44:31
 * @FilePath     : /epicgames-claimer/test.py
 * @Copyright 2021 mahf, All Rights Reserved.
"""
import os
import asyncio
from pyppeteer import launch
from epicgames_claimer import EpicgamesClaimer

CHROMIUM_PATH = os.path.abspath(r"E:\Tools\chrome-win32\chrome.exe")

cookies_path = "User_Data/Default/test.json"
def main():
    claimer = EpicgamesClaimer(headless=False, sandbox=True, browser_args=["--disable-infobars", "--no-first-run"],chromium_path=r'E:\Tools\chrome-win32\chrome.exe')
    claimer.log("Creating user data, please log in in the browser ...")
    claimer.navigate("https://www.w3school.com.cn/cssref/css_selectors.asp", timeout=0)
    claimer.find("#user[data-component=SignedIn]", timeout=0)
    claimer.save_cookies(cookies_path)
    claimer.log("Login successful")
    claimer.close_browser()
    # print(await page.cookies())
    # await page.screenshot({'path': 'example.png'})
    # await browser.close()

# asyncio.get_event_loop().run_until_complete(main())
main()
asyncio.sleep(20)