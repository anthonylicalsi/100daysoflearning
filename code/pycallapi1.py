import requests
import pprint

api_url = "https://api.coindesk.com/v1/bpi/currentprice.json"


def get_url(url):

    response = requests.get(url)

    return response.json()


if __name__ == '__main__':
    r = get_url(api_url)
    print(r)
    print(">>>>>>>>>>>>>>>>>>>>>>>>")
    print(type(r))
    print(">>>>>>>>>>>>>>>>>>>>>>>>")

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(r)
