from .m_team_config import MTeamConfig
from .const import Const
from . import util
import requests
import json
import asyncio
import aiohttp
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone
import pytz
import logging
from util.log import log

logger = log()

class MTeam:
    def __init__(self, config: MTeamConfig):
        self.config = config

    async def search(self, pageNumber: int, pageSize: int, keyword: str, sortField: str, discount: str, sortDirection: str, mode: str):
        header = {
            "Content-Type": "application/json",
            "x-api-key": self.config.x_api_key
        }
        body = {
            "pageNumber": pageNumber,
            "pageSize": pageSize,
            "keyword": keyword,
            "sortField": sortField,
            "discount": discount,
            "sortDirection": sortDirection,
            "mode": mode
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(Const.M_TEAM_HOST + "/api/torrent/search", headers=header, data=json.dumps(body)) as response:
                    if response.status == 200:
                        logger.info(f"search {mode} success.")
                        result_str = await response.text()
                        result = json.loads(result_str)
                        if result["message"].upper() == "SUCCESS":
                            return result["data"]
                        else:
                            logger.error(f"Search error:{response.text}")
                            return None
                    else:
                        logger.error(f"Search error：{response.status_code}")
                        return None
        except aiohttp.ClientError:
            logger.error("Connect timeout, please check net or server condition.")
            return None
        except asyncio.TimeoutError as e:
            logger.error(f"Search error：{e}")
            return None
    
    def get_active_top(self, param):
        results_queue = asyncio.Queue()
        asyncio.run(self.gather_search_result(param, results_queue))
        search_result = []
        while not results_queue.empty():
              search_result.extend(results_queue.get_nowait()["data"]) 
        result = self.parse_search_content(search_result)
        result = self.filter(result, param)
        asyncio.run(self.set_di_token(result))
        return result
    
    
    async def gather_search_result(self, param, results_queue):
        tasks = []
        search_result = []
        for mode_item in param.mode:
            task = asyncio.create_task(self.search(1, 100, Const.SEARCH_KEY, "LEECHERS", "FREE", "DESC", mode_item))
            tasks.append(task)
        await asyncio.gather(*tasks)
        for task in tasks:
            if not task.exception():
                await results_queue.put(task.result())
        
    def filter(self, data, param):
        if param.single_bigger_than is not None:
            data = list(filter(lambda x: int(x["size"]) >= param.single_bigger_than * 1024**3 , data))
        
        if param.single_small_than is not None:
            data = list(filter(lambda x: int(x["size"]) <= param.single_small_than * 1024**3 , data))
        
        if param.total_small_than is not None:
            # sort by size 
            data = sorted(data, key=lambda x: int(x["size"]))
            result = []
            total_size = 0
            for item in data:
                if int(item['size']) + total_size < param.total_small_than * 1024**3:
                    result.append(item) 
                    total_size += int(item['size'])
                else:
                    break
            data = result
        
        if param.free_left is not None:
            current_time = datetime.now()
            data = list(filter(lambda x: self.__get_free_left(x) > param.free_left * 3600, data))
        
        if param.sort_field is not None:
            if param.sort_field == "date":
                data = sorted(data, key=lambda x: datetime.strptime(x["createdDate"], "%Y-%m-%d %H:%M:%S"), reverse=(param.sort_order != "desc"))
            elif param.sort_field == "size":
                data = sorted(data, key=lambda x: int(x["size"]), reverse=(param.sort_order != "desc"))
        if param.count is not None:
            data = data[:param.count]
        unique_dict = {item["id"]: item for item in data}
        data = list(unique_dict.values())

        return data
    def __get_free_left(self, data):
        return (datetime.strptime(data['status']["discountEndTime"], "%Y-%m-%d %H:%M:%S") - datetime.now()).total_seconds()
             
    def parse_search_content(self, search_data):
        result = []
        max_num = -1
        for item in search_data:
            if item["status"]["toppingLevel"] == 1:
                #  only topping
                active_num = self.parse_num(item["smallDescr"])
                item["active_num"] = active_num
                if active_num > max_num:
                    max_num = active_num
                # convert byte to gb
                try:
                    size = int(item["size"])
                    item["sizeGb"] = util.bytes_to_gb(size)
                except ValueError:
                    logger.error(f"Can't convert size {size}")
                    continue
                result.append(item)
        return list(filter(lambda x: x["active_num"] == max_num, result))
    
    def parse_num(self, content: str):
        parts = content.split(Const.SEARCH_KEY)
        second_part = parts[1].split("*")
        try:
            return int(second_part[0])
        except ValueError:
            return -1
        
    def get_category_list(self):
        header = {
            "Content-Type": "application/json",
            "x-api-key": self.config.x_api_key
        }
        try:
            response = requests.post(Const.M_TEAM_HOST + "/api/torrent/categoryList", headers=header)
            if response.status_code == 200:
                logger.info("Get category success.")
                result_str = response.text
                result = json.loads(result_str)
                if result["message"].upper() == "SUCCESS":
                   data = result["data"]["list"]
                   return dict(map(lambda x: (x["id"], x["nameEng"]), data))
                else:
                   logger.error(f"Get category error:{response.text}")
                   return {}
            else:
                logger.error(f"Get category error：{response.status_code}")
                return {}
        except requests.exceptions.Timeout:
            logger.error("Connect timeout, please check internet or server condition.")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Search error：{e}")
            return None
        
    async def set_di_token(self, data):
        tasks = []
        for item in data:
            task = asyncio.create_task(self.__get_di_token(item["id"]))
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        for result in results:
            id = result[0]
            di_token = result[1]
            matching_elements = list(filter(lambda x: x["id"] == id, data))
            if matching_elements is not None:
                matching_elements[0]["di_token"] = di_token
        
        
    async def __get_di_token(self, id:str):
        header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "x-api-key": self.config.x_api_key
        }
        data = {
            "id":  id
        }
        try:
             async with aiohttp.ClientSession() as session:
                 async with session.post(Const.M_TEAM_HOST + "/api/torrent/genDlToken", headers=header, data=data) as response:
                    if response.status == 200:
                        logger.info("getDiToken success.")
                        result_str = await response.text()
                        result = json.loads(result_str)
                        if result["message"].upper() == "SUCCESS":
                            return id, result["data"]
                        else:
                            logger.error(f"getDiToken error:{response.text}")
                            return id, None
                    else:
                        logger.error(f"getDiToken error：{response.status}")
                        return id, None
        except aiohttp.ClientError:
            logger.error("Connect timeout, please check internet or server condition.")
            return id, None
        except asyncio.TimeoutError as e:
            logger.error(f"Search error：{e}")
            return id, None
    
    def generate_rss(self, param):
        data = self.get_active_top(param)
        categroy_map = self.get_category_list()
        fg = FeedGenerator()
        fg.title("M-Team - TP Torrents")
        fg.link(href=Const.M_TEAM_HOST)
        fg.description("Active top torrent From M-Team, power by mteam-active-top-rss")
        for item in data:
            fe = fg.add_entry()
            fe.title(title=item["name"])
            fe.link(href=(Const.TORRENT_PREFIX + item["id"]))
            fe.description(item["smallDescr"])
            fe.enclosure(url=item["di_token"], length=item["size"], type="application/x-bittorrent")
            category = item["category"]
            fe.category(label=categroy_map[category], term=Const.CATEGORY_PREFIX + category)
            created_date = datetime.strptime(item["createdDate"], "%Y-%m-%d %H:%M:%S")
            tz = pytz.timezone('Asia/Shanghai')
            created_date_tz = tz.localize(created_date)
            fe.pubDate(pubDate=created_date_tz)
            fe.comments(Const.TORRENT_PREFIX + item["id"] + "#comment")
            fe.guid(item["id"], permalink=False)
            
        rss_str = fg.rss_str(pretty=True, encoding='utf-8')
        return rss_str.decode('utf-8')
        

