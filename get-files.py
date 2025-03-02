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

sharepoint_download_url = "https://mehmetakifedutr-my.sharepoint.com/:f:/g/personal/ihsanpence_mehmetakif_edu_tr/EtNvTlDRs4pFrTi9F8Tar7kBFyyGzoxwWOlpkjDmhuTvkw?e=3vZdhv"
download_dir = os.getcwd() + "/downloads"
css_selector = "[aria-label='Download'], [data-id='download']"


def check_zip(_) -> bool:
    return os.listdir(download_dir) != [] and list(Path(download_dir).glob("*.part")) == []


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

    print(">>> going to website")
    driver = webdriver.Firefox(options=options)
    driver.get(sharepoint_download_url)

    print(">>> waiting for download button")
    _ = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

    print(">>> clicking download button")
    elem = driver.find_element(By.CSS_SELECTOR, css_selector)
    elem.click()

    print(">>> waiting for zip file to download")
    _ = WebDriverWait(driver, 60).until(check_zip)
    sleep(5)
    driver.quit()


if __name__ == "__main__":
    main()
