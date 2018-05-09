class TestJsonObject:
    def __init__(self, longname):
        self.longname = longname

    def json(self):
        return {"longname": self.longname}

case1_success_1_sites = {
        "site1": TestJsonObject("site1_longname"),
        "site2": TestJsonObject("site2_longname"),
    }

case1_success_1_wans = {
        "wan1": TestJsonObject("wan1_longname"),
        "wan2": TestJsonObject("wan2_longname"),
    }
case1_success_1_uplinks_return = {"items": [
        {
            "name": "Berlin_Shop",
            "site": "site1",
            "wan": "wan1",
        },
        {
            "name": "Melbourne",
            "site": "site2",
            "wan": "wan2",
        },
    ]}

def site_return(site_id):
    return case1_success_1_sites[site_id]

def wan_return(wan_id):
    return case1_success_1_wans[wan_id]

case1_basic_request = 'hi'
case1_success_1_uplinks = 'All uplinks:'
count = 1
for uplink in case1_success_1_uplinks_return["items"]:
    site = case1_success_1_sites[uplink["site"]].json()["longname"]
    name = uplink["name"]
    wan = case1_success_1_wans[uplink["wan"]].json()["longname"]

    case1_success_1_uplinks += "\n {}. {}/{}/{}".format(count, site, name, wan)
    count += 1