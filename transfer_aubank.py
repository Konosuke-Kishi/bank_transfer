# ======================================================
# ライブラリ
# ======================================================
from config import CONFIG
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, chromedriver_autoinstaller, geckodriver_autoinstaller

# ======================================================
# 設定ファイル（config.py）の読み込み
# ======================================================
# 使用するブラウザの種類
USE_BROWSER = CONFIG['useBrowser']
# 入金金額
AMOUNT_OF_MONEY = CONFIG['amountOfMoney']
# ヘッドレスブラウザを使用するかどうか
USE_HEADLESS_BROWSER = CONFIG['useHeadlessBrowser']
# 待機時間
ELEMENT_WAIT_TIME = CONFIG['elementWaitTime']
DEVICE_AUTH_WAIT_TIME = CONFIG['deviceAuthWaitTime']
# auじぶん銀行情報
AU_BANK_CUSTOMER_NO = CONFIG['aubankCustomerNo']
AU_BANK_PASSWORD = CONFIG['aubankLoginPassword']
AU_BANK_PAYMENT_COUNT = CONFIG['aubankPaymentCount']

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
def au_jibun_bank_transfer():
    # driverの設定
    driver = create_driver()
    driver.implicitly_wait(10)

    try:
        # 1. トップページへアクセス
        print("トップページへアクセス中...")
        driver.get("https://www.jibunbank.co.jp/")
        
        # 現在のウィンドウハンドルを保存
        main_window_handle = driver.current_window_handle

        # 2. ログインボタンクリック (新しいウィンドウが開く)
        print("ログインボタンをクリック...")
        login_link = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "ログイン")))
        login_link.click()

        # 新しいウィンドウが開くのを待つ
        WebDriverWait(driver, ELEMENT_WAIT_TIME).until(EC.number_of_windows_to_be(2))
        
        # 新しいウィンドウへ切り替え
        for handle in driver.window_handles:
            if handle != main_window_handle:
                driver.switch_to.window(handle)
                break
        
        print("ログイン画面へ切り替え完了")

        # 3. ログイン処理
        print("ログイン情報を入力中...")
        
        # お客さま番号入力
        customer_no_input = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
            EC.presence_of_element_located((By.ID, "customerNo")))
        customer_no_input.clear()
        customer_no_input.send_keys(AU_BANK_CUSTOMER_NO)
        
        # パスワード入力
        password_input = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
            EC.presence_of_element_located((By.ID, "loginPW")))
        password_input.clear()
        password_input.send_keys(AU_BANK_PASSWORD)
        
        # ログイン実行
        print("ログイン実行...")
        login_submit_btn = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "ログイン")))
        login_submit_btn.click()

        # 重要なお知らせがあれば確認ボタン押下
        time.sleep(ELEMENT_WAIT_TIME)
        info_confirm_btn = driver.find_elements(By.LINK_TEXT, "確認")
        if info_confirm_btn:
            info_confirm_btn[0].click()
            print("お知らせスキップ")
        else: pass
            
        # 振込メニューへ
        print("振込メニューを開く...")
        transfer_link = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "振込")))
        transfer_link.click()
        
        # 2つ目の「振込」リンクをクリック
        sub_transfer_link = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "振込")))
        sub_transfer_link.click()

        # 4. 振込ループ処理
        for i in range(AU_BANK_PAYMENT_COUNT):
            print(f"振込処理 {i+1} / {AU_BANK_PAYMENT_COUNT} 回目開始")

            # 登録口座から選択
            print("登録口座から選択...")
            registered_account_btn = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'登録口座から選択')]")))
            registered_account_btn.click()

            # 振込先選択 (一番上)
            print("振込先を選択...")
            first_account = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".c-box-result-normal-result-item:nth-child(1) .c-box-result-item-bank-branch")))
            first_account.click()

            # 金額入力
            print(f"金額入力: {AMOUNT_OF_MONEY}円")
            amount_input = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
                EC.presence_of_element_located((By.ID, "piaAmt")))
            amount_input.clear()
            amount_input.send_keys(AMOUNT_OF_MONEY)

            # 確認ボタン
            print("確認画面へ...")
            confirm_btn = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "確認する")))
            confirm_btn.click()

            # 振込実行ボタン
            print("振込実行押下...")
            execute_btn = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "振込する")))
            execute_btn.click()

            # スマホ承認待機
            print(f"スマホ承認待機: {DEVICE_AUTH_WAIT_TIME}秒...")
            driver.execute_script("window.scrollTo(0,0)")
            next_transfer_btn = WebDriverWait(driver, DEVICE_AUTH_WAIT_TIME).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "続けて振込")))
            print(f"振込処理 {i+1} 回目完了")

            # 次の振込へ
            next_transfer_btn.click()

        # 5. ログアウト
        print("ログアウト処理...")
        logout_link = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "ログアウト")))
        logout_link.click()
        print("ログアウトしました。")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        print("ブラウザを終了します")
        driver.quit()

if __name__ == "__main__":
    au_jibun_bank_transfer()
