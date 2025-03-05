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
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    # Open Chrome Browser Window
    try:
        with Chrome(options=options) as driver:
            wait = WebDriverWait(driver, 15)
            # Hit the url
            driver.get(url)

            # wait until some part of page is loaded and then scroll down.
            time.sleep(2)
            
            title = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="title"]/h1/yt-formatted-string'))).text
            time.sleep(1)

            #Scrape the elements containing information about likes and dislikes
            # try-except block required as some videos can make numbers private
            try:
                # //*[@id="top-level-buttons-computed"]/segmented-like-dislike-button-view-model/yt-smartimation/div/div/like-button-view-model/toggle-button-view-model/button-view-model/button/div[2]
                likes = driver.find_element(By.XPATH, '//*[@id="top-level-buttons-computed"]/segmented-like-dislike-button-view-model/yt-smartimation/div/div/like-button-view-model/toggle-button-view-model/button-view-model/button/div[2]').text
                # dislikes = elements[1].get_attribute("aria-label")
            except:
                pass
            # Check if "Show More" button is present for description
            # try-except required as some videos have short description and won't have show more button
            try:
                # If yes then press it to load whole description
                # //*[@id="expand"]
                expand_button = driver.find_element(By.XPATH, '//*[@id="expand"]')
                # Remove hidden attribute
                driver.execute_script("arguments[0].removeAttribute('hidden');", expand_button)

                # Scroll into view before clicking
                driver.execute_script("arguments[0].scrollIntoView(true);", expand_button)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", expand_button)
                time.sleep(2)
            except:
                print("Unable to click")
                pass

            # Loop over all parts of description and concatenate it to make a paragraph
            # //*[@id="description-inline-expander"]/yt-attributed-string/span
            description_parts = driver.find_elements(By.XPATH, '//*[@id="description-inline-expander"]/yt-attributed-string/span')
            for d in description_parts:
                description += d.text.strip().replace("\n", " ") + " "

            # Scrape the number of views and published date of the video
            # try-except required as some videos may not have views and date
            try:
                views = driver.find_element(By.XPATH, '//*[@id="info"]/span[1]').text
                date = driver.find_element(By.XPATH, '//*[@id="info"]/span[3]').text
            except:
                pass

            # //*[@id="info"]/a[1]
            hashtag_parts = driver.find_elements(By.XPATH, '//*[@id="info"]/a')

            for h in hashtag_parts:
                hashTags.append(h.text)

            try:
                wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
                time.sleep(2)
                # //*[@id="count"]/yt-formatted-string/span[1]
                number_of_comments = driver.find_element(By.CSS_SELECTOR, "ytd-comments div#title h2#count span").text
            except:
                pass

            new_url = driver.current_url
            
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
        if views:
            views = views.split()[0].replace(',', '')

        return {"vid_url": new_url, "Likes": likes, "Dislikes": dislikes, "Title": title, "Description": description, "Num_of_Views": views, "Date_of_Upload": date, "Number_of_Comments": number_of_comments, "Hashtags": hashTags}
    except Exception as e:
        print(e)
        return None
