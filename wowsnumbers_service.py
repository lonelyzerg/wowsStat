import socket
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import threading
import queue
import pickle
from modules.query import get_recent_url
import signal
import sys


recent_q = queue.Queue(100)
result_q = queue.Queue(200)
sr = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
driver = None


def init():
    print('initializing wows numbers query service...')
    global driver
    driver = uc.Chrome()
    urls = ['https://wows-numbers.com/', 'https://na.wows-numbers.com/', 'https://asia.wows-numbers.com/',
            'https://ru.wows-numbers.com/']
    for init_url in urls:
        driver.get(init_url)
        agree_btn = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-success')))
        time.sleep(1.5)
        #driver.find_element(By.CLASS_NAME, 'btn-success').click()
        agree_btn.click()
        time.sleep(1)

    sr.bind(('127.0.0.1', 9875))
    recent_thread = threading.Thread(target=get_recent)
    recent_thread.setDaemon(True)
    recent_thread.start()


    return_thread = threading.Thread(target=return_result)
    return_thread.setDaemon(True)
    return_thread.start()

    while True:
        print('waiting request...')
        para = sr.recv(1024).decode('utf-8')
        print('new request:')
        server, accid, date = para.strip().split()
        url = get_recent_url(server, accid, date)
        print(url)
        recent_q.put(url)

    return 1


def return_result():
    while True:
        if not result_q.empty():
            result = result_q.get()
            data = pickle.dumps(result)
            ss.sendto(data, ('127.0.0.1', 9874))
            print('data returned.')
        else:
            time.sleep(1)


def get_recent():
    while True:
        if not recent_q.empty():
            try:
                url = recent_q.get()
                print('reading player data...')
                driver.get(url)
                WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.TAG_NAME, 'thead')))
                result = []
                # parse data
                ships = driver.find_elements(by=By.CLASS_NAME, value='cells-middle')
                for ship in ships:
                    fields = ship.find_elements(By.TAG_NAME, 'td')
                    if len(fields) == 8:
                        data = {}

                        # 1: warship; 2: tier; 3: battles; 4: wr; 5: pr; 6: avg dmg; 7: avg frags; 8: avg planes
                        data['战舰'] = fields[0].text.strip()
                        data['等级'] = fields[1].text.strip()
                        data['场次'] = fields[2].text.strip()

                        wr = fields[3].text.split()[0].strip()
                        wr_color = fields[3].find_element(By.TAG_NAME, 'span').value_of_css_property('color')
                        data['胜率'] = [wr, wr_color]

                        pr = fields[4].text.split('\n')[0].replace(' ', '').strip()
                        pr_color = fields[4].find_element(By.TAG_NAME, 'span').value_of_css_property('color')
                        data['PR'] = [pr, pr_color]

                        avg_dmg = fields[5].text.strip()
                        dmg_color = fields[5].find_element(By.TAG_NAME, 'span').value_of_css_property('color')
                        data['场均伤害'] = [avg_dmg, dmg_color]

                        avg_frag = fields[6].text.strip()
                        farg_color = fields[6].find_element(By.TAG_NAME, 'span').value_of_css_property('color')
                        data['场均击沉'] = [avg_frag, farg_color]

                        avg_plane = fields[7].text.strip()
                        plane_color = fields[7].find_element(By.TAG_NAME, 'span').value_of_css_property('color')
                        data['场均飞机击落'] = [avg_plane, plane_color]

                        result.append(data)

                result_q.put({'status': True, 'data': result})
                print('finished reading.')
            except Exception:
                data = {'status': False}
                result_q.put(data)
                print('no record.')

        else:
            time.sleep(1)


def signal_handler(signal, frame):
    sr.shutdown()
    sr.close()
    ss.close()
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    init()
