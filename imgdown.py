import time
from selenium import webdriver
import urllib.request
from google.cloud import vision_v1 as vision
import io, os, string
import pyperclip
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

class clawer:
    def __init__(self):
        self.url = "http://192.168.0.1"
        self.imagePath = './image/'
        self.driver = webdriver.Chrome("D://saRice//code//pythonProject2//chromedriver.exe")
        self.driver.get(self.url)
        self.iframeName = "iframe_captcha"
        self.captcha_tagName = 'captcha_file'

    def switchFrame(self, iframeName):
        self.driver.implicitly_wait(1)
        self.driver.switch_to.frame(iframeName)

    def switchMain(self):
        self.driver.implicitly_wait(1)
        self.driver.switch_to.default_content()

    def imgDown(self):
        self.driver.implicitly_wait(1)
        element =self.driver.find_element_by_name(self.captcha_tagName)
        time.sleep(1)
        imgValue = element.get_attribute('value')
        urllib.request.urlretrieve(self.url+'/captcha/'+imgValue+'.gif', self.imagePath+imgValue+'.jpg')
        print(self.url + '/captcha/' + imgValue + '.gif')

        return imgValue

    def inputID(self):
        self.driver.implicitly_wait(3)
        id_ele = self.driver.find_element_by_xpath("/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/input")
        id_ele.clear()
        #pyperclip.copy('admin')
        id_ele.click()
        time.sleep(1)
        #action.send_keys_to_element(id_ele, 'admin').send_keys(Keys.RETURN)
        id_ele.send_keys('admin')

    def inputPWD(self):
        self.driver.implicitly_wait(3)
        pwd_ele = self.driver.find_element_by_xpath("/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[4]/td[2]/input")
        pwd_ele.click()
        time.sleep(1)
        action = ActionChains(self.driver)
        action.send_keys('admin').perform()
        # pyperclip.copy('admin')
        # action.send_keys_to_element(id_ele, 'admin').send_keys(Keys.RETURN)

    def inputCaptcha(self, captchaText):
        cap_ele = self.driver.find_element_by_xpath('/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[6]/td/input')
        cap_ele.click()
        #action.send_keys_to_element(cap_ele, captchaText).send_keys(Keys.ENTER)
        cap_ele.send_keys(captchaText)
        #action.key_down(Keys.CONTROL).send_keys('v').perform()
        time.sleep(2)

        button = self.driver.find_element_by_xpath('//*[@id="submit_bt"]')
        button.click()

    def middlePage(self, middleUrl):
        self.driver.implicitly_wait(3)
        self.driver.get(middleUrl)
        self.driver.find_element_by_xpath('/html/body/map/area[1]').click()

    def finalPage(self):
        self.driver.implicitly_wait(3)
        self.url = self.driver.current_url
        self.driver.get(self.url)

        self.switchFrame('main_body')
        self.switchFrame('navi_menu_advance')

        #self.driver.find_element_by_xpath('/html/body/form/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[10]/td/table/tbody/tr[5]/td[5]/span/a')

        self.driver.find_element_by_link_text('timepro.cgi?tmenu=expertconf&smenu=advertise').click()

        # self.driver.find_element_by_xpath('/html/body/form/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr/td[3]/span').click()
        # time.sleep(0.5)  fjm g
        # self.driver.find_element_by_xpath('/html/body/form/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[9]/td/table/tbody/tr/td[4]/span').click()
        # time.sleep(0.5)
        # self.driver.find_element_by_xpath('//*[@id="expertconf_advertise_3_td"]/span/a').click()
        # time.sleep(0.5)
        # self.driver.find_element_by_tag_name('input')
        # time.sleep(0.5)
        # self.driver.find_element_by_name('url_redir').click()
        # time.sleep(0.5)
        # self.driver.find_element_by_tag_name('input')
        # time.sleep(0.5)
        # inputUrl = self.driver.find_element_by_name('url_redir_url')
        # time.sleep(0.5)
        # inputUrl.click()
        # inputUrl.send_keys('http://www.naver.com')


class breakCaptcha:
    def __init__(self, fileName):
        self.url = "http://192.168.0.1"
        self.imagePath = './image/'+fileName +'.jpg'
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:/saRice/code/pythonProject2/drone-314700-a167ea11a73b.json"
        self.client = vision.ImageAnnotatorClient()

    def getFile(self):
        with io.open(self.imagePath, 'rb') as image_file:
            content = image_file.read()

        return content

    def getText(self, content):
        image = vision.types.Image(content=content)

        price_candidate = []
        card_number_candidate = []
        date_candidate = []

        response = self.client.text_detection(image=image)
        texts = response.text_annotations

        for text in texts:
            content = text.description
            content = content.replace(',', '')

        return str(content)

if __name__ =="__main__":

    while(1):
        coockie = clawer()
        coockie.inputID()
        coockie.inputPWD()

        coockie.switchFrame('iframe_captcha')
        imgValue = coockie.imgDown()

        bc = breakCaptcha(imgValue)
        captext = (bc.getText(bc.getFile()))
        print(captext)

        if (len(captext) == 5 and captext.isalpha()):
            coockie.switchMain()
            coockie.inputCaptcha(captext)

            # http://192.168.0.1/sess-bin/login.cgi?
            if coockie.driver.current_url == coockie.url+'/sess-bin/login.cgi?':
                coockie.middlePage(coockie.driver.current_url)
                break
            else:
                coockie.driver.close()

        else:
            time.sleep(3)
            coockie.driver.close()

    coockie.finalPage()

    del coockie
    del bc

