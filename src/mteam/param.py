from flask import jsonify
from mteam.util import *
from mteam.const import *
import json


class Param:
    def __init__(self) -> None:
        self.sort_field = None
        self.sort_order = None
        self.mode = None
        self.single_bigger_than = None
        self.single_small_than = None
        self.total_small_than = None
        self.free_left = None
        self.count = None
        self.seeders_less_than = None
        self.seeders_more_than = None
        self.download_more_than = None
        self.download_less_than = None
        self.url_use_https = None
        self.url_type = None

    def parse(self, request):
        self.sort_field = request.args.get("sort_field")
        self.sort_order = request.args.get("sort_order")
        single_bigger_than_str = request.args.get("single_bigger_than")
        single_small_than_str = request.args.get("single_small_than")
        total_small_than_str = request.args.get("total_small_than")
        free_left = request.args.get("free_left")
        count = request.args.get("count")
        seeders_less_than = request.args.get("seeders_less_than")
        seeders_more_than = request.args.get("seeders_more_than")
        download_more_than = request.args.get("download_more_than")
        download_less_than = request.args.get("download_less_than")
        url_use_https = request.args.get("url_use_https")
        url_type = request.args.get("url_type")


        
        if single_bigger_than_str is not None:
            self.single_bigger_than = int(single_bigger_than_str)
        if single_small_than_str is not None:
            self.single_small_than = int(single_small_than_str)
        if total_small_than_str is not None:
            self.total_small_than = int(total_small_than_str)
        if free_left is not None:
            self.free_left = int(free_left)
        if count is not None:   
            self.count = int(count)
        if seeders_less_than is not None:
            self.seeders_less_than = int(seeders_less_than)
        if seeders_more_than is not None:
            self.seeders_more_than = int(seeders_more_than)
        if download_more_than is not None:
            self.download_more_than = int(download_more_than)
        if download_less_than is not None:
            self.download_less_than = int(download_less_than)
        if url_use_https is not None:
            self.url_use_https = url_use_https
        if url_type is not None:
            self.url_type = url_type
        

            
        self.mode = request.args.get("mode")
        if self.sort_field is not None and not is_legal(self.sort_field, Const.SORT_FEILD_LIST):
            return False, 'Invalid sort_field value, avilable:' + ','.join(Const.SORT_FEILD_LIST), 400
        if self.sort_order is not None and not is_legal(self.sort_order, Const.SORT_ORDER_LIST):
            return False, 'Invalid sort_order value, avilable:' + ','.join(Const.SORT_ORDER_LIST), 400
        if self.sort_order is None:
            self.sort_order = "desc"
        if self.mode is not None:
            ok, self.mode = mode_legal(self.mode, Const.MODE_LIST)
            if not ok:
                return False, 'Invalid mode value, avilable:' + Const.MODE_LIST + "or set all.", 400
        else:
            self.mode = Const.MODE_LIST
        if self.url_type is not None and not is_legal(self.url_type, Const.URL_TYPE_LIST):
            return False, 'Invalid url_type value, avilable:' + ','.join(Const.URL_TYPE_LIST), 400
        if self.url_use_https is not None and not is_legal(self.url_use_https, Const.URL_USE_HTTPS_LIST):
            return False, 'Invalid url_use_https value, avilable:true or false', 400

        return True, None, None

