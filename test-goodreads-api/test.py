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

    response = requests.get(
        "https://www.goodreads.com/search/index.xml?key=OKwj2qRaOnsUBJqogIu8tw&q=Ender%27s+Game&page=1")

    if response.status_code == 200:
        string_xml_reponse = response.content.decode("utf-8")
        root = ET.fromstring(string_xml_reponse)
        for root_child in root:
            if root_child.tag == "search":
                for search_child in list(root_child):
                    if search_child.tag == "results":
                        for results_child in search_child:
                            print("\t","Work child ==>")
                            for work_child in results_child:
                                print("\t",work_child.tag, work_child.text)
                                if work_child.tag == "best_book":
                                    print("\t\t","Best Book child ==>")
                                    for best_book_child in work_child:
                                        print("\t\t",best_book_child.tag, best_book_child.text)
                                        if best_book_child.tag == "author":
                                            print("\t\t\t","Author child ==>")
                                            for author_child in best_book_child:
                                                print("\t\t\t",author_child.tag, author_child.text)
                            break


if __name__ == "__main__":
    # clearing screen
    if os.name == "nt":
        _ = os.system('cls')

    main()
    input("\n\n\nPress enter to exit 🚀...")

    # clearing screen
    if os.name == "nt":
        _ = os.system('cls')
