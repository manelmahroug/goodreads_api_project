"""
For running this script, please ensure that `sample` directory has `resources` directory container chromedriver for your OS executable file,
clone this repository for better usage.


"""


try:
    import json
    import re
    import pprint
    import xmltodict
    import requests
    import urllib
    import os
    import time
    import configparser
    from bs4 import BeautifulSoup
    from collections import defaultdict
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
except Exception as e:
    print(e)

# Reading the config files
config = configparser.ConfigParser()
config.read("./config.ini")
# =======================================================
# Extracting config files
CLIENT_KEY = config['credentials']['client_key']  # string
CLIENT_SECRET = config['credentials']['client_secret']  # string
EMAIL_ID = config['credentials']['email_id']  # string
PASSWORD = config['credentials']['password']  # string
# =======================================================
ROOT_URL = config['nav-links']['root_url']  # string
CHILD_URL = config['nav-links']['child_url']  # string
# =======================================================
GENRES = config['scrap-config']['genres'].split(',')  # string[]

# print(CLIENT_KEY, CLIENT_SECRET)

driver = webdriver.Chrome("./resources/chromedriver")
driver.delete_all_cookies()
pp = pprint.PrettyPrinter(indent=2)


def element_grabber(param, by_type="xpath"):
    global driver
    element = None
    if by_type == "xpath":
        element = driver.find_element(By.XPATH, param)
    elif by_type == "id":
        element = driver.find_element(By.ID, param)
    return element


def response_to_json_dict(response):
    dict_response = defaultdict()
    json_response = ""
    if response.status_code == 200:

        print(f"Response Status Code : {response.status_code} ✔️")

        string_xml_response = response.content.decode("utf-8")
        json_response = json.dumps(xmltodict.parse(string_xml_response))
        dict_response = json.loads(json_response)

    else:

        print(f"Response Status Code : {response.status_code} ❌")

    return dict_response, json_response


def link_navigator():
    global driver

    # opening the goodreads website using selenium framework
    driver.get(ROOT_URL)

    # logging into goodreads API as a developer
    try:

        # grabbing the email field
        email_input_box = element_grabber(
            "/html/body/div[2]/div[1]/div/div/div[1]/div/div/form/div[1]/input[1]")
        # sending the email as input to the above field
        email_input_box.send_keys(EMAIL_ID)

        # grabbing the password field
        password_textbox = element_grabber(
            "/html/body/div[2]/div[1]/div/div/div[1]/div/div/form/div[2]/div/input")
        # sending the password as input to the above field
        password_textbox.send_keys(PASSWORD)

        # grabbing sign in button
        sign_btn = element_grabber(
            "/html/body/div[2]/div[1]/div/div/div[1]/div/div/form/div[3]/input[1]")
        # submitting the login form
        sign_btn.click()

        retrieval_count = 0
        for genre in GENRES:
            retrieval_count += 1
            print(f"Book Retrieved #{retrieval_count}")

            # navigating the books paginated link
            driver.get(CHILD_URL + genre)

            book_link = element_grabber(
                "/html/body/div[2]/div[3]/div[1]/div[2]/div[3]/div[4]/div[1]/a[2]").get_attribute('href')
            print("Accessing Book URL...⏰")
            print(book_link)

            ID = re.findall(r'(\d{1,11})', book_link)[0]

            print(f"Requesting Goodreads API 🔥 with Client key 🔑, Book ID = {ID}")

            url = f'https://www.goodreads.com/book/show/{ID}.xml?key=OKwj2qRaOnsUBJqogIu8tw'
            print(url)

            response = requests.get(url)

            print("Request sent 📨")
            dict_response, json_response = response_to_json_dict(response)

            with open("static/response.txt", "w+") as file:
                file.write(json_response)

            print("============================================================")
            book_title = dict_response['GoodreadsResponse']['book']['title']
            print("Book Title : " + book_title)

            isbn = dict_response['GoodreadsResponse']['book']['isbn']
            print("ISBN : " + isbn)

            isbn13 = dict_response['GoodreadsResponse']['book']['isbn13']
            print("ISBN13 : " + isbn13)

            publication_year = dict_response['GoodreadsResponse']['book']['publication_year']
            print("Publication Year : " + publication_year)

            publication_month = dict_response['GoodreadsResponse']['book']['publication_month']
            print("Publication Month : " + publication_month)

            publication_day = dict_response['GoodreadsResponse']['book']['publication_day']
            print("Publication Day : " + publication_day)

            reviews_widget = dict_response['GoodreadsResponse']['book']['reviews_widget']
            review_widgets_json = json.loads(json.dumps(reviews_widget))

            soup = BeautifulSoup(review_widgets_json, features="html.parser")
            # print(soup.prettify())

            reviews_url = soup.iframe['src'].replace("DEVELOPER_ID", CLIENT_KEY)

            driver.get(reviews_url)

            # working with review 1

            view_more_link = element_grabber("/html/body/div/div[2]/div/a").get_attribute('href')
            driver.get(view_more_link)

            print("========================================================================")
            # we arrive at specific review's page

            # Reviewer's Name
            reviewer_name = element_grabber("/html/body/div[2]/div[3]/div[1]/div[2]/h1/a").text
            print("Reviewer's name : " + reviewer_name.strip("'s Reviews"))

            # Likes on her reviews
            likes_on_reviews = element_grabber("/html/body/div[2]/div[3]/div[1]/div[2]/div[3]/div[2]/div/div/div[1]/div/div[3]/span/a/span").text.strip(" likes")
            print("Likes on Review : " + likes_on_reviews)

            # Review
            review = element_grabber("/html/body/div[2]/div[3]/div[1]/div[2]/div[3]/div[2]/div/div/div[1]/div/div[2]").text
            print("Review : " + review)

            # Date of review
            date_of_review = element_grabber("/html/body/div[2]/div[3]/div[1]/div[2]/div[3]/div[2]/div/div/div[1]/div/div[1]/div[1]/span[1]").text
            print("Date Of Review : " + date_of_review)

            # Ratings
            rating = element_grabber("/html/body/div[2]/div[3]/div[1]/div[2]/div[3]/div[2]/div/div/div[1]/div/div[1]/div[3]/meta").get_attribute('content')
            print("Rating : " + rating)

            # Experience
            rating_exp = element_grabber("/html/body/div[2]/div[3]/div[1]/div[2]/div[3]/div[2]/div/div/div[1]/div/div[1]/div[3]/span[2]").get_attribute('title')
            print("Reviewer Reading Experience : " + rating_exp)







            break

    except Exception as exception:
        print(exception)
    finally:
        driver.quit()


# START HERE
if __name__ == "__main__":
    # clearing screen
    if os.name == "nt":
        _ = os.system('cls')

    link_navigator()

    input("\n\n\nPress enter to exit 🚀...")

    # clearing screen
    if os.name == "nt":
        _ = os.system('cls')
