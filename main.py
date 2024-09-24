from selenium.common.exceptions import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from os import environ
import time

W_PATH = environ.get("CHROME_PATH")

W_SERVICES = Service(executable_path=W_PATH)
W_OPTIONS  = Options()
W_OPTIONS.add_experimental_option("detach",True)

def get_speed_test_url() -> str:
    # W_URL = "https://www.speedtest.net/"
    # W_URL = "https://fiber.google.com/speedtest/"
    w_url = "https://www.google.com/search?q=google+speed+test&oq=google+spee&gs_lcrp=EgZjaHJvbWUqDAgAECMYJxiABBiKBTIMCAAQIxgnGIAEGIoFMgYIARBFGDkyBwgCEAAYgAQyBwgDEAAYgAQyBwgEEAAYgAQyBwgFEAAYgAQyBwgGEAAYgAQyBggHEEUYPNIBCDM2NjVqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8"
    return w_url



def get_web_driver():
    W_DRIVER = None
    try:
        W_DRIVER = webdriver.Chrome(service=W_SERVICES, options=W_OPTIONS)

        w_url = get_speed_test_url()    
        W_DRIVER.get(url=w_url)
    except Exception as e:
        print(f"fail to open browser - msg: {e}")
        W_DRIVER = None


    return W_DRIVER


def get_user_expected_internet_speed() -> float:
    w_expected_speed : float = None
    while True:
        try:
            w_user_expected_speed = input(f"What is the expected Internet speed? (Type Exit to quit)\n")

            if w_user_expected_speed.upper() == "EXIT":
                w_expected_speed = None
                break

            if not w_user_expected_speed or not w_user_expected_speed.isnumeric():
                raise ValueError("Please enter valid values or EXIT.")
            else:
                w_expected_speed = float(w_user_expected_speed)

            if w_expected_speed < 1 or w_expected_speed > 9999:
                raise ValueError("Unacceptable speed range")
            
            break
        except Exception as e:
            print(e)


    return w_expected_speed
    

def main() -> None:    

    w_user_expected_speed = get_user_expected_internet_speed()
    if not w_user_expected_speed:
        print(f"Program terminated.")
        return

    print(f"processing")

    w_web_driver = get_web_driver()
    if not w_web_driver:
        print(f"Program terminated.")
        return

    time.sleep(5)
    try:
        w_speed_test_btn = w_web_driver.find_element(By.ID, value='knowledge-verticals-internetspeedtest__test_button')
        print(w_speed_test_btn.text)

        w_speed_test_btn.click()  
        time.sleep(30)

        w_result_download = w_web_driver.find_element(By.ID,value="knowledge-verticals-internetspeedtest__download").text
        w_result_upload   = w_web_driver.find_element(By.ID,value="knowledge-verticals-internetspeedtest__upload").text
    except Exception as e:
        w_web_driver.quit() #Close browser
        print(f"Program terminated, processing failure - msg : {e}")
        return

    w_web_driver.quit() #Close browser

    w_download = w_result_download.split("\n")
    w_upload   = w_result_upload.split("\n")    
    
    w_download_speed       : float = ""
    w_upload_speed         : float = ""
    w_download_speed_units : str = ""
    w_upload_speed_units   : str = ""


    if len(w_download) > 1:
        w_download_speed = w_download[0]
        w_download_speed = float(w_download_speed)

        w_download_speed_units = w_download[1]
        w_download_speed_units = w_download_speed_units.replace("download","").strip()

    if len(w_upload) > 1:
        w_upload_speed = w_upload[0]
        w_upload_speed = float(w_upload_speed)

        w_upload_speed_units = w_upload[1]
        w_upload_speed_units = w_upload_speed_units.replace("upload","").strip()
    
    w_message : str = None
    if w_download_speed < w_user_expected_speed:
       w_message = f"Internet speed is BELOW the expected download value of {w_user_expected_speed}"
        
    if w_upload_speed < w_user_expected_speed:
        if not w_message:
            w_message = f"Internet speed is BELOW the expected upload value of {w_user_expected_speed}"
        else:
            w_message = f"Internet speed is BELOW the expected download and upload value of {w_user_expected_speed}"

    if w_message:
       w_message = f"🦥🐢 {w_message}\n\nDownload: {w_download_speed}-{w_download_speed_units}\nUpload  : {w_upload_speed}-{w_upload_speed_units}"
    else:
        w_message = f"🚀🚄 NICE!! Internet speed is ABOVE the expected value of {w_user_expected_speed}\n\nDownload: {w_download_speed}-{w_download_speed_units}\nUpload  : {w_upload_speed}-{w_upload_speed_units}"
    
    print(w_message)



if __name__ == "__main__":    
    main()
    print("----------------------")
    print("Process completed!! 🏁")