from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import smtplib, ssl
from datetime import date
from datetime import timedelta

# --- VARIABLER ---
padelCourts = ["Ultimate Padel", "Catella Arena", "Padelverket Spånga", "Klövern Padelcenter : Kista", "MOVE Wellness", "Solna Padel Court", "Svea Padel : Täby"]

NUMB_OF_DAYS = 6
SKIP_DAYS = [7,1]
PREF_TID = [15,24]
TO_EMAIL = ''
FROM_EMAIL = ''
EMAIL_PASSWORD = ''
# ----------------

def TimeOut(elementID):
    try:
        element_present = EC.presence_of_element_located((By.XPATH, elementID))
        WebDriverWait(driver, 20).until(element_present)
        time.sleep(1)
    except TimeoutException:
        print("Timed out waiting for page to load")
    finally:
        print("Page loaded")

def Settings():
    with open("Settings.txt", "r") as f:

        content = f.readlines()
        print(content[0])


def RepresentsInt(s):
    try:
        int(s)
        return True

    except ValueError:

        return False

def enterDate(string,datum):
    driver.find_element_by_id(string).clear()
    driver.find_element_by_id(string).send_keys(datum)
    return None


Settings()
PATH = "D:\Program\python\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://www.matchi.se/")
#Datum = driver.find_element_by_id("date").get_attribute("value")
driver.find_element_by_css_selector("button[data-id='sport']").click()
driver.find_element_by_css_selector("li[data-original-index='5']").click()

slotID = 0
areTimesAvailable = False
foundTimes = False

message = """\
Subject: Det finns padeltider att boka!

In och boka nu! https://www.matchi.se/book/index
"""


for courtIndex in range(len(padelCourts)):

    # First search, different html Id on search element
    if courtIndex == 0:
        enterDate("date", date.today().isoformat())
        driver.find_element_by_id("q").send_keys(padelCourts[courtIndex])
    else: # Other searches
        enterDate("showDate", date.today().isoformat())
        driver.find_element_by_name("q").clear()
        driver.find_element_by_name("q").send_keys(padelCourts[courtIndex])

    driver.find_element_by_name("submit").click()
    time.sleep(2) # wait for page to load courts / slots

    courtId = driver.page_source.find("slots_")

    # SlotId can be 1-3 numbers, this gets the full slotId number
    for j in range(10):
        if (RepresentsInt(driver.page_source[courtId+6: courtId + 7+j])):
            slotID = driver.page_source[courtId+6: courtId +7 + j]
        else:
            break
    print(slotID)



    for dayIndex in range(NUMB_OF_DAYS):
        dateIteration = (date.today() + timedelta(days=dayIndex))
        # Checks if current date iteration is not in days to skip (monday = 0 etc.)
        if dateIteration.isoweekday() not in SKIP_DAYS:
            print(dateIteration.isoformat())

            prefTimesList = []
            areTimesAvailable = False
            enterDate("showDate", dateIteration.isoformat())
            driver.find_element_by_name("submit").click()

            time.sleep(2)

            availableTimes = driver.find_elements_by_xpath("//*[@id='slots_" + str(slotID) + "']/ul/li")

            for timeIndex in range(len(availableTimes)):

                TidTabell = driver.find_element_by_xpath("//*[@id='slots_" + str(slotID) + "']/ul/li[" + str(timeIndex + 1) + "]/button").text
                Tid = TidTabell[:2]

                if PREF_TID[0] <= int(Tid) <= PREF_TID[1]:
                    print('Hittade en tid '+Tid)
                    TidTabell = TidTabell.replace(" ",":")
                    prefTimesList.append(TidTabell)
                    areTimesAvailable = True
                else:
                    print('Ointresserad av: '+ Tid )

            if areTimesAvailable:
                prefTimesStr = ', '.join(prefTimesList)
                message += " \n"+dateIteration.isoformat() + " - " + padelCourts[courtIndex]+": " + prefTimesStr
                print(message)
            else:
                print('Hittade inga tider')








if areTimesAvailable:
    print('sending email... '+message)
    message = message.replace("Ä","A")
    message = message.replace("ä", "a")
    message = message.replace("Ö", "O")
    message = message.replace("ö", "o")
    message = message.replace("Å", "A")
    message = message.replace("å", "a")

    port = 465  # For SSL

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(FROM_EMAIL, EMAIL_PASSWORD)
        server.sendmail(FROM_EMAIL, TO_EMAIL, message)

    #mailserver = smtplib.SMTP('smtp.office365.com',587)
    #mailserver.ehlo()
    #mailserver.starttls()
    #mailserver.login('padeltimer@outlook.com', 'matchitimer1')
    #mailserver.sendmail('padeltimer@outlook.com', TO_EMAIL, message)
    #mailserver.quit()