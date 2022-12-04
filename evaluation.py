import subprocess
import sys
subprocess.run([sys.executable, "-m", "pip","install","-r","requirement.txt"])

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import exceptions as Exceptions
import chromedriver_autoinstaller
import time
import random

allowed_Point = [2,3,7]

def ranBias(bias = allowed_Point)-> int:
    return bias[random.randint(0,len(bias)-1)]

def Convert(string, delim = '\n')-> list:
    return list(string.split(delim))


def main():
    print("Downloading Requirement...")
    # Check for chrome driver if not found install one
    try: 
        chromedriver_autoinstaller.install()
    except:
        print("Requirement error make sure that you have Google chrome 96.0+")
        return 1

    print("Requirement sastisfied")

    driver = webdriver.Chrome()
    driver.get("http://www.student.mahidol.ac.th/evaluation/index.asp?cookie-lost")
    driver.set_window_size(1280, 715)

    # Wait for 60 second for enter username and password
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "td:nth-child(1) > a > b")))
    print ("Page is ready!")
    driver.find_element(By.CSS_SELECTOR, "td:nth-child(1) > a > b").click()

    # Get the most recent semester 
    current_Sem = driver.find_element(By.CSS_SELECTOR, "td:nth-child(1) > a > b").text
    time.sleep(1)

    # Grab all the subject name and subject code from the most recent semester
    user_info = Convert(driver.find_element_by_xpath("/html/body").text)
    subjecta = []
    for text in user_info:
        if text.isupper():
            subjecta.append(text)

    # Store all the avaliable subject as a subject code
    subject_code = []
    for text in subjecta:
        if len(text) == 7:
            subject_code.append(text)

    # Loops through all the subject code 
    for subject in subject_code:
        print("Subject : ",subject,"Year  : ",current_Sem[-2::1], "Term : ",current_Sem[0])
        driver.get(f"http://www.student.mahidol.ac.th/evaluation/evaluate.asp?cid={subject}&fid=EG006C&tid=EG005T&mid=0&quarter={current_Sem[-2::1]}{current_Sem[0]}")
        driver.set_window_size(1280, 715)

        # Check weather evaluation is complete
        if not "นักศึกษาประเมินรายวิชาเสร็จเรียบร้อยแล้ว" in driver.page_source:
            # Max number of checkboxes start from 3 to 23 with 10,19,2 
            for checkbox in range(3,24,1):
                if checkbox == 10:
                    driver.find_element(By.CSS_SELECTOR, f"tr:nth-child(10) > #q2").click()
                elif checkbox == 19:
                    driver.find_element(By.CSS_SELECTOR, f"tr:nth-child(19) > #q3").click()

                try:
                    driver.find_element(By.CSS_SELECTOR, f"tr:nth-child({checkbox}) .scorePic:nth-child({ranBias()})").click()
                except Exceptions.NoSuchElementException:
                    pass
                
            # Press a submit button
            driver.find_element(By.CSS_SELECTOR, f"td:nth-child(2) > .btnBar").click()

            # Press an accept button
            driver.switch_to.alert.text == "กรุณาตรวจสอบข้อมูลให้ถูกต้อง\nหากบันทึกผลการประเมินแล้ว ระบบจะไม่อนุญาตให้ทำการแก้ไข\n\nต้องการบันทึกผลการประเมินหรือไม่"
            driver.switch_to.alert.accept()

        # Loops through all available teacher
        driver.get(f"http://www.student.mahidol.ac.th/evaluation/teacher.asp?cid={subject}&tid=EG005T&mid=0&quarter={current_Sem[-2::1]}{current_Sem[0]}")
        while  "Click เพื่อประเมิน" in driver.page_source:
            driver.find_element(By.LINK_TEXT, "Click เพื่อประเมิน").click()
            element = driver.find_element(By.LINK_TEXT, "Click เพื่อประเมิน")
            actions = ActionChains(driver)
            actions.move_to_element(element).perform()
            element = driver.find_element(By.CSS_SELECTOR, "body")
            actions = ActionChains(driver)
            time.sleep(0.5)
            
            # Fill each checkbox with random value
            for selected in range (25):
                try:
                    driver.find_element(By.CSS_SELECTOR, f"tr:nth-child({selected}) .scorePic:nth-child({ranBias()})").click()
                except Exceptions.NoSuchElementException:
                    # If the element is not befound continue
                    continue
            
            # Fill missing checkbox
            for i in range (3):
                for missing in range (25):
                    try:
                        driver.find_element(By.CSS_SELECTOR, f"tr:nth-child({missing}) > #q{i} > .scorePic:nth-child({ranBias()})").click()
                    except Exceptions.NoSuchElementException:
                        # If the element is not befound continue
                        continue
            driver.find_element(By.CSS_SELECTOR, f"td:nth-child(2) > .btnBar").click()
            assert driver.switch_to.alert.text == "กรุณาตรวจสอบข้อมูลให้ถูกต้อง\nหากบันทึกผลการประเมินแล้ว ระบบจะไม่อนุญาตให้ทำการแก้ไข\n\nต้องการบันทึกผลการประเมินหรือไม่"
            driver.switch_to.alert.accept()
            time.sleep(0.5)
    
    return 0 

if __name__ == "__main__":
    print("Program Running")
    fail = main()
    if not fail:
        print("\nSuscessfully Evaluated!!!! Thankyou for using. ")
        input("Press enter to exit the program")
    
    else:
        print("\nAn error might occured please restart the program.")
