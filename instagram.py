import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import requests
import os
import json
import cv2
import subprocess

chrome_options = Options()
chrome_options.add_argument("--incognito")
capabilities = webdriver.DesiredCapabilities.CHROME
capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}

    
driver = webdriver.Chrome(options=chrome_options) 
driver.start_session(capabilities)
url = 'https://www.instagram.com/'
username = "lalalalisa_m"
driver.get(url)
wait = WebDriverWait(driver, 10)

folder_path = os.path.join('instagram', username)
os.makedirs(folder_path, exist_ok=True)

time.sleep(5)
email_area = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div[1]/div[1]/div/label/input')
email_area.send_keys('not.in.bro')
# email_area.send_keys('for.instagram.niku@gmail.com')

time.sleep(3)
password_area = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div[1]/div[2]/div/label/input')
password_area.send_keys('hulk15right')
# password_area.send_keys('r3d!mi')

time.sleep(3)
login = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginForm"]/div[1]/div[3]' )))
login.click()
time.sleep(10)

  
def get_links():

    links = []
    images = []
    reels = []
    
    driver.execute_script(f"window.open('{url}{username}', '_blank');")
    print(f'profile of {username} opened')
    driver.close()
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[-1])
    time.sleep(5)

    posts = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[3]/ul/li[1]/div/span/span').text
    posts = posts.split(',')
    posts = ''.join(posts)
    posts = int(posts)
    print(posts)

    while True:
        try:
            post_area = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/div[2]')
            image_element = post_area.find_elements(By.TAG_NAME, 'a')
            pre_post_length = len(links)

            for element in image_element:
                link = element.get_attribute("href")
                if link not in links:
                    links.append(link)

            driver.execute_script("window.scrollBy(0, 1000);")  
            time.sleep(3)
            post_post_length = len(links)
            
            if pre_post_length == post_post_length:
                if posts != len(links):
                    print("total posts not equal to number of posts captured")

                else:
                    print("total posts equal to number of posts captured")

                # links.reverse()
                for link in links:
                    if link.split('/')[4] == 'p':
                        images.append(link)

                    else:
                        reels.append(link)

                print(f'number of image posts: {len(images)}')
                print(f'number of reels posts: {len(reels)}')
                break

        except:
            print('exception occured while collecting post links')
            time.sleep(0.5)
            driver.refresh()
            pass

    return images, reels


