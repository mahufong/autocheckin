import requests
import aiohttp
from loguru import logger
import asyncio
import time
from lxml import etree

class ProxyFlare(object):
    """代理 用于过cloudflare
        使用flareovererr实现

        使用async with 保证对资源进行销毁
        若不使用  请确保  proxy_strat 和 proxy_close的执行
    """

    def __init__(self, url: str):
        self.__url = url
        self.__uuid_list = []
        self.__session = None

    async def proxy_cmd(self, cmd: str, uuid: str = None) -> dict:
        """
            代理常用命令
        :param self (None):
        :param cmd (str): option[sessions.create,sessions.list,sessions.destroy]
        :param uuid (str):

        :return (None):
        Examples:
        Note:
        """

        async with self.__session.post(self.__url, json={"cmd": cmd, "session": uuid}) as resp:
            if resp.status == 200:
                logger.info(f'{cmd} succeed \n{await resp.json()}')
                ret = await resp.json()
                return ret
            else:
                logger.warning(f'cmd failed {resp.status}')
                return

    @logger.catch()
    async def proxy_get(self, url: str, uuid: str = None):
        """
                代理get请求
        :param self (None):
        :param url (str):
        :param uuid (str): 会话id

        :return (None): status,headers,response
        Examples:
        Note:
        """
        body = {"cmd": "request.get", "url": url}
        if uuid:
            body['session'] = uuid
        async with self.__session.post(self.__url, json=body) as resp:
            logger.info(f"get : {url}")
            if resp.status == 200:
                ret = await resp.json()
                logger.info(f'get  succeed \n{ret}')
                return ret['solution']
            else:
                logger.warning(f'get failed {resp.status}')
                return

    @logger.catch()
    async def proxy_post(self, url: str, data: dict, uuid: str = None):
        """
                代理post请求
        :param self (None):
        :param url (str):
        :param data (dict): 
        :param uuid (str):

        :return (None):
        Examples:
        Note: 当uuid为空时 代理自动创建 并在结束时销毁
        """
        strdata = ''
        strlist = []
        for key, value in data.items():
            strlist.append(f'{key}={value}')
        strdata = '&'.join(strlist)

        body = {"cmd": "request.post", "url": url, "postData": strdata}
        if uuid:
            body["session"] = uuid

        async with self.__session.post(self.__url, json=body) as resp:
            logger.info(f"post : {url}\n data : {strdata}")
            if resp.status == 200:
                ret = await resp.json()
                logger.info(f'post succeed \n{ret}')
                return ret['solution']
            else:
                logger.warning(f'post failed {resp.status}')
                return

    async def proxy_session_add(self):
        """
                增加一个代理会话 
        :param self (None):

        :return (None):
        Examples:
        Note:
        """
        uuid = str(int(round(time.time() * 1000)))
        if await self.proxy_cmd("sessions.create", uuid):
            self.__uuid_list.append(uuid)
            logger.info(f'session add , uuid : {uuid}')
            return uuid
        else:
            logger.info(f'session add failef , uuid : {uuid}')
            return

    async def proxy_session_delete(self, uuid: str):
        """
                删除一个代理会话
        :param self (None):
        :param uuid (str):

        :return (None):
        Examples:
        Note:
        """
        if await self.proxy_cmd('sessions.destroy', uuid):
            if uuid in self.__uuid_list:
                self.__uuid_list.remove(uuid)
                logger.info(f'session delete , uuid : {uuid}')
                return uuid
        else:
            logger.info(f'session delete failed , uuid : {uuid}')
            return

    async def proxy_session_destroy(self):
        """
                删除所有代理会话
        :param self (None):

        :return (None):
        Examples:
        Note:
        """
        logger.info('session destroy')
        ret = await self.proxy_cmd('sessions.list')
        session_list = ret.get('sessions', [])
        logger.info(f'session list : {session_list}')
        for item in session_list:
            await self.proxy_session_delete(item)

    async def proxy_start(self):
        """
                启动代理
        :param self (None):

        :return (None):
        Examples:
        Note: 要使用代理一定要先启动
        """
        if self.__session is None:
            logger.info('proxy start')
            self.__session = aiohttp.ClientSession()

    async def proxy_close(self):
        """
                关闭代理
        :param self (None):

        :return (None):
        Examples:
        Note:会删除所有会话
        """

        logger.info('proxy close')
        for item in self.__uuid_list:
            await self.proxy_session_delete(item)
        await self.proxy_session_destroy()
        await self.__session.close()


async def test():
    # async with ProxyFlare('http://127.0.0.1:8191/v1', '123456') as proxy:
    #     logger.info('test')
    proxy = ProxyFlare('http://127.0.0.1:8191/v1')
    await proxy.proxy_start()
    url = "https://kp.m-team.cc"
    ret = await proxy.proxy_get(url)
    if ret:
        cookies = ret['cookies']
        logger.info(f"cookies : {cookies}")
        cook = cookies[0]["name"] + '=' + cookies[0]["value"]
        logger.info(f"cook {cook}")

        headers = {'User-Agent': ret["userAgent"],
                    "Cookie":cook}
        new_headers = {"User-Agent":ret["userAgent"],
               "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Language":"zh-CN,zh;q=0.9",
                "Cache-Control":"no-cache",
                "Connection":"keep-alive",
                "Cookie":cook,
                "Pragma":"no-cache",
                "Referer":"https://pt.btschool.club/login.php",
                "Sec-Fetch-Dest":"document",
                "Sec-Fetch-Mode":"navigate",
                "Sec-Fetch-Site":"same-origin",
                "Sec-Fetch-User":"?1",
                "Upgrade-Insecure-Request":"1",
                "sec-ch-ua-mobile":"?0",
                "sec-ch-ua-platform":"Windows"}

        logger.info(f"headwes : {new_headers}")
        
        # html = etree.HTML(ret['response'])
        # image_url = html.xpath("//td[@align='left']/img/@src")
        # image_url = url + image_url[0]
        # logger.info(f'image url {image_url}')

        
        logger.warning(response.url)  # 打印响应的url
        logger.warning(response.status_code)  # 打印响应的状态码
        logger.warning(response.request.headers)  # 打印响应对象的请求头
        logger.warning(response.headers)  # 打印响应头
        logger.warning(response.request._cookies)  # 打印请求携带的cookies
        logger.warning(response.cookies)  # 打印响应中携带的cookies
        image = response.content
        with open('captcha.png', 'wb') as file:
            file.write(image)


    # await proxy.proxy_close()

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
    loop.close()
