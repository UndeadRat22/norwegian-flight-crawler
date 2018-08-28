import requests
import re
from pyquery import PyQuery
from FlightInfo import FlightInfo

base_url = "https://www.norwegian.com/us/ipc/availability/avaday"
payload = {
    "D_City" : "OSL", #departure city
    "A_City" : "RIX", #arrival city
    
    "D_Day" : "01", #departure day
    "D_SelectedDay" : "01", #departure day (selected)
    "D_Month" : "201810", #departure year+month
    
    "R_Day" : "01", #return day
    "R_SelectedDay" : "01", #return day (selected)
    "R_Month" : "201810", #return year+month
    
    "IncludeTransit" : "true", # direct(false)/non-direct(true) flights
    "CurrencyCode" : "USD", # currency

    "CabinFareType" : "0", # 0 - LowFare, 1 - LowFare+, 2 - Flex, cheap->expensive

    #other variables that doen't change anything
    "processid" : "2100",
    "rnd" : "100",
    "TripType" : "1",
    
    #other
    "mode" : "ab",
}

def construct_url(url, payload):
    _out = "".join(url)
    if not ("?" in _out):
        _out = _out + "?"
    for key, value in payload.items():
        _out = _out + key + "=" + value + "&"
    return _out

def download_html(url):
    headers = requests.utils.default_headers()
    headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"})
    resp = requests.get(url)
    return resp.content.decode("UTF-8")

def values_from_html(base_query, filters):
    c = base_query
    for fil in filters:
        c = c.find(fil)
    l = []
    for x in c:
        new_query = PyQuery(x)
        l.append(new_query.text())
    return l

if __name__ == "__main__":
    #with open("to_analyze.html", "r") as html_file:
        #_html = html_file.read().encode("UTF-8")
    url = construct_url(base_url, payload)
    #print(url)
    _html = download_html(url)
    parser = PyQuery(_html).find("tbody")

    #oddrow1
    parser_odd1 = parser.find("tr.oddrow.rowinfo1")
    odd_departure_times = values_from_html(parser_odd1, ["td.depdest", "div.content.emphasize"])
    odd_arrival_times = values_from_html(parser_odd1, ["td.arrdest", "div.content.emphasize"])
    odd_price_lf = values_from_html(parser_odd1, ["td.fareselect.standardlowfare", "div.content"])
    odd_price_lfp = values_from_html(parser_odd1, ["td.fareselect.standardlowfareplus", "div.content"])
    odd_price_flx = values_from_html(parser_odd1, ["td.fareselect.standardflex.endcell", "div.content"])
    #evenrow1
    parser_even1 = parser.find("tr.evenrow.rowinfo1")
    even_departure_times = values_from_html(parser_even1, ["td.depdest", "div.content.emphasize"])
    even_arrival_times = values_from_html(parser_even1, ["td.arrdest", "div.content.emphasize"])
    even_price_lf = values_from_html(parser_even1, ["td.fareselect.standardlowfare", "div.content"])
    even_price_lfp = values_from_html(parser_even1, ["td.fareselect.standardlowfareplus", "div.content"])
    even_price_flx = values_from_html(parser_even1, ["td.fareselect.standardflex.endcell", "div.content"])

    #combine
    deptimes = odd_departure_times + even_departure_times
    arrtimes = odd_arrival_times + even_arrival_times
    lowfare = odd_price_lf + even_price_lf
    lowfareplus = odd_price_lfp + even_price_lfp
    flex = odd_price_flx + even_price_flx
    print(deptimes)
    print(arrtimes)
    print(lowfare)
    print(lowfareplus)
    print(flex)