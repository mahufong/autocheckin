"""
 * @2022-05-25 17:43:59
 * @Author       : mahf
 * @LastEditTime: 2022-05-27 17:51:52
 * @FilePath: /epicgames-claimer/test_request.py
 * @Copyright 2022 mahf, All Rights Reserved.
"""
import requests


#new_headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0"}

# new_cookies = {"cf_clearance":"CYnXpnRrogSkt2Iw1nBUgNNDOJH8A1HRVjPzGMz3BXU-1640161760-0-150",
#                 "c_secure_ssl":"eWVhaA==",
#                 "_dd_s":"logs=1&id=24f3aa17-9caf-4de2-a982-aa2f278795fc&created=1653472631289&expire=1653473547515",
#                 "c_secure_uid":"NDkxMTA=",
#                 "c_secure_pass":"07f92cbfd051cea860267f27b3ed9799",
#                 "c_secure_tracker_ssl":"eWVhaA==",
#                 "c_secure_login":"bm9wZQ=="}
# new_headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
#                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#                 "Accept-Language":"zh-CN,zh;q=0.9",
#                 "Cache-Control":"no-cache",
#                 "Connection":"keep-alive",
#                 "Cookie":"cf_clearance=pFT3tPBrpE6OfwEY8TgUoJblXKfFBY65v3lPyykQQ5I-1653643605-0-150",
#                 "Pragma":"no-cache",
#                 "Referer":"https://pt.btschool.club/login.php",
#                 "Sec-Fetch-Dest":"document",
#                 "Sec-Fetch-Mode":"navigate",
#                 "Sec-Fetch-Site":"same-origin",
#                 "Sec-Fetch-User":"?1",
#                 "Upgrade-Insecure-Request":"1",
#                 "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
#                 "sec-ch-ua-mobile":"?0",
#                 "sec-ch-ua-platform":"Windows"}
# #new_cookies = {"cf_clearance":"cf_clearance=xe8POWlFbkZpbAmyBucQTYPWjv6ZlKKwVh0TfZASWfQ-1653637703-0-150"}
new_headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
                "Cookie": "cf_clearance=pFT3tPBrpE6OfwEY8TgUoJblXKfFBY65v3lPyykQQ5I-1653643605-0-150"}

response = requests.post("https://pt.btschool.club/image.php?action=regimage&imagehash=a5f17ec8b7f2b63d669e955c7de5ea68",headers=new_headers)
# response = requests.post("https://pt.btschool.club/login.php",headers=new_headers)

print(response.content)
