import time
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_binary

def getInfo(url):
    # Initialize Vars
    hashTags = []
    likes = None
    dislikes = None
    title = ""
    description = ""
    views = None
    date = None
    number_of_comments = None
    new_url = url
    # comments = []

    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    # Open Chrome Browser Window
    try:
        with Chrome(options=options) as driver:
            wait = WebDriverWait(driver, 15)
            # Hit the url
            driver.get(url)

            # wait until some part of page is loaded and then scroll down.
            # time.sleep(2)
            # wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
            time.sleep(2)
            
            
            #Scrape the title of the video
            # title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text
            title = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/h1/yt-formatted-string'))).text
            # description_parts =  wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"div#description yt-formatted-string")))
            time.sleep(1)
            #Scrape the elements containing information about likes and dislikes
            # try-except block required as some videos can make numbers private
            try:
                elements = driver.find_elements_by_css_selector("a.yt-simple-endpoint.style-scope.ytd-toggle-button-renderer yt-formatted-string")
                likes = elements[0].get_attribute("aria-label")
                dislikes = elements[1].get_attribute("aria-label")
                # likes = driver.find_element(By.XPATH, '//*[@id="top-level-buttons-computed"]/ytd-toggle-button-renderer[1]/a').get_attribute("aria-label")
                print(likes)
                # dislikes = driver.find_element(By.XPATH, '//*[@id="top-level-buttons-computed"]/ytd-toggle-button-renderer[2]/a').get_attribute("aria-label")
            except:
                pass
            print(likes, dislikes)
            # Check if "Show More" button is present for description
            # try-except required as some videos have short description and won't have show more button
            try:
                # If yes then press it to load whole description
                driver.find_element_by_css_selector("tp-yt-paper-button#more").click()
            except:
                pass

            # Loop over all parts of description and concatenate it to make a paragraph
            description_parts = driver.find_elements_by_css_selector("div#description yt-formatted-string span")
            for d in description_parts:
                description += d.text.strip().replace("\n", " ") + " "
            
            # Scrape the number of views and published date of the video
            # No try-except required as all videos will have views and date
            # views = driver.find_element(By.CSS_SELECTOR,"div#count > ytd-video-view-count-renderer > span.view-count.style-scope.ytd-video-view-count-renderer").text
            views = driver.find_element(By.XPATH, '//*[@id="count"]/ytd-video-view-count-renderer/span[1]').text
            
            # date = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#date > yt-formatted-string.style-scope.ytd-video-primary-info-renderer"))).text
            date = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="info-strings"]/yt-formatted-string'))).text

            hashtag_parts = driver.find_elements_by_css_selector("yt-formatted-string.super-title a")

            for h in hashtag_parts:
                hashTags.append(h.text)

            try:
                wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
                time.sleep(2)
                number_of_comments = driver.find_element_by_css_selector("ytd-comments div#title h2#count span").text
            except:
                pass
        
            new_url = driver.current_url
            print(new_url)
            
            # if collectComments > 0:
            #     # Wait for loading page and then scroll down
            #     # wait for some time (1 sec) for slow internet connection
            #     commentsCollected = 0
            #     for item in range(20): 
            #         # Wait for loading page and then scroll down
            #         # wait for some time (1 sec) for slow internet connection
            #         time.sleep(1)
            #         wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
            #         time.sleep(1)
            #         # Check if comments start loading
            #         try:
            #             # If they do load then scroll down to load more comments
            #             commentsCollected = len(wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content-text"))))
            #             # print("Number of Comments Loaded : {}".format(commentsCollected))
            #             # If comments loaded passed requirec number then stop loading more
            #             if commentsCollected >= collectComments:
            #                 break
            #         except:
            #             # If comments do not load, then the comments are off. (Most probably)
            #             break
                
            #     # Wait for elements with id = "content-text" to be loaded
            #     # Then append all the texts to data
            #     if (commentsCollected > 0):
            #         for commentElem in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content-text")))[:200]:
            #             comments.append(commentElem.text)
        #return the info obtained on the video for metadata storage
        if likes:
            likes = likes.split()[0].replace(',', '')
        if dislikes:
            dislikes = dislikes.split()[0].replace(',', '')
        if number_of_comments:
            number_of_comments = number_of_comments.replace(',', '')
        views = views.split()[0].replace(',', '')

        return {"url": new_url, "Likes": likes, "Dislikes": dislikes, "Title": title, "Description": description, "Num_of_Views": views, "Date_of_Upload": date, "Number_of_Comments": number_of_comments, "Hashtags": hashTags}
    except:
        return None
