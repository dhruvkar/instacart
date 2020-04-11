import os
import requests

from bs4 import BeautifulSoup as bs

from dotenv import load_dotenv
load_dotenv()



class Instacart(object):
    STORES = {
        "COSTCO":"costco",
        "FRESH_THYME":"fresh-thyme-farmers-market",
        "SCHNUCKS":"schnucks",
        "SAMS_CLUB": "sams-club",
        "SPROUTS": "sprouts",
        "ALDI": "aldi",
        "TARGET": "target",
        "BEVMO": "bevmo",
        "RALPHS": "ralphs",
        "SAFEWAY": "safeway",
        "SMART_FINAL": "smart-final"
        }

    def __init__(self):

        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
        
        #get and parse result for <meta name="csrf-token" content=
        headers0 = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Host": "www.instacart.com",
            "User-Agent":self.user_agent,
            }
        url0 = "https://www.instacart.com/"

        #get - this sets cookies
        headers1 = {
            "Host": "www.instacart.com",
            "User-Agent": self.user_agent,
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.instacart.com/",
            "content-type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "x-client-identifier": "web",
            "X-CSRF-Token": "undefined",
            "Connection": "keep-alive",
            "TE": "Trailers",
            }
        url1 = "https://www.instacart.com/v3/containers/next_gen/authenticate?&source=web&cache_key=undefined"
        
        #post - to login
        data2 = {
                "address":None,
                "authenticity_token":"",
                "email":os.getenv("INSTACART_USERNAME"),
                "grant_type":"password",
                "password":os.getenv("INSTACART_PASSWORD"),
                "scope":"",
                "signup_v3_endpoints_web": None,
                }
        headers2 = {
            "Host": "www.instacart.com",
            "User-Agent": self.user_agent,
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.instacart.com/",
            "content-type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "x-client-identifier": "web",
            "X-CSRF-Token": "undefined",
            "Origin": "https://www.instacart.com",
            "Connection": "keep-alive",
            }
        url2 = "https://www.instacart.com/v3/dynamic_data/authenticate/login?source=web&cache_key=undefined"
       
        self.session = requests.session()

        # get main instacart page
        self.session.headers.update(headers0)
        r0 = self.session.get(url0)

        # get csrf-token for later
        soup0 = bs(r0.content, "lxml")
        metas = soup0.find_all("meta")
        for meta in metas:
            try:
                if meta.attrs["name"] == "csrf-token":
                    data2["authenticity_token"] = meta.attrs["content"]
            except KeyError:
                pass

        # set proper cookies
        self.session.headers.update(headers1)
        r1 = self.session.get(url1)

        # post to login
        self.session.headers.update(headers2)
        r2 = self.session.post(url2, json=data2)


    def check_delivery_times(self, store):
        headers = {
            "Host": "www.instacart.com",
            "User-Agent": self.user_agent,
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.instacart.com/store/{0}/info?tab=delivery".format(store),
            "content-type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "x-client-identifier": "web",
            "Connection": "keep-alive",
            "TE": "Trailers",
            }
        url = "https://www.instacart.com/v3/containers/{0}/next_gen/retailer_information/content/delivery".format(store)

        ## then check containers -> modules -> data.

        self.session.headers.update(headers)
        r = self.session.get(url)
        self.raw = r
        if len(r.json()["container"]["modules"]) == 1:
            try:
                print (r.json()["container"]["modules"][0]["data"]["title"])
            except KeyError:
                print ("Delivery times might be available")
        elif len(r.json()["container"]["modules"]) == 2:
            os.system("mutt -s 'delivery available at {0}!' {1} < /dev/null".format(store, os.getenv("NOTIFICATION_EMAIL")))
            av_days = r.json()["container"]["modules"][1]["data"]["service_options"]["service_options"]["days"]
            for ad in av_days:
                options = ad["options"]
                for option in options:
                    print (option["delivery_full_window"])
