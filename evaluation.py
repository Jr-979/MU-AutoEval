from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import chromedriver_autoinstaller
import time
import random

allowed_Point = [2,3,7]
def ranBias():
    random_point = list(allowed_Point)
    ran_id = random.randint(0,len(allowed_Point)-1)
    return random_point[ran_id]

def Convert(string, delim = '\n'):
    li = list(string.split(delim))
    return li

def main():
    print("Downloading Requirement...")
    try: 
        chromedriver_autoinstaller.install()
    except:
        print("Requirement error make sure that you have Google chrome 96.0+")
        return False

    print("Requirement sastisfied")    
    driver = webdriver.Chrome()

    driver.get("http://www.student.mahidol.ac.th/evaluation/index.asp?cookie-lost")
    driver.set_window_size(1280, 715)

    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "td:nth-child(1) > a > b")))
        print ("Page is ready!")
        driver.find_element(By.CSS_SELECTOR, "td:nth-child(1) > a > b").click()
        current_Sem = driver.find_element(By.CSS_SELECTOR, "td:nth-child(1) > a > b").text

        time.sleep(1)
        user_info = Convert(driver.find_element_by_xpath("/html/body").text)


        subject = []
        for text in user_info:
            if text.isupper():
                subject.append(text)

        subject_code = subject[1::2]


        for subject in subject_code:
            driver.get(f"http://www.student.mahidol.ac.th/evaluation/evaluate.asp?cid={subject}&fid=EG006C&tid=EG005T&mid=0&quarter={current_Sem[-2::1]}{current_Sem[0]}")
            driver.set_window_size(1280, 715)
            if not "นักศึกษาประเมินรายวิชาเสร็จเรียบร้อยแล้ว" in driver.page_source:
                driver.find_element(By.CSS_SELECTOR, f"tr:nth-child(3) .scorePic:nth-child({ranBias()})").click()
                driver.find_element(By.CSS_SELECTOR, f"tr:nth-child(4) .scorePic:nth-child({ranBias()})").click()
                driver.find_element(By.CSS_SELECTOR, f"tr:nth-child(5) .scorePic:nth-child({ranBias()})").click()
                driver.find_element(By.CSS_SELECTOR, f"tr:nth-child(6) .scorePic:nth-child({ranBias()})").click()
                driver.find_element(By.CSS_SELECTOR, f"tr:nth-child(7) .scorePic:nth-child({ranBias()})").click()
                driver.find_element(By.CSS_SELECTOR, f"tr:nth-child(9) .scorePic:nth-child({ranBias()})").click()
                driver.find_element(By.CSS_SELECTOR, f"tr:nth-child(10) > #q2").click()
                driver.find_element(By.CSS_SELECTOR, f"tr:nth-child(10) .scorePic:nth-child({ranBias()})").click()
                driver.find_element(By.CSS_SELECTOR, f"tr:nth-child(11) .scorePic:nth-child({ranBias()})").click()
                driver.find_element(By.CSS_SELECTOR, f"tr:nth-child(12) .scorePic:nth-child({ranBias()})").click()
                driver.find_element(By.CSS_SELECTOR, f"tr:nth-child(13) .scorePic:nth-child({ranBias()})").click()
                driver.find_element(By.CSS_SELECTOR, f"tr:nth-child(14) .scorePic:nth-child({ranBias()})").click()
                driver.find_element(By.CSS_SELECTOR, f"tr:nth-child(15) .scorePic:nth-child({ranBias()})").click()
                driver.find_element(By.CSS_SELECTOR, f"tr:nth-child(16) .scorePic:nth-child({ranBias()})").click()
                driver.find_element(By.CSS_SELECTOR, f"tr:nth-child(18) .scorePic:nth-child({ranBias()})").click()
                driver.find_element(By.CSS_SELECTOR, f"tr:nth-child(19) > #q3").click()
                driver.find_element(By.CSS_SELECTOR, f"tr:nth-child(19) .scorePic:nth-child({ranBias()})").click()
                driver.find_element(By.CSS_SELECTOR, f"tr:nth-child(20) .scorePic:nth-child({ranBias()})").click()
                driver.find_element(By.CSS_SELECTOR, f"tr:nth-child(22) .scorePic:nth-child({ranBias()})").click()
                driver.find_element(By.CSS_SELECTOR, f"tr:nth-child(23) .scorePic:nth-child({ranBias()})").click()
                driver.find_element(By.CSS_SELECTOR, f"td:nth-child(2) > .btnBar").click()
                driver.switch_to.alert.text == "กรุณาตรวจสอบข้อมูลให้ถูกต้อง\nหากบันทึกผลการประเมินแล้ว ระบบจะไม่อนุญาตให้ทำการแก้ไข\n\nต้องการบันทึกผลการประเมินหรือไม่"
                driver.switch_to.alert.accept()

            driver.get(f"http://www.student.mahidol.ac.th/evaluation/teacher.asp?cid={subject}&tid=EG005T&mid=0&quarter={current_Sem[-2::1]}{current_Sem[0]}")
            while  "Click เพื่อประเมิน" in driver.page_source:
                driver.find_element(By.LINK_TEXT, "Click เพื่อประเมิน").click()
                element = driver.find_element(By.LINK_TEXT, "Click เพื่อประเมิน")
                actions = ActionChains(driver)
                actions.move_to_element(element).perform()
                element = driver.find_element(By.CSS_SELECTOR, "body")
                actions = ActionChains(driver)
                time.sleep(0.5)
                
                for selected in range (25):
                    try:
                        driver.find_element(By.CSS_SELECTOR, f"tr:nth-child({selected}) .scorePic:nth-child({ranBias()})").click()
                    except:
                        continue

                for i in range (3):
                    for missing in range (25):
                        try:
                            driver.find_element(By.CSS_SELECTOR, f"tr:nth-child({missing}) > #q{i} > .scorePic:nth-child({ranBias()})").click()
                        except:
                            continue
                driver.find_element(By.CSS_SELECTOR, f"td:nth-child(2) > .btnBar").click()
                assert driver.switch_to.alert.text == "กรุณาตรวจสอบข้อมูลให้ถูกต้อง\nหากบันทึกผลการประเมินแล้ว ระบบจะไม่อนุญาตให้ทำการแก้ไข\n\nต้องการบันทึกผลการประเมินหรือไม่"
                driver.switch_to.alert.accept()
                time.sleep(0.5)
        
        return True
    except:
        return False

    driver.quit()

if __name__ == "__main__":
    print("Program Running")
    Suscess = main()
    if Suscess:
        print("\nSuscessfully Evaluated!!!! Thankyou for using. ")
        input("Press enter to exit the program")
    
    else:
        print("\nAn error might occured please restart the program.")