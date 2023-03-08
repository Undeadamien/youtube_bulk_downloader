"""
A script that automate the downloading of video from
https://ytmp3.nu/0/youtube-to-mp3
"""
from os import listdir, remove
from os.path import dirname, join
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

DOWNLOADER = "https://ytmp3.nu/0/youtube-to-mp3"

# folders to check for already downloaded file
DESTINATION_FOLDERS = ["C:\\Users\\Damien\\Downloads",
                       "C:\\Users\\Damien\\Music",
                       "C:\\Users\\Damien\\Desktop\\DRAWING_\\Documentation"]
URL_FOLDERS = [join(dirname(__file__), "urls_to_download\\mp3"),
               join(dirname(__file__), "urls_to_download\\mp4")]


def link_collector(folder):
    """Return the url link of every url shortcuts"""
    for file_ in listdir(folder):
        if file_.lower().endswith(".url"):
            with open(f"{folder}\\{file_}", "r", encoding="utf-8") as shortcut:
                for line in shortcut:
                    if line.startswith("URL"):
                        yield line[4:-1]


def download(link, format_):
    """Automate the interaction with the site"""
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    driver.get(DOWNLOADER)

    wait.until(EC.visibility_of_element_located
               ((By.XPATH, '//*[@id="url"]')))
    driver.find_element(By.XPATH, '//*[@id="url"]').send_keys(link)

    if format_ == "mp4":
        wait.until(EC.visibility_of_element_located
                   ((By.XPATH, '//*[@id="format"]')))
        driver.find_element(By.XPATH, '//*[@id="format"]').click()

    wait.until(EC.visibility_of_element_located
               ((By.XPATH, '//*[@id="form"]/form/input[3]')))
    driver.find_element(By.XPATH, '//*[@id="form"]/form/input[3]').click()

    wait.until(EC.visibility_of_element_located
               ((By.XPATH, '//*[@id="download"]/a[1]')))
    driver.find_element(By.XPATH, '//*[@id="download"]/a[1]').click()

    def wait_until_file_downloaded():
        """
        Call it self recursively every 5s,
        as long as there is a file downloading
        otherwise the driver would close
        """
        sleep(5)
        for file_ in listdir(DESTINATION_FOLDERS[0]):
            if "crdownload" in file_.lower():
                wait_until_file_downloaded()
    wait_until_file_downloaded()


def delete_used_urls():

    """
    Compare the name of each music file with the url of each URL file,
    if the two match delete the URL file
    """

    def simplified_title(title):
        """Simplify the title keeping only the words, return a list"""
        for element_to_delete in ["-", "(", ")", "[", "]", ".mp3", ".mp4"]:
            title = title.replace(element_to_delete, "")
        title = title.split()
        return title

    for url_folder in URL_FOLDERS:
        for folder in DESTINATION_FOLDERS:

            for url_file in [x for x in listdir(url_folder)
                             if x.lower().endswith(".url")]:

                for music_file in [x for x in listdir(folder)
                                   if x.lower().endswith((".mp3", ".mp4"))]:

                    if all([True if word.lower() in url_file.lower()
                            else False
                            for word in simplified_title(music_file)]):

                        remove(f"{url_folder}\\{url_file}")


def main():
    """
    Deleted already used urls,
    then download every urls from both folder one by one
    and finally delete used urls
    """

    delete_used_urls()  # to avoid duplicates
    for folder in URL_FOLDERS:
        for link in link_collector(folder):
            if "mp3" in folder:
                download(link, "mp3")
            elif "mp4" in folder:
                download(link, "mp4")
    delete_used_urls()  # clean up


if __name__ == "__main__":
    main()
