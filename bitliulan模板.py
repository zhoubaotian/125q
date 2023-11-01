from multiprocessing.dummy import Pool

from config.config import *
from publics.public_function import *


# from publics.Ads_server import *


def update_status(windows_id, status):
    try:
        db = sqlite3.connect(f'../../{DB_NAME}')
        cursor = db.cursor()
        cursor.execute(f"UPDATE bitbrowser SET status = '{str(status)}' WHERE windows_id = '{str(windows_id)}'")
        db.commit()
    except:
        pass

def begin(data):
    bit_id = 'f121eb64042e4e8f89b289abc340d855'
    driver = bitbrowser.open_browser(bit_id)
    # options = webdriver.ChromeOptions()
    # options.debugger_address = '127.0.0.1:54445'
    # driver = webdriver.Chrome(options=options)

    driver.get('https://www.peew.vip/airdrop/?r=oekilhc6')
    exit()
    try:
        time.sleep(3)
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "//button[text()=' OK ']"))).click()
        except Exception as e:
            pass
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'input[name="address"]'))).send_keys(data['address'])
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'input[name="email"]'))).send_keys(data['mail'])
        time.sleep(3)

        try:
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[text()=' Claim 500,000 $PEEW ']"))).click()
        except Exception as e:
            pass
        while True:
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "//button[text()=' OK ']"))).click()
            except Exception as e:
                pass
            if 'You just unlocked 500,000 $PEEW from airdrop' in driver.page_source:
                print(data['address'],'处理成功')
                update_status(bit_id,'处理成功')
                break
            time.sleep(1)

    except Exception as e:
        print(e)
    time.sleep(3)
    bitbrowser.quit_browser(bit_id)


def set_proxies(win_id):
    bit_info = bitbrowser.bit_detail(win_id)
    update_data = bit_info['data']
    update_data['proxyType'] = 'socks5'
    update_data['proxyMethod'] = 2
    ip = requests.get(
        'http://list.sky-ip.net/user_get_ip_list?token=PxBGZJjvxKgYHI5v1676614177448&qty=1&country=nl&time=10&format=txt&protocol=socks5').text.strip()
    print(ip)
    agency = ip.split(":", 1)
    update_data['host'] = agency[0]
    update_data['port'] = agency[1]
    result = bitbrowser.bit_update(update_data)
    if result['success']:
        print(f'修改成功！！！')


if __name__ == '__main__':
    bitbrowser = bitbrowser_sv(localurl=LOCALURL,web_type='d')

    begin({})
    exit()

    pool = Pool(5)
    pool.map(begin, lists)

