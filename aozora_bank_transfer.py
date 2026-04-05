# ======================================================
# ライブラリ
# ======================================================
import time, chromedriver_autoinstaller, geckodriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config_edit import CONFIG

# ======================================================
# 設定ファイル（config.py）の読み込み
# ======================================================
# 使用するブラウザの種類
USE_BROWSER = CONFIG['useBrowser']
# ヘッドレスブラウザを使用するかどうか
USE_HEADLESS_BROWSER = CONFIG['useHeadlessBrowser']
# あおぞら銀行情報
AMOUNT_OF_MONEY = CONFIG["amountOfMoney"]
AOZORA_BANK_CUST_NUM = CONFIG["aozorabankCustomerNo"]
AOZORA_BANK_PASSWORD = CONFIG["aozorabankLoginPassword"]
AOZORA_BANK_PAYMENT_COUNT = CONFIG["aozorabankPaymentCount"]
# 待機時間
ELEMENT_WAIT_TIME = 20
DEVICE_AUTH_WAIT_TIME = 30

# ======================================================
# ドライバの設定
# ======================================================
def create_driver():
  if(USE_BROWSER == "Firefox"):
    executable_path = geckodriver_autoinstaller.install()
    options = webdriver.FirefoxOptions()
    options.add_argument('--disable-popup-blocking')
    options.headless = USE_HEADLESS_BROWSER
    service = webdriver.firefox.service.Service(executable_path)
    return webdriver.Firefox(service=service, options=options)
  if(USE_BROWSER == "Chrome"):
    executable_path = chromedriver_autoinstaller.install()
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-popup-blocking')
    options.headless = USE_HEADLESS_BROWSER
    service = webdriver.chrome.service.Service(executable_path)
    return webdriver.Chrome(service=service, options=options)
  
# ======================================================
# メイン処理
# ======================================================
def main():
    # driverの設定
    driver = create_driver()
    driver.implicitly_wait(10)

    try:
        # ログイン画面へアクセス
        print("ログイン画面へアクセス中...")
        driver.get("https://www.ib2.aozorabank.co.jp/ib/index.do?PT=BS&CCT0080=0398")
        
        # ウィンドウサイズ設定
        driver.set_window_size(1475, 1060)

        # ログイン情報入力
        print("ログイン情報を入力中...")
        WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
            EC.presence_of_element_located((By.NAME, "BTX0010"))
        ).send_keys(AOZORA_BANK_CUST_NUM)
        
        # パスワード入力
        WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
            EC.presence_of_element_located((By.NAME, "BPW0020"))
        ).send_keys(AOZORA_BANK_PASSWORD)
        
        # ログイン実行
        print("ログイン実行...")
        WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
            EC.element_to_be_clickable((By.NAME, "forward_BSM2010"))).click()

        # ログイン完了待機
        WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
           EC.presence_of_element_located((By.ID, "btn002-1")))
        print("ログイン成功")
            
        # 振込メニュー選択
        WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
            EC.element_to_be_clickable((By.ID, "btn002-1"))).click()

        # 振込ループ処理
        for i in range(AOZORA_BANK_PAYMENT_COUNT):
            print(f"振込処理 {i+1} / {AOZORA_BANK_PAYMENT_COUNT} 回目開始")

            # 振込先選択画面へ
            print("振込先を選択...")
            WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
                EC.element_to_be_clickable((By.ID, "btn558-1"))).click()

            # 金額入力
            print(f"金額入力: {AMOUNT_OF_MONEY}円")
            WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".inputA02"))
            ).send_keys(AMOUNT_OF_MONEY)

            # 取引確認画面へ
            print("取引確認画面へ...")
            WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
                EC.element_to_be_clickable((By.ID, "btn001"))).click()

            # スマホ承認待機
            print(f"スマホ承認待機: {DEVICE_AUTH_WAIT_TIME}秒...")

            # OKボタン押下
            print("OKボタン押下...")
            WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".ui-button"))).click()

            # チェックボックスがあれば押下
            time.sleep(ELEMENT_WAIT_TIME)
            check_box = driver.find_elements(By.ID, "chkBox002")
            if check_box:
                check_box[0].click()
                print("チェックボックス押下")
            else: pass

            # デバイス認証完了後、実行ボタン押下
            time.sleep(DEVICE_AUTH_WAIT_TIME - ELEMENT_WAIT_TIME)
            otp_register_button = driver.find_elements(By.XPATH, "//button[contains(.,'実行')]")
            if otp_register_button:
                otp_register_button[0].click()
            else: pass

            # 振込完了確認
            WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
               EC.element_to_be_clickable((By.ID, "btn006"))).click()
            print(f"振込処理 {i+1} 回目完了")

        # ログアウト
        print("ログアウト処理...")
        WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#cs_globalButton_logout > img"))).click()
        print("ログアウトしました。")

    except Exception as e:
        print(f"ステータス: エラー - {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        print("ブラウザを終了します")
        driver.quit()

if __name__ == "__main__":
    main()
