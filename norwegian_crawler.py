import requests
import re
from pyquery import PyQuery
from FlightInfo import FlightInfo

base_url = "https://www.norwegian.com/us/ipc/availability/avaday"

'''
POST /us/ipc/availability/avaday?
D_City=OSL&
A_City=RIX&
TripType=1&
D_Day=01&
D_Month=201810&
D_SelectedDay=01&
R_Day=01&
R_Month=201810&
R_SelectedDay=01&
dFlight=DY738OSLTRDDY1078TRDRIX&d
CabinFareType=1&
AgreementCodeFK=-1&
CurrencyCode=USD&
rnd=85501&
processid=80276&
mode=ab HTTP/1.1
'''
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
    "dFlight" : "DY1072OSLRIX",

    #other variables that doen't change anything
    "processid" : "40",
    "rnd" : "10",
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
    if resp.status_code != 200:
        return None
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

def min_price(a, b, c):
    a = float(a)
    b = float(b)
    c = float(c)
    return str(min(min(a, b), c))


def construct_flight_info(departure_times, arrival_times, lowfare, lowfareplus, flex, airport_d, airport_a):
    info = []
    n = len(departure_times)
    for i in range(0, n):
        price = min_price(lowfare[i], lowfareplus[i], flex[i])
        mem = FlightInfo(departure_times[i], arrival_times[i], price, airport_d, airport_a)
        info.append(mem)
    return info

if __name__ == "__main__":
    url = construct_url(base_url, payload)
    _html = download_html(url)
    
    with open("with_flight_number", "w") as f:
        f.write(_html)

    pageloads = []
    if _html:
        pageloads.append(url)
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

    #get airports
    parser = parser.find("tr.oddrow.rowinfo2.lastrow")

    airport_dept = parser.find("td.depdest").find("div.content").text()
    airport_arrv = parser.find("td.arrdest").find("div.content").text()
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
    print(airport_dept)
    print(airport_arrv)

    info = construct_flight_info(deptimes, arrtimes, lowfare, lowfareplus, flex, airport_dept, airport_arrv)
    for flight in info:
        print(str(flight))