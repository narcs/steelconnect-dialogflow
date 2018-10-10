# Utility functions that actions can call on.

class APIError(Exception):
    pass

def format_wan_list(items):
    """
    Given the successful result of `api_auth.list_wans().json()["items"]`,
    returns the list of WANs as a nicely-formatted string suitable for
    presenting to the user.
    """

    s = ""

    for wan in items:
        if wan["longname"] is not None:
            s += "\n - " + str(wan["name"]) + " (" + wan["longname"] + ")"
        else:
            s += "\n - " + str(wan["name"])
    
    return s


def get_wan_id_by_name(api_auth, wan_name):
    """
    Given a WAN's short name:
    - If there is a WAN by that exact name, returns the ID of the first matching WAN.
    - If no such WAN exists, raises an APIError with a human-readable error string.
    """

    res = api_auth.wan.list_wans()
    data = res.json()["items"]

    if res.status_code == 200:
        for wan in data:
            if wan["name"] == wan_name:
                return wan["id"]

        raise APIError("The WAN '{}' does not exist. Valid WANs (use the name not in brackets):".format(wan_name) + format_wan_list(data))
    else:
        raise APIError("Failed to get the list of WANs")


def get_site_id_by_name(api_auth, site_name, city, country_code):
    """
    Given a Site's short name:
    - If there is a Site by that name city and country, returns the ID of the first matching Site.
    - If no such site exists, raises an APIError with a human-readable error string.
    """
    res = api_auth.site.list_sites()

    if res.status_code == 200:
        data = res.json()["items"]

        for site in data:
            if site["name"] == site_name and site["city"] == city and site["country"] == country_code:
                return site["id"]
        raise APIError(("The site {} in {} {} does not exist").format(site_name, city, country_code))
    elif res.status_code == 400:
        raise APIError("Invalid parameters: {}".format(res.json()["error"]["message"]))
    elif res.status_code == 500:
        raise APIError("Failed to get the list of Sites")
    else:
        raise APIError("Error: Could not connect to SteelConnect")


def format_sitelink_list(api_auth, items):
    """
    Given the successful result of `api_auth.sitelink.get_sitelinks().json()["items"]`,
    returns the list of sitelinks as a nicely-formatted string suitable for
    presenting to the user.

    Requires `api_auth` to get the names of the remote sites.
    """

    s = ""

    for link in items:
        remote_site_name = ""
        res = api_auth.site.get_site(link["remote_site"])

        if res.status_code == 200:
            remote_site_name = res.json()["name"]
        else:
            remote_site_name = "<unknown>"

        s += "\n - To: {} ({}), Status: {}".format(remote_site_name, link["remote_site"], link["status"])

    return s

