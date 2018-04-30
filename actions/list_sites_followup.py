import logging

from flask import json

def list_sites_followup(api_auth, parameters):
    """
    :param api_auth: steelconnect api object
    :type api_auth: SteelConnectAPI
    :param parameters: json parameters from Dialogflow intent
    :type parameters: json
    :return: Returns a response to be read out to user
    :rtype: string
    """

    # Context doesn't actually need to be checked here, just left as an example
    # context = None
    # for item in parameters["results"]["contexts"]:
    #     if item["name"] == "listsites-followup":
    #         context = item
    #         break                                       # break once correct context is found
    #
    # if not context:
    #     logging.error("Error listsites-followup context not found")
    #     return "There was an error fulfilling your request"
    # else:
    #     pass



    # Get all sites and return a response based on the number of sites
    res = api_auth.site.list_sites()

    if res.status_code == 200:
        data = res.json()["items"]
        num_sites = len(data)

        if parameters:
            try:
                number = int(parameters["number"])
                position = parameters["position"]
            except KeyError as e:
                logging.error("Error processing list_sites_followup intent. {0}".format(e))

                return "There was an error fulfilling your request"
        else:
            number = num_sites
            position = "all"

        speech = ""

        if number > num_sites:
            number = num_sites

        if position == "first":
            data = data[:number]
        elif position == "last":
            data = data[-number:]
        elif position == "all":
            pass
        else:
            logging.error("Error processing list_sites_followup intent. Unrecognised positon: {}".format(position))
            return "There was an error fulfilling your request"

        for site in data:
            speech += ", {}".format(site["name"])

        speech = speech[2:] + "."

    else:
        speech = "Error: Could not connect to SteelConnect"

    logging.debug(speech)

    return speech



    # "contexts": [
    #     {
    #         "name": "readsitelist",
    #         "parameters": {
    #             "number": "2",
    #             "position": "first",
    #             "number.original": "two",
    #             "position.original": "first"
    #         },
    #         "lifespan": 4
    #     },
    #     {
    #         "name": "listsites-followup",
    #         "parameters": {
    #             "number": "2",
    #             "position": "first",
    #             "number.original": "two",
    #             "position.original": "first"
    #         },
