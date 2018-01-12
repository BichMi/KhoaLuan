# -*- coding: utf-8 -*-
from scrapy import Spider
import requests
import json
from scrapy.utils.response import open_in_browser


class Airline(Spider):
    name = "SearchAirline"
    download_delay = 5.0
    allowed_domains = ['https://vietjets.com.vn/flight/search?session=1122171013']
    start_urls = ['https://vietjets.com.vn/flight/search?session=1122171013']

    def parse(self, response):
        #open_in_browser(response)
        request = requests.get('https://vietjets.com.vn/flight/search?session=2043220430')
        header = {
            'Host': 'https://vietjets.com.vn/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://vietjets.com.vn/',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': '174',
            'Cookie':str(request.cookies),
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

        formdata = {'flightType': '0', 'depAirport': 'TP.Hồ+Chí+Minh+(SGN)', 'arvAirport': 'Hải+Phòng+(HPH)',
                    'depDate': '09/01/2018', 'adultNo': '1', 'childNo': '0', 'infantNo': '0', 'rdoTravelPref': 'on'}
        request = requests.post('https://vietjets.com.vn/flight/search?session=1122171013', headers=header, data=formdata, callback=self.parse_item())

        jsoncontent = json.loads(request.content)

    def parse_item(self, response):
        flights = response.xpath('//*[@id="DataTables_Table_0"]/tbody/tr/td[2]/text()').extract()
        date_gos = response.xpath('//*[@id="DataTables_Table_0"]/tbody/tr/td[3]/text()').extract()
        date_backs = response.xpath('//*[@id="DataTables_Table_0"]/tbody/tr/td[4]/text()').extract()
        prices = response.xpath('//*[@id="DataTables_Table_0"]/tbody/tr/td[6]/span/text()').extract()
        for item in zip(flights, date_gos, date_backs, prices):
            data = {
                'flight' : item[0],
                'date_go': item[1],
                'date_back': item[2],
                'price': item[3],
            }
            yield data
            

