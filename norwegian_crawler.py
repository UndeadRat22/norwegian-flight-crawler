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

counter = 0
def query_html_data(pyquery, qfilters):
    for f in qfilters:
        pyquery = pyquery.find(f)
    gen = pyquery.items()
    data = []
    for x in gen:
        print(x)
        pq = PyQuery(x)
        txt = pq.text()
        data.append(txt)
    return data

def min_price(list):
    low = float(list[0])
    for x in list:
        if float(x) < low:
            low = float(x)
    return str(low)

def generate_flight_info(deptimes, arrtimes, lfp, lfpp, sfp, dep_air, arr_air):
    n = len(deptimes)
    info = []
    for i in range(0, n):
        info.append(FlightInfo(deptimes[i], arrtimes[i], min_price([lfp[i], lfpp[i], sfp[i]]), dep_air, arr_air))
    return info


if __name__ == "__main__":
    #with open("to_analyze.html", "r") as html_file:
        #_html = html_file.read().encode("UTF-8")
    url = construct_url(base_url, payload)
    print(url)
    _html = download_html(url)
    with open("temp.html", "w") as blah:
        blah.write(_html)
    parser = PyQuery(_html).find("tbody")

    #oddrow rowinfo1
    parser_a = parser.find("tr.oddrow.rowinfo1")
    deptimes = query_html_data(parser_a, ["td.depdest"])
    arrtimes = query_html_data(parser_a, ["td.arrdest"])
    lowfareprices = query_html_data(parser_a, ["td.fareselect.standardlowfare", "div.content", "label"])
    lowfareplusprices = query_html_data(parser_a, ["td.fareselect.standardlowfareplus", "div.content", "label"])
    standardflexprices = query_html_data(parser_a, ["td.fareselect.standardflex.endcell", "div.content", "label"])
    
    #oddrow rowinfo2 lastrow
    parser_b = parser.find("tr.oddrow.rowinfo2.lastrow")

    dep_airport = query_html_data(parser_b, ["td.depdest", "div.content"])[0]
    arr_airport = query_html_data(parser_b, ["td.arrdest", "div.content"])[0]

    flightinfo = generate_flight_info(deptimes, arrtimes, lowfareprices, lowfareplusprices, standardflexprices, dep_airport, arr_airport)
    for fi in flightinfo:
        print(str(fi))
    #print(deptimes)
    #print(arrtimes)
    #print(lowfareprices)
    #print(lowfareplusprices)
    #print(standardflexprices)
    #parser_part1 = parser.find("td.depdest")
    #print(parser_part1)
    #tag = parser("td").filter(".depdest").text()
    #print(tag)

    #url = construct_url(base_url, payload)
    #print(get_data(url))