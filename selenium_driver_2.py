from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


import config


class SeleniumDriver:
    def __init__(self):
        self.start_driver()
        self.driver.get("https://www.reebuild.com")
        self.logged_in = False
        self.in_meeting = False

    def start_driver(self):
        opt = Options()
        opt.add_experimental_option("excludeSwitches", ["enable-automation"])
        opt.add_argument('--start-maximized')
        opt.add_experimental_option("prefs",
                                    {
                                        "profile.default_content_setting_values.media_stream_mic": 1,
                                        "profile.default_content_setting_values.media_stream_camera": 1,
                                        "profile.default_content_setting_values.geolocation": 0,
                                        "profile.default_content_setting_values.notifications": 1})

        service = Service('/usr/bin/chromedriver')
        self.driver = webdriver.Chrome(service=service, options=opt)
        self.driver.get("https://www.reebuild.com")
        self.logged_in = False
        self.in_meeting = False

    def get_driver(self):
        return self.driver

    def close_driver(self):
        self.driver.close()

    def open_url(self, url):
        if self.in_meeting:
            self.in_meeting = False
        if not url.startswith("http"):
            url = "http://" + url
        self.driver.get(url)

    def google_login(self, mail_address, password):
        # restart the driver
        self.driver.close()
        self.start_driver()

        # Login Page
        self.driver.get('https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=https://www.google.com/&ec=GAZAAQ')

        # input Gmail
        self.driver.find_element(By.ID, "identifierId").send_keys(mail_address)
        self.driver.find_element(By.ID, "identifierNext").click()
        self.driver.implicitly_wait(10)

        # input Password
        self.driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
        self.driver.implicitly_wait(10)
        self.driver.find_element(By.ID, "passwordNext").click()
        self.driver.implicitly_wait(10)

    def start_meeting(self):
        self.driver.implicitly_wait(10)
        self.driver.get('https://meet.google.com/?hs=197&authuser=0&pli=1')

        if "https://workspace.google.com/products/meet/" in self.driver.current_url:
            ele = self.driver.find_element(By.XPATH, '//*[@id="m2"]/div/div/div[1]/div[2]/div[1]/gws-button[1]')
            if ele:
                ele.click()

        # click on New Meeting button
        self.driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[4]/div[1]/div/div[1]/div[3]/div/div[1]/div[1]/div/button').click()
        self.driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[4]/div[1]/div/div[1]/div[3]/div/div[1]/div[2]/div/ul/li[2]').click()

        # wait until hs= is not in the url anymore
        while "hs=" in self.driver.current_url:
            self.driver.implicitly_wait(10)

        self.configure_meet()

        print(self.driver.current_url)
        self.in_meeting = True
        return self.driver.current_url

    def configure_meet(self):
        privacy_settings = self.driver.find_element(By.XPATH,
                                                    '//*[@id="yDmH0d"]/c-wiz/div[1]/div/div[24]/div[3]/div[10]/div/div/div[3]/div/div[5]/div/div/span/button').click()

        open_to_all = self.driver.find_element(By.XPATH,
                                               '//*[@id="yDmH0d"]/c-wiz/div[1]/div/div[24]/div[3]/div[4]/div[2]/div/div[2]/div/div[2]/div/div/div[5]/div[3]/div[2]/div[1]/div[1]').click()

        privacy_settings = self.driver.find_element(By.XPATH,
                                                    '//*[@id="yDmH0d"]/c-wiz/div[1]/div/div[24]/div[3]/div[10]/div/div/div[3]/div/div[5]/div/div/span/button').click()

        camera = self.driver.find_element(By.XPATH, '/html/body/div[1]/c-wiz/div[1]/div/div[24]/div[3]/div[10]/div/div/div[2]/div/div[2]/div/span/button').click()

        notification = self.driver.find_element(By.XPATH, '/html/body/div[1]/c-wiz/div[2]/div[1]/button').click()

        dot_settings = self.driver.find_element(By.XPATH,
                                                '/html/body/div[1]/c-wiz/div[1]/div/div[24]/div[3]/div[10]/div/div/div[2]/div/div[7]/div[5]/div[1]/span/button').click()

        layout = self.driver.find_element(By.XPATH, '/html/body/div[3]/div/ul/li[4]').click()

        spotlight = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[2]/div/div[2]/div[2]/label[3]/div/div/input').click()

        # selenium driver send esc key to close the settings
        action_chain = webdriver.ActionChains(self.driver)
        action_chain.send_keys("\ue00C").perform()

        dot_settings = self.driver.find_element(By.XPATH,
                                                '/html/body/div[1]/c-wiz/div[1]/div/div[24]/div[3]/div[10]/div/div/div[2]/div/div[7]/div[5]/div[1]/span/button').click()

        full_screen = self.driver.find_element(By.XPATH, '/html/body/div[3]/div/ul/li[5]').click()



        # selenium driver send tab enter to close the safety warning
        action_chain = webdriver.ActionChains(self.driver)
        action_chain.send_keys("\ue004").perform()
        action_chain.send_keys("\ue007").perform()


if __name__ == "__main__":
    driver = SeleniumDriver()
    driver.google_login(config.google_mail, config.google_password)
    driver.start_meeting()
