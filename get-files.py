#!/usr/bin/env python

import os
from pathlib import Path
from time import sleep
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

sharepoint_download_url = "https://mehmetakifedutr-my.sharepoint.com/:f:/g/personal/eduman_mehmetakif_edu_tr/EtVND89XNJ9Pt0XAG1uigEgBzcposrNYqLOOWwfvLAekvQ?e=7G7xcV"
download_dir = os.getcwd() + "/downloads"


def check_zip(_) -> bool:
    return os.listdir(download_dir) != [] and list(Path(download_dir).glob(".part")) == []


def main():
    if not Path(download_dir).exists():
        Path(download_dir).mkdir()

    options = Options()
    options.add_argument("--headless")
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir",
                           download_dir)
    options.set_preference(
        "browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")

    driver = webdriver.Firefox(options=options)
    driver.get(sharepoint_download_url)

    _ = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.NAME, "Download")))

    elem = driver.find_element(By.NAME, "Download")
    elem.click()

    _ = WebDriverWait(driver, 60).until(check_zip)
    sleep(1)
    driver.quit()


if __name__ == "__main__":
    main()
