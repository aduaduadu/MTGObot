from selenium import webdriver


def main():
    # alter User Agent and open url
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17')
    browser = webdriver.Firefox(profile)
    browser.get('http://mtgoclanteam.com/Cards?edition=RTR')

    # identify critical parts of webpage
    cardTable = browser.find_element_by_css_selector('#cardtable > tbody:nth-child(2)')
    cardList = cardTable.find_elements_by_tag_name('tr')

    for row in cardList:
        elements = row.find_elements_by_tag_name('td')

        name = elements[0].text
        buy = float(elements[2].text)
        sell = float(elements[3].text)

        stock = elements[4].text

        print(len(stock))

    browser.quit()
