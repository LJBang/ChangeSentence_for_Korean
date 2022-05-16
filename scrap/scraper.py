from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import csv
import re
import saveposts

options = webdriver.ChromeOptions()


keywords = ["인문학", "철학", "글쓰기"]

options.add_argument('headless') # 창이 안뜨게
options.add_argument('--blink-settings=imagesEnabled=false') # 이미지 로딩 x
options.add_experimental_option("excludeSwitches", ["enable-logging"]) # usb에러
options.add_argument('incognito') # 시크릿 모드
options.add_argument('--start-maximized') #브라우저가 최대화된 상태로 실행
options.add_argument('--start-fullscreen') #브라우저가 풀스크린 모드(F11)로 실행


for keyword in keywords:
    driver = webdriver.Chrome("./chromedriver", options=options)
    WAIT_TIME = 2
    driver.implicitly_wait(WAIT_TIME)

    driver.get("https://brunch.co.kr/")

    search_box = driver.find_element(By.XPATH,
                '//*[@id="btnServiceMenuSearch"]')
    search_box.click()
    search_bar = driver.find_element(By.XPATH,
                '//*[@id="txt_search"]')
    search_bar.send_keys(keyword)
    search_bar.send_keys(Keys.RETURN)

    contents = []

    start_content = 1
    last_height = driver.execute_script("return document.body.scrollHeight")
    cnt = 0
    while cnt < 100:
        cnt += 1
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(WAIT_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

        # 글을 19개씩 확인
        print("brunch-{} ~ {}".format(start_content, start_content+19))
        for content in range(start_content, start_content+19):
            try:
                acting_point = driver.find_element(By.XPATH,
                    "//*[@id='resultArticle']/div/div[1]/div[2]/ul/li["+str(content)+"]/a/div[1]/strong")
                driver.execute_script("arguments[0].click();", acting_point)
            except:
                continue
            driver.switch_to.window(driver.window_handles[1])
            driver.get_window_position(driver.window_handles[1])
            driver.implicitly_wait(WAIT_TIME)
            
            not_magazine = True
            # 좋아요 수를 기준으로 거르기
            try:
                like_cnt = driver.find_element(By.XPATH,
                "/html/body/div[1]/div[2]/div[3]/div/div[2]/a[1]/span[2]")
                not_magazine = False
            except:
                like_cnt = driver.find_element(By.XPATH,
                "/html/body/div[1]/div[2]/div[2]/div/div[2]/a[1]/span[2]")
            
            like_cnt = int(like_cnt.text) if like_cnt.text else 0
            if like_cnt < 7 or not_magazine:
                time.sleep(WAIT_TIME)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                driver.get_window_position(driver.window_handles[0])
                continue
            
            content_text = ""
            try:
                div_p_elems = driver.find_elements_by_xpath(
                    "/html/body/div[3]/div[1]/div[2]/div[1]/p[@class='wrap_item item_type_text'] | /html/body/div[3]/div[1]/div[2]/div[1]/h4[@class='wrap_item item_type_text']")
                for item in div_p_elems:
                    content_text += item.text
                content_text = content_text.replace('\n', " ")
            
            except:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                driver.get_window_position(driver.window_handles[0])
                continue
            
            content_text = re.sub('[\'\"]', '', content_text)
            time.sleep(WAIT_TIME)

            contents.append({
                "keyword": keyword,
                "content": content_text,
            })
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            driver.get_window_position(driver.window_handles[0])
        
        start_content += 19
        if cnt % 10 == 0:
            print("SAVE!")
            db = saveposts.CRUD()

            f = open("./dataset/posts.csv", "a", encoding="UTF-8", newline="")
            csvWriter = csv.writer(f)
            for con in contents:
                print(con["keyword"], con["content"])
                csvWriter.writerow([con["keyword"], con["content"]])
                db.insertDB(table="raw_post", column="keyword, content", 
                        data = f"""'{con["keyword"]}', '{con["content"]}'""")
            db.insertCommit()
            
            del db
            f.close()
            contents = []
    driver.close()
print("SCRAP FINISH!!")