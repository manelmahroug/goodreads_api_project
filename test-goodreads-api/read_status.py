try:
    import pprint
    import os
    import xml.etree.ElementTree as ET
    import json
    import requests
except Exception as e:
    print("\t",e)


def main():

    pp = pprint.PrettyPrinter(indent=4)
    url = "https://www.goodreads.com/read_statuses/ID?format=xml&key=OKwj2qRaOnsUBJqogIu8tw"
    response = requests.get(url)

    if response.status_code == 200:
        
        string_json_response = response.content.decode("utf-8")
        # json_response = json.loads(string_json_response)
        pp.pprint(string_json_response)


if __name__ == "__main__":
    # clearing screen
    if os.name == "nt":
        _ = os.system('cls')

    main()
    input("\n\n\nPress enter to exit 🚀...")

    # clearing screen
    if os.name == "nt":
        _ = os.system('cls')
