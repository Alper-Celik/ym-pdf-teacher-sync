import os
from pathlib import Path
from time import sleep
from selenium import webdriver

# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

css_selector = "[aria-label='Download'], [data-id='download']"


def check_zip(download_dir) -> bool:
    return (
        os.listdir(download_dir) != [] and list(Path(download_dir).glob("*.part")) == []
    )


def get_files(sharepoint_download_url, download_dir):
    print(f"> {download_dir = }")
    if not Path(download_dir).exists():
        Path(download_dir).mkdir()

    options = Options()
    options.add_argument("--headless")
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir", download_dir)
    options.set_preference(
        "browser.helperApps.neverAsk.saveToDisk", "application/x-gzip"
    )

    print(">>> going to website")
    driver = webdriver.Firefox(options=options)
    driver.get(sharepoint_download_url)

    print(">>> waiting for download button")
    _ = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
    )

    print(">>> clicking download button")
    elem = driver.find_element(By.CSS_SELECTOR, css_selector)
    elem.click()

    print(">>> waiting for zip file to download")
    _ = WebDriverWait(driver, 60).until(lambda _: check_zip(download_dir))
    sleep(5)
    driver.quit()