def get_image(urls_list):

    image_links = []
    video_links = []
    post_count = 1

    for url in urls_list:

        driver.execute_script(f"window.open('{url}', '_blank');")
        print(f'post {post_count} opened of {username}')
        n_b = None
        image_count = 0

        driver.close()
        window_handles = driver.window_handles
        driver.switch_to.window(window_handles[-1])
        time.sleep(4)

        image_count_element = driver.find_elements(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div[2]/div[1]/article/div/div[1]/div/div[2]/div')
        image_in_post = len(image_count_element)
        
        while True:
            try:
                image_card_element = driver.find_elements(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div[2]/div[1]/article/div/div[1]/div/div[1]')
                
                for card in image_card_element:
                    time.sleep(1)
                    image_element = card.find_elements(By.TAG_NAME, 'img')
                    video_element = card.find_elements(By.TAG_NAME, 'video')

                for image in image_element:
                    img_src = image.get_attribute('src')

                    if img_src not in image_links:
                        image_links.append(img_src)
                        print(f'image captured {len(image_links)}')
                        image_count += 1

                for video in video_element:
                    vid_src = video.get_attribute('src')

                    if vid_src not in video_links:
                        video_links.append(vid_src)
                        print(f'video captured {len(video_links)}')
                
                buttons = driver.find_elements(By.TAG_NAME, 'button')

                for button in buttons:
                    next_button = button.get_attribute('aria-label')

                    if next_button == 'Next':
                        n_b = button
                        button.click()

                if n_b not in buttons:
                    break

            except Exception as e:
                print('Exception occured during capturing image links')
                driver.refresh()
                time.sleep(2)
                pass
        if image_in_post == 0:
            print(f'{image_count} image in post {post_count}')
        elif image_count == image_in_post:
            print(f'{image_count} images in post {post_count}')
        else:
            print(f'{image_in_post} images in post {post_count}')
            print(f'{image_count} images saved in post {post_count}')
            print(f'not all images were saved in post {post_count}')
        post_count += 1

    print(f'video_count: {len(video_links)}')
    print(f'image_count: {len(image_links)}')

    return image_links, video_links


def save_image(image_link):

    number = 1
    for link in image_link:
        try:
            response = requests.get(link, stream=True)
            response.raw.decode_content = True  # Ensure correct decoding
            file_name = f'image_{number}.jpg'
            user_path = os.path.join(folder_path, 'images')
            os.makedirs(user_path, exist_ok=True)
            file_path = os.path.join(user_path, file_name)

            # Save the image to a file
            with open(file_path, 'wb') as f:  # Choose the appropriate file extension (jpg, png, etc.)
                f.write(response.content)
                print(f'{file_name} saved')

            number += 1
        
        except:
            print(f'Error occored while saving image {number+1}')
            pass


def save_video():
    pass


def save_reels(reels):
    user_path = os.path.join(folder_path, 'reels')
    os.makedirs(user_path, exist_ok=True)
    try:
        for reel in reels:
            for number, link in reel.items():
                video = link['video']
                audio = link['audio']
                file_name = f'reel_{number}.mp4'
                file_path = os.path.join(user_path, file_name)
                temp = 'temp'
                os.makedirs(temp, exist_ok=True)
                video_path = os.path.join(temp, 'video.mp4')
                audio_path = os.path.join(temp, 'audio.mp4')

                if audio == None:
                    response = requests.get(video, stream=True)
                    if response.status_code == 200:
                        with open(file_path, "wb") as f:
                            f.write(response.content)
                            print(f"{file_name} saved")

                else:
                    response = requests.get(video, stream=True)
                    if response.status_code == 200:
                        with open(video_path, "wb") as f:
                            f.write(response.content)
                            print(f"{video_path} saved")

                    response = requests.get(audio, stream=True)
                    if response.status_code == 200:
                        with open(audio_path, "wb") as f:
                            f.write(response.content)
                            print(f"{audio_path} saved")

                    ffmpeg_command = [
                                'ffmpeg',
                                '-i', video_path,
                                '-i', audio_path,
                                '-c:v', 'copy',  # Copy video stream without re-encoding
                                '-c:a', 'aac',  # Re-encode audio stream (optional, adjust codec as needed)
                                '-map', '0:v:0',  # Map video stream from the first input
                                '-map', '1:a:0',  # Map audio stream from the second input
                                file_path
                            ]
                    subprocess.run(ffmpeg_command, check=True)
            subprocess.run(["rmdir", "/s", "/q", temp], shell=True, check=True)
    except Exception as e:
        print(e)
        print('Error while saving reels')
        pass


def filter_reels_link(links, number):
    reels = {}
    audio_exists = False
    video_exists = False
    count = 1
    bitrate_saved = 0
    width_saved = 0
    temp = 'temp'
    os.makedirs(temp, exist_ok=True)
    for url in links:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            file_name = f'reel_{count}.mp4'
            file_path = os.path.join(temp, file_name)
            with open(file_path, "wb") as f:
                f.write(response.content)
                count += 1
                print(f"{file_name} saved")

            # Use OpenCV to get video details
            cap = cv2.VideoCapture(file_path)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            bitrate = float(cap.get(cv2.CAP_PROP_BITRATE))
            cap.release()

            # if not audio_exists and not video_exists:
            if width == 0:
                audio = url
                audio_exists = True
                # print('audio file', audio)
            if width >= width_saved and bitrate > bitrate_saved:
                bitrate_saved = bitrate
                width_saved = width
                video = url
                video_exists = True
                # print('video file', video)
    
    if audio_exists and video_exists:
        src = {
            'video': video,
            'audio': audio
        }

    elif not audio_exists and video_exists:
        src = {
            'video': video,
            'audio': None
        }
    else:
        src = {
            'video': None,
            'audio': None
        }
    
    reels[number] = src
    subprocess.run(["rmdir", "/s", "/q", temp], shell=True, check=True)
    return reels
    pass


def get_reels_links(links):
    number = 1
    reels = []
    reels_link = []
    for link in links:
        driver.execute_script(f"window.open('{link}', '_blank');")
        driver.close()
        window_handles = driver.window_handles
        driver.switch_to.window(window_handles[-1])
        print(f'post {number} opened of {username}')
        time.sleep(5)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div[2]/div[1]/article/div/div[1]/div')))
        
        performance_logs = driver.get_log('performance')
        video_url_links = []

        for entry in performance_logs:
            message = json.loads(entry['message'])['message']

            # Check for network requests
            if message['method'] == 'Network.responseReceived':
                
                mime_type = message['params']['response']['mimeType']
                if mime_type == 'video/mp4':
                # Access request details
                    # request_id = message['params']['requestId']
                    url = message['params']['response']['url']
                    url = url.split('&bytestart')[0]
                    if url not in reels:
                        video_url_links.append(url)
                        reels.append(url)
        
        filtered_links = filter_reels_link(video_url_links, number)
        reels_link.append(filtered_links)
        number += 1
    return reels_link


def get_video_links(links):
    pass


def main():
    images_links, reel_links = get_links()
    # images_links = ["https://www.instagram.com/rubyfnql/p/DFVy5j7zOqH/", "https://www.instagram.com/rubyfnql/p/DFSzzJdTXs-/", "https://www.instagram.com/rubyfnql/p/DEAg5Xyz7eb/", "https://www.instagram.com/rubyfnql/p/DD7d2uMTMEd/", "https://www.instagram.com/rubyfnql/p/DDy1RqNTfyc/", "https://www.instagram.com/rubyfnql/p/DDxbpAwzXom/", "https://www.instagram.com/rubyfnql/p/DDWo0N0TAjo/", "https://www.instagram.com/rubyfnql/p/DDU9y8XT5e-/", "https://www.instagram.com/rubyfnql/p/DDT_wDkz64i/", "https://www.instagram.com/rubyfnql/p/DC4Qsajzoyn/", "https://www.instagram.com/rubyfnql/p/DC4OXrrzD_v/", "https://www.instagram.com/rubyfnql/p/DCq-jm6zl4-/", "https://www.instagram.com/rubyfnql/p/DCYaJdoT23N/", "https://www.instagram.com/rubyfnql/p/DCP64QHzi7j/", "https://www.instagram.com/rubyfnql/p/DCO1NZyTpP8/", "https://www.instagram.com/rubyfnql/p/DCKHG3EzfGh/", "https://www.instagram.com/rubyfnql/p/DB1VxSOTWdq/", "https://www.instagram.com/rubyfnql/p/DBx_7pexefN/", "https://www.instagram.com/rubyfnql/p/DBxCpUKz4LU/", "https://www.instagram.com/rubyfnql/p/DBo3F0STS55/", "https://www.instagram.com/rubyfnql/p/DBPSPuMz2y_/", "https://www.instagram.com/rubyfnql/p/DBEoolCzcZ8/", "https://www.instagram.com/rubyfnql/p/DA5PvuHTLRa/", "https://www.instagram.com/rubyfnql/p/DAOa2_gTsa3/", "https://www.instagram.com/rubyfnql/p/DAMrRvxTT9n/", "https://www.instagram.com/rubyfnql/p/C_2-GWTT-lP/", "https://www.instagram.com/rubyfnql/p/C_pwPaqTg5V/", "https://www.instagram.com/rubyfnql/p/C_hS4uxxRzp/", "https://www.instagram.com/rubyfnql/p/C_bGuaCzbAz/", "https://www.instagram.com/rubyfnql/p/C_SIQsBx6Ae/", "https://www.instagram.com/rubyfnql/p/C_PmD7zR244/", "https://www.instagram.com/rubyfnql/p/C_NiqKNTvEG/", "https://www.instagram.com/rubyfnql/p/C_FmmB_RBYy/", "https://www.instagram.com/rubyfnql/p/C-g18BrTX9f/", "https://www.instagram.com/rubyfnql/p/C-geA_QzOdu/", "https://www.instagram.com/rubyfnql/p/C-H-9fuTVYx/", "https://www.instagram.com/rubyfnql/p/C83mlRux7Nv/", "https://www.instagram.com/rubyfnql/p/C8y82k4xqe2/", "https://www.instagram.com/rubyfnql/p/C8rIBBORtw8/", "https://www.instagram.com/rubyfnql/p/C71le3cS8Qr/", "https://www.instagram.com/rubyfnql/p/C7i_b_zRtTL/", "https://www.instagram.com/rubyfnql/p/C6jPgiixcJj/", "https://www.instagram.com/rubyfnql/p/C6jOH7xR55z/", "https://www.instagram.com/rubyfnql/p/C6c7D2SRph9/", "https://www.instagram.com/rubyfnql/p/C6c6Zs1x9bI/", "https://www.instagram.com/rubyfnql/p/C6bZfTQxjz4/", "https://www.instagram.com/rubyfnql/p/C58FYpmRy3G/", "https://www.instagram.com/rubyfnql/p/C54J-kLhq55/", "https://www.instagram.com/rubyfnql/p/C5ydoLySqXU/", "https://www.instagram.com/rubyfnql/p/C5b9-k_y1YX/", "https://www.instagram.com/rubyfnql/p/C49pXAQxY5I/", "https://www.instagram.com/rubyfnql/p/C4nvPwVxmxY/", "https://www.instagram.com/rubyfnql/p/C30AiV_xRwz/", "https://www.instagram.com/rubyfnql/p/C3V3ZzThSct/", "https://www.instagram.com/rubyfnql/p/C3Vv6DBBdll/", "https://www.instagram.com/rubyfnql/p/C2nOujKPr8v/", "https://www.instagram.com/rubyfnql/p/C2hW_5PRLad/", "https://www.instagram.com/rubyfnql/p/C1_V1emRrhx/", "https://www.instagram.com/rubyfnql/p/C15NYu-h4A3/", "https://www.instagram.com/rubyfnql/p/C0oTEb5RYga/", "https://www.instagram.com/rubyfnql/p/C0WReXFxn53/", "https://www.instagram.com/rubyfnql/p/C0UmxYPBhF1/", "https://www.instagram.com/rubyfnql/p/C0PuLQwBApr/", "https://www.instagram.com/rubyfnql/p/Cy5aKdsxq7A/", "https://www.instagram.com/rubyfnql/p/CyQIsI4R4ds/", "https://www.instagram.com/rubyfnql/p/CyKwcMrxefd/", "https://www.instagram.com/rubyfnql/p/CxmBnRCB2E2/", "https://www.instagram.com/rubyfnql/p/Cw223UnpLv5/", "https://www.instagram.com/rubyfnql/p/CtyGnjLxt5h/", "https://www.instagram.com/rubyfnql/p/CtvtuxwxiKA/", "https://www.instagram.com/rubyfnql/p/CsGvq6Hx19r/", "https://www.instagram.com/rubyfnql/p/Cq8A74xJMYp/", "https://www.instagram.com/rubyfnql/p/Co8VRHHh936/", "https://www.instagram.com/rubyfnql/p/Co2SiRTr062/", "https://www.instagram.com/rubyfnql/p/Cobm3nKp42j/", "https://www.instagram.com/rubyfnql/p/CoSGZHkpXcY/", "https://www.instagram.com/rubyfnql/p/CoMs0GoJHKD/", "https://www.instagram.com/rubyfnql/p/CnUnLG_BwOy/", "https://www.instagram.com/rubyfnql/p/Cm2rnnwpCYJ/", "https://www.instagram.com/rubyfnql/p/CjAboa5pLkB/", "https://www.instagram.com/rubyfnql/p/Ci3J2HxBibj/", "https://www.instagram.com/rubyfnql/p/CifTJ8LJ0DV/", "https://www.instagram.com/rubyfnql/p/CicMzzOJfLQ/", "https://www.instagram.com/rubyfnql/p/CFysllVMZdm/"]
    image_src, video_src = get_image(images_links)
    
    # save_video(video_src)
    # reel_links = ["https://www.instagram.com/rubyfnql/reel/DE0TZo5TcBJ/", "https://www.instagram.com/rubyfnql/reel/DDrfvtWTC4j/", "https://www.instagram.com/rubyfnql/reel/DCfM2auMAis/", "https://www.instagram.com/rubyfnql/reel/DCfK_o_swcy/", "https://www.instagram.com/rubyfnql/reel/DCTz_p4MFfv/", "https://www.instagram.com/rubyfnql/reel/DB3xZKSM1Cy/", "https://www.instagram.com/rubyfnql/reel/C-owGHtMJ-_/", "https://www.instagram.com/rubyfnql/reel/C1zqCbRRa2h/"]
    reels_src = get_reels_links(reel_links)
    # reels_src = [{1: {'video': 'https://instagram.fblr2-3.fna.fbcdn.net/o1/v/t2/f2/m367/AQOsPI1yABMk4-QbZvmd1cWdQjI8mopP9_sbiJ28MengzmobXOHBuQsZBhzrILGFxWmNQwTeGnzhZtcnLr6NCoTCzc8iYGxdCnz9PgOIHuZz.mp4?strext=1&_nc_cat=104&_nc_sid=9ca052&_nc_ht=instagram.fblr2-3.fna.fbcdn.net&_nc_ohc=IRlM1o5L6z4Q7kNvgHLADZI&efg=eyJ2ZW5jb2RlX3RhZyI6ImlnLXhwdmRzLmNsaXBzLmMyLUMzLmRhc2hfcjJldmV2cDktcjFnZW4ydnA5X3E5MCIsInZpZGVvX2lkIjpudWxsLCJjbGllbnRfbmFtZSI6ImlnIiwib2lsX3VybGdlbl9hcHBfaWQiOjkzNjYxOTc0MzM5MjQ1OSwidXJsZ2VuX3NvdXJjZSI6Ind3dyJ9&ccb=9-4&_nc_zt=28&oh=00_AYApou6vUenj7ptKjehiQoajiUeM2m-CKuzZVGpL6bMKaQ&oe=67A54C59', 'audio': None}}, {2: {'video': 'https://instagram.fblr2-2.fna.fbcdn.net/o1/v/t2/f2/m367/AQNN8ImtX5x4sP-Eykmdyakky4E3CH6Kg1JV3CEhYWHR59vVt5_bnGejfPEenLCH54jd1nXol_9ZCaT4qPg6A2RSnKMnJNthYd9exkoXTb4g.mp4?strext=1&_nc_cat=109&_nc_sid=9ca052&_nc_ht=instagram.fblr2-2.fna.fbcdn.net&_nc_ohc=v8Kl5tlB1dIQ7kNvgFPsi9T&efg=eyJ2ZW5jb2RlX3RhZyI6ImlnLXhwdmRzLmNsaXBzLmMyLUMzLmRhc2hfcjJldmV2cDktcjFnZW4ydnA5X3E5MCIsInZpZGVvX2lkIjpudWxsLCJjbGllbnRfbmFtZSI6ImlnIiwib2lsX3VybGdlbl9hcHBfaWQiOjkzNjYxOTc0MzM5MjQ1OSwidXJsZ2VuX3NvdXJjZSI6Ind3dyJ9&ccb=9-4&_nc_zt=28&oh=00_AYDUXiUPytuqADUsTfISw_P2SmojMeuXJg_03J15GoBAsg&oe=67A56ECE', 'audio': 'https://instagram.fblr2-3.fna.fbcdn.net/o1/v/t16/f2/m69/AQM21wGvX8KBUDYDy7nDea65dCSDY7IPkbAYoVUmLuF2IuB-c-xCs3nXa1T2MDZXcyF2ZXkgdJ47HJjNoAiI_ELt.mp4?strext=1&_nc_cat=102&_nc_sid=9ca052&_nc_ht=instagram.fblr2-3.fna.fbcdn.net&_nc_ohc=U7rVKO-QrEcQ7kNvgESotPb&efg=eyJ2ZW5jb2RlX3RhZyI6ImlnLXhwdmRzLmNsaXBzLmMyLUMzLmRhc2hfbG5faGVhYWNfdmJyM19hdWRpbyIsInZpZGVvX2lkIjpudWxsLCJjbGllbnRfbmFtZSI6ImlnIiwib2lsX3VybGdlbl9hcHBfaWQiOjkzNjYxOTc0MzM5MjQ1OSwidXJsZ2VuX3NvdXJjZSI6Ind3dyJ9&ccb=9-4&_nc_zt=28&oh=00_AYCBcM9n9tE_l_da-nrPXw4srE3xn0eKzb75NCjuMKk1uw&oe=67A565E3'}}, {3: {'video': 'https://instagram.fblr2-3.fna.fbcdn.net/o1/v/t16/f2/m69/AQNyp1Qfq7X3rF6RMD9wj5Fp1BV14A8ntQzC4sjusfP3G0a-cpeDX4OfinIze_xeup06Ne2_qw_4DvT5CIM0-eiQ.mp4?strext=1&_nc_cat=101&_nc_sid=9ca052&_nc_ht=instagram.fblr2-3.fna.fbcdn.net&_nc_ohc=nVKyjUIQQwQQ7kNvgGs4lju&efg=eyJ2ZW5jb2RlX3RhZyI6ImlnLXhwdmRzLmNsaXBzLmMyLUMzLmRhc2hfcjJldmV2cDktcjFnZW4ydnA5X3E5MCIsInZpZGVvX2lkIjpudWxsLCJjbGllbnRfbmFtZSI6ImlnIiwib2lsX3VybGdlbl9hcHBfaWQiOjkzNjYxOTc0MzM5MjQ1OSwidXJsZ2VuX3NvdXJjZSI6Ind3dyJ9&ccb=9-4&_nc_zt=28&oh=00_AYDCg01wtHREKcRTPYA8NNEMdH6NDrud1IPEwa_DBXZlcQ&oe=67A54ACE', 'audio': 'https://instagram.fblr2-2.fna.fbcdn.net/o1/v/t16/f2/m69/AQMU_Ec9SeLqRkRQInevyTsBOw_vetVEadG7BAtwEMUoHXk94kvmpT5x9-cENqTu-7XpeEQUxk47CZsa4-jAqJQ9.mp4?strext=1&_nc_cat=100&_nc_sid=9ca052&_nc_ht=instagram.fblr2-2.fna.fbcdn.net&_nc_ohc=g6wWMlQuzvwQ7kNvgH6H6s4&efg=eyJ2ZW5jb2RlX3RhZyI6ImlnLXhwdmRzLmNsaXBzLmMyLUMzLmRhc2hfbG5faGVhYWNfdmJyM19hdWRpbyIsInZpZGVvX2lkIjpudWxsLCJjbGllbnRfbmFtZSI6ImlnIiwib2lsX3VybGdlbl9hcHBfaWQiOjkzNjYxOTc0MzM5MjQ1OSwidXJsZ2VuX3NvdXJjZSI6Ind3dyJ9&ccb=9-4&_nc_zt=28&oh=00_AYA9nPVQjrsUIv1Pmwov70EXIQPQa00Q1xMM8YJN0PZSrg&oe=67A56C71'}}, {4: {'video': 'https://instagram.fblr2-2.fna.fbcdn.net/o1/v/t16/f2/m69/AQM6Td1rIVmMljJYbs0slLKuexj3otmETdqhUTUCVS5kdUsIvWiViAjXCne9f7ljxCGaQ03o0mCoOiJYQ4-DO-A7.mp4?strext=1&_nc_cat=110&_nc_sid=9ca052&_nc_ht=instagram.fblr2-2.fna.fbcdn.net&_nc_ohc=ALqhjzRjNJYQ7kNvgFPoWBf&efg=eyJ2ZW5jb2RlX3RhZyI6ImlnLXhwdmRzLmNsaXBzLmMyLUMzLmRhc2hfcjJldmV2cDktcjFnZW4ydnA5X3E5MCIsInZpZGVvX2lkIjpudWxsLCJjbGllbnRfbmFtZSI6ImlnIiwib2lsX3VybGdlbl9hcHBfaWQiOjkzNjYxOTc0MzM5MjQ1OSwidXJsZ2VuX3NvdXJjZSI6Ind3dyJ9&ccb=9-4&_nc_zt=28&oh=00_AYAC6WyJbRLQLLWHVhe9rieI5EjN5banXS6TUBDwuXDoQQ&oe=67A55F9F', 'audio': 'https://instagram.fblr2-3.fna.fbcdn.net/o1/v/t16/f2/m69/AQNPmZRsC3RN9Fs5sJZfC3kgefk9MbAoaurIsij-9LzvxoDXA-q6-GdxjfRxRFKW6flaJcrP-lylVr167NvS8u5v.mp4?strext=1&_nc_cat=101&_nc_sid=9ca052&_nc_ht=instagram.fblr2-3.fna.fbcdn.net&_nc_ohc=0eW-tJkRLxoQ7kNvgE8NeCy&efg=eyJ2ZW5jb2RlX3RhZyI6ImlnLXhwdmRzLmNsaXBzLmMyLUMzLmRhc2hfbG5faGVhYWNfdmJyM19hdWRpbyIsInZpZGVvX2lkIjpudWxsLCJjbGllbnRfbmFtZSI6ImlnIiwib2lsX3VybGdlbl9hcHBfaWQiOjkzNjYxOTc0MzM5MjQ1OSwidXJsZ2VuX3NvdXJjZSI6Ind3dyJ9&ccb=9-4&_nc_zt=28&oh=00_AYDK6U4OULEEllaWhLKPRlmebEP4qXWS_-vtqGzlNL8gWA&oe=67A5752A'}}, {5: {'video': 'https://instagram.fblr2-2.fna.fbcdn.net/o1/v/t16/f2/m69/AQMVafiA_uBUDeGZRKpHeqgglE6LT7HSXfuD6pPwQI4NSbindNCoOdAJ6j8l0oXFsaUtLMP6TCXZw0Z_v4BGQg50.mp4?strext=1&_nc_cat=110&_nc_sid=9ca052&_nc_ht=instagram.fblr2-2.fna.fbcdn.net&_nc_ohc=02Bj4sGuVtQQ7kNvgGpcnh7&efg=eyJ2ZW5jb2RlX3RhZyI6ImlnLXhwdmRzLmNsaXBzLmMyLUMzLmRhc2hfcjJldmV2cDktcjFnZW4ydnA5X3E5MCIsInZpZGVvX2lkIjpudWxsLCJjbGllbnRfbmFtZSI6ImlnIiwib2lsX3VybGdlbl9hcHBfaWQiOjkzNjYxOTc0MzM5MjQ1OSwidXJsZ2VuX3NvdXJjZSI6Ind3dyJ9&ccb=9-4&_nc_zt=28&oh=00_AYBBsA6ldzjAWTkMQX3I3jY75I8mYUBZnN76wJ8KUazbnQ&oe=67A55EE7', 'audio': 'https://instagram.fblr2-3.fna.fbcdn.net/o1/v/t16/f2/m69/AQMb83EC4-TW7Gj275PT0qhbOofeOehSolSAAWzVT35jlIZ9w1L9vfGMt8fRZHNPVzLH-cFpldqCHobiwbST0Mqg.mp4?strext=1&_nc_cat=106&_nc_sid=9ca052&_nc_ht=instagram.fblr2-3.fna.fbcdn.net&_nc_ohc=wByHD2y60y8Q7kNvgFWRf1s&efg=eyJ2ZW5jb2RlX3RhZyI6ImlnLXhwdmRzLmNsaXBzLmMyLUMzLmRhc2hfbG5faGVhYWNfdmJyM19hdWRpbyIsInZpZGVvX2lkIjpudWxsLCJjbGllbnRfbmFtZSI6ImlnIiwib2lsX3VybGdlbl9hcHBfaWQiOjkzNjYxOTc0MzM5MjQ1OSwidXJsZ2VuX3NvdXJjZSI6Ind3dyJ9&ccb=9-4&_nc_zt=28&oh=00_AYD_TnzR27I5fVEPoJNHJaRNNG6R8QKEPsaECj2AKWtlNg&oe=67A5507F'}}, {6: {'video': 'https://instagram.fblr2-3.fna.fbcdn.net/o1/v/t2/f2/m367/AQPBvXNPRY3qiC8zbllNGyGZRITskCRHfnV5eoiX6vVNzRdbxKAjwaRobfdmTXQcBNhBhTc-9hLYFTOjfO_ZU8EUQsHuoCJT8ESPly1Ld_6D.mp4?strext=1&_nc_cat=106&_nc_sid=9ca052&_nc_ht=instagram.fblr2-3.fna.fbcdn.net&_nc_ohc=2FwkWJygnu0Q7kNvgEEV32a&efg=eyJ2ZW5jb2RlX3RhZyI6ImlnLXhwdmRzLmNsaXBzLmMyLUMzLmRhc2hfcjJldmV2cDktcjFnZW4ydnA5X3E5MCIsInZpZGVvX2lkIjpudWxsLCJjbGllbnRfbmFtZSI6ImlnIiwib2lsX3VybGdlbl9hcHBfaWQiOjkzNjYxOTc0MzM5MjQ1OSwidXJsZ2VuX3NvdXJjZSI6Ind3dyJ9&ccb=9-4&_nc_zt=28&oh=00_AYA2E5frSiixWPRWn_JiF1eeEp8KqaJoUZO7v2qHcKfw_Q&oe=67A562E3', 'audio': 'https://instagram.fblr2-3.fna.fbcdn.net/o1/v/t16/f2/m69/AQNvgITPkbo3DPLMZ1H1CxZFHWTRcjDQY3LAE4wmNJBi92Ij7DGk9uz2Ecw9b28X_jGBSCKboF7OYpgJX88HkTHq.mp4?strext=1&_nc_cat=104&_nc_sid=9ca052&_nc_ht=instagram.fblr2-3.fna.fbcdn.net&_nc_ohc=2yNkx6PAuCMQ7kNvgGPLcUv&efg=eyJ2ZW5jb2RlX3RhZyI6ImlnLXhwdmRzLmNsaXBzLmMyLUMzLmRhc2hfbG5faGVhYWNfdmJyM19hdWRpbyIsInZpZGVvX2lkIjpudWxsLCJjbGllbnRfbmFtZSI6ImlnIiwib2lsX3VybGdlbl9hcHBfaWQiOjkzNjYxOTc0MzM5MjQ1OSwidXJsZ2VuX3NvdXJjZSI6Ind3dyJ9&ccb=9-4&_nc_zt=28&oh=00_AYAEvtZXl1eGBqZEhNY_mH6WoSCX0VCxvXZ4c2ZdoPxtgg&oe=67A5519D'}}, {7: {'video': 'https://instagram.fblr2-3.fna.fbcdn.net/o1/v/t16/f2/m69/AQPaXu0awuR8zKhP4Uh2NxJqPGlm6lv4IqF9Ov-ZUPL98ZQ6e3f5Ldn9HxAz3lOO8jxE6z_IpMq3BQ-EfTn3LQmF.mp4?strext=1&_nc_cat=101&_nc_sid=9ca052&_nc_ht=instagram.fblr2-3.fna.fbcdn.net&_nc_ohc=pU5YeKdYNLsQ7kNvgG-AQHY&efg=eyJ2ZW5jb2RlX3RhZyI6ImlnLXhwdmRzLmNsaXBzLmMyLUMzLmRhc2hfcjJldmV2cDktcjFnZW4ydnA5X3E5MCIsInZpZGVvX2lkIjpudWxsLCJjbGllbnRfbmFtZSI6ImlnIiwib2lsX3VybGdlbl9hcHBfaWQiOjkzNjYxOTc0MzM5MjQ1OSwidXJsZ2VuX3NvdXJjZSI6Ind3dyJ9&ccb=9-4&_nc_zt=28&oh=00_AYB6Yd5j6K1-raisKvVmaihQmaDr3gRRsSHeivBHqpwIFQ&oe=67A5537A', 'audio': None}}, {8: {'video': 'https://instagram.fblr2-3.fna.fbcdn.net/o1/v/t2/f2/m82/AQOKO_bjYEvhHCw0EUe723rsdsOM0ZmxqnFxtp7V9CrDejzJP7s9hr0vqjbxSKl4DZJUjdq5ZDiw-fbvfdgblXK0xjnDrBwZsTgOBr8dKCm_.mp4?strext=1&_nc_cat=103&_nc_sid=9ca052&_nc_ht=instagram.fblr2-3.fna.fbcdn.net&_nc_ohc=TXvwutGehYwQ7kNvgHmE5cQ&efg=eyJ2ZW5jb2RlX3RhZyI6ImlnLXhwdmRzLmNsaXBzLmMyLUMzLmRhc2hfYmFzZWxpbmVfMV92MSIsInZpZGVvX2lkIjpudWxsLCJjbGllbnRfbmFtZSI6ImlnIiwib2lsX3VybGdlbl9hcHBfaWQiOjkzNjYxOTc0MzM5MjQ1OSwidXJsZ2VuX3NvdXJjZSI6Ind3dyJ9&ccb=9-4&_nc_zt=28&oh=00_AYB9-7ZDQ3pTD6uDLL4_kUQLwQ2nVCZwtasY11UfAL0x7g&oe=67A154C8', 'audio': 'https://instagram.fblr2-3.fna.fbcdn.net/o1/v/t16/f2/m69/AQNnm0uEGkLjHduz-3feFF5GSMBtSDf6fcSdsmZgIYIj2G7rjS4Uv5T8hE89Rce-GRdNdBzINbtYNM0NasQu5ngg.mp4?strext=1&_nc_cat=103&_nc_sid=9ca052&_nc_ht=instagram.fblr2-3.fna.fbcdn.net&_nc_ohc=hzzW3v5GTsQQ7kNvgHhIQ0-&efg=eyJ2ZW5jb2RlX3RhZyI6ImlnLXhwdmRzLmNsaXBzLmMyLUMzLmRhc2hfYmFzZWxpbmVfYXVkaW9fdjEiLCJ2aWRlb19pZCI6bnVsbCwiY2xpZW50X25hbWUiOiJpZyIsIm9pbF91cmxnZW5fYXBwX2lkIjo5MzY2MTk3NDMzOTI0NTksInVybGdlbl9zb3VyY2UiOiJ3d3cifQ%3D%3D&ccb=9-4&_nc_zt=28&oh=00_AYCFVINDKO7PAyjWDxFW18P5reR6C-S1uCWi_zAyYLQRMQ&oe=67A574BC'}}]
    # print(reels_src)
    

    user_links = { 
        username: {
            'posts': {
                'images_posts': images_links, # images_links,
                'reels_posts': reel_links # reel_links
            },
            'images_posts': {
                'images_src': image_src,
                'video_src': {}
            },
            'reels_posts': reels_src,
            'count': {
                'images': len(images_links),
                'video': len([]),
                'reels': len(reel_links)
            }
        }
    }

    # Convert dictionary to JSON string
    json_string = json.dumps(user_links)
    file_path = os.path.join(folder_path, f'{username}.json')

    # Save JSON string to a file
    with open(file_path, 'w') as f:
        f.write(json_string)

    save_image(image_src)
    save_reels(reels_src)

if __name__ == "__main__":
    main()
