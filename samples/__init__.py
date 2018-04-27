from samples.create_uplink import *
from api.api_auth import SteelConnectAPI
import app

if __name__ == "__main__":
    mock_api = SteelConnectAPI("Aubrey", "Aubrey", 'monash.riverbed.cc', 'org-Monash-d388075e40cf1bfd')
    app.create_uplink(mock_api, melbourne_shop_parameters)
