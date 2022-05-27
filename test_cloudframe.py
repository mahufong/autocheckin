"""
 * @2022-04-24 17:29:10
 * @Author       : mahf
 * @LastEditTime : 2022-04-24 17:31:33
 * @FilePath     : /epicgames-claimer/test_cloudframe.py
 * @Copyright 2022 mahf, All Rights Reserved.
"""
import cloudscraper

scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
# Or: scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
print(scraper.get("https://pt.btschool.club").text)  # => "<!DOCTYPE html><html><head>..."