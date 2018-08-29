import requests
from re import findall as regex
from pyquery import PyQuery
from flightinfo import FlightInfo

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

def get_flight_ids(html_text):
    __pq = PyQuery(html_text).find("tbody").find("td.inputselect").find("div.content").find("input")
    ids = []
    for __node in __pq.items():
        if (__node.hasClass("radio-ajax")):
            __matched = regex("[A-Z]{2}.*[A-Z]",str(__node.attr("value")))
            ids.extend(__matched)
    return ids

def get_flight_info_by_id(id, html_text):
    __pqbody = PyQuery(html_text).find("tbody")
    __pqtable = PyQuery(html_text).find("div.selectioncontainer").find("table.selectiontable")

    __pqrow1 = __pqbody.find("tr.selectedrow.rowinfo1")
    __pqrow2 = __pqbody.find("tr.selectedrow.rowinfo2")

    dep_time = __pqrow1.find("td.depdest").text()
    arr_time = __pqrow1.find("td.arrdest").text()

    dep_port = __pqrow2.find("td.depdest").text()
    arr_port = __pqrow2.find("td.arrdest").text()

    __pqprices = __pqtable.find("td.rightcell.emphasize")

    full_price = __pqprices.eq(0).text()
    tax_price = __pqprices.eq(1).text()

    finfo = FlightInfo(id, dep_time, arr_time, full_price, tax_price, dep_port, arr_port)
    
    print(dep_time, arr_time, dep_port, arr_port, full_price, tax_price)

    return finfo

if __name__ == "__main__":
    url = construct_url(base_url, payload)
    __html = download_html(url)
    
    #with open("with_flight_number.html", "w") as f:
    #    f.write(_html)

    pageloads = []
    if not __html:
        exit()
    
    pageloads.append(url)

    flight_ids = get_flight_ids(__html)
    get_flight_info_by_id(flight_ids[0], __html)