# ======================================================
# ライブラリ
# ======================================================
from config import CONFIG
from undetected_geckodriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
import subprocess, re, undetected_chromedriver as uc

# ======================================================
# 設定ファイル（config.py）の読み込み
# ======================================================
# ウィンドウ設定
WINDOW_WIDTH = CONFIG['windowWidth']
WINDOW_HEIGHT = CONFIG['windowHeight']
# 使用するブラウザの種類
USE_BROWSER = CONFIG['useBrowser']
# 入金金額
AMOUNT_OF_MONEY = CONFIG["amountOfMoney"]
# ヘッドレスブラウザを使用するかどうか
USE_HEADLESS_BROWSER = CONFIG['useHeadlessBrowser']
# 待機時間
ELEMENT_WAIT_TIME = CONFIG["elementWaitTime"]
DEVICE_AUTH_WAIT_TIME = CONFIG["deviceAuthWaitTime"]
# Chromeのパスとバージョン取得コマンド
CHROME_PATH = CONFIG['chromePath']
CMD_OPTIONS = CONFIG['cmdOptions']
# SBI新生銀行情報
SHINSEI_BANK_XPATH = CONFIG["shinseibankXPath"]
SHINSEI_BANK_PASSWORD = CONFIG["shinseibankLoginPassword"]
SHINSEI_BANK_LOGIN_URL = CONFIG["shinseibankLoginUrl"]
SHINSEI_BANK_CUSTOMER_NO = CONFIG["shinseibankCustomerNo"]
SHINSEI_BANK_PAYMENT_COUNT = CONFIG["shinseibankPaymentCount"]

# ======================================================
# chromeのメジャーバージョンを取得する
# ======================================================
def get_chrome_version_mac():
    # MacのChromeパス
    cmd = [CHROME_PATH, CMD_OPTIONS]
    result = subprocess.check_output(cmd).decode("utf-8")
    # バージョン番号（数字部分）を抽出
    version = re.search(r"(\d+\.\d+\.\d+\.\d+)", result).group(1)
    return version.split('.')[0] # メジャーバージョン

# ======================================================
# ドライバの設定
# ======================================================
def create_driver():
  if(USE_BROWSER == "Firefox"):
    options = Options()
    options.headless = USE_HEADLESS_BROWSER
    options.add_argument('--disable-popup-blocking')
    return Firefox(options=options)
  if(USE_BROWSER == "Chrome"):
    options = uc.ChromeOptions()
    options.headless = USE_HEADLESS_BROWSER
    options.add_argument('--disable-popup-blocking')
    return uc.Chrome(options=options, version_main=int(get_chrome_version_mac()))


# ======================================================
# メイン処理
# ======================================================
def sbi_shinsei_bank_transfer():
    # driverの設定
    driver = create_driver()
    try:
        # ログイン画面へアクセス
        print("ログイン画面へアクセス中...")
        driver.get(SHINSEI_BANK_LOGIN_URL)
        
        # ウィンドウサイズ設定
        driver.set_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)

        # ログイン処理
        print("ログイン情報を入力中...")

        # 店番号・口座番号入力
        customer_no_input = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
            EC.element_to_be_clickable((By.NAME, "nationalId")))
        customer_no_input.clear()
        customer_no_input.send_keys(SHINSEI_BANK_CUSTOMER_NO)
        
        # パスワード入力
        password_input = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
            EC.element_to_be_clickable((By.ID, "loginPassword")))
        password_input.clear()
        password_input.send_keys(SHINSEI_BANK_PASSWORD)

        # ログイン実行
        print("ログイン実行...")
        login_btn = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'ログイン')]")))
        login_btn.click()
        
        # ログイン完了待機 (振込ボタンが表示されるのを待つ)
        WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
            EC.presence_of_element_located((By.LINK_TEXT, "振込")))
        print("ログイン成功")

        # 振込メニューへ
        print("振込メニューを開く...")
        transfer_link = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "振込")))
        transfer_link.click()

        # 振込ループ処理
        for i in range(SHINSEI_BANK_PAYMENT_COUNT):
            print(f"振込処理 {i+1} / {SHINSEI_BANK_PAYMENT_COUNT} 回目開始")

            # 振込を行う
            print("振込を行うを選択...")
            do_transfer_link = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'振込を行う')]")))
            do_transfer_link.click()

            # 振込先選択 (1番目)
            print("振込先(1番目)を選択...")
            first_payee_btn = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
                EC.element_to_be_clickable((By.XPATH, SHINSEI_BANK_XPATH)))
            first_payee_btn.click()

            # 金額入力
            print(f"金額入力: {AMOUNT_OF_MONEY}円")
            amount_input = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
                EC.element_to_be_clickable((By.NAME, "amount")))
            amount_input.clear()
            amount_input.send_keys(AMOUNT_OF_MONEY)

            # 次へ
            print("次へ...")
            next_btn = driver.find_element(By.XPATH, "//button[contains(.,'次へ')]")
            next_btn.click()
            
            # スクロール (必要なら)
            driver.execute_script("window.scrollTo(0,0)")

            # 実行を押下
            print("実行を押下...")
            execute_btn = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "spAuth")))
            execute_btn.click()

            # スマホ承認待機
            print(f"スマホ承認待機: {DEVICE_AUTH_WAIT_TIME}秒...")
            other_transfer_btn = WebDriverWait(driver, DEVICE_AUTH_WAIT_TIME).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'他の振込を行う')]")))
            print(f"振込処理 {i+1} 回目完了")

            # 次の振込へ
            other_transfer_btn.click()

        # ログアウト押下
        print("ログアウト処理...")
        logout_link = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "ログアウト")))
        logout_link.click()
        
        # ログアウト実行
        print("ログアウト確認...")
        yes_btn = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'はい')]")))
        yes_btn.click()
        print("ログアウトしました。")

    # エラー処理
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
    
    # ブラウザを終了
    finally:
        print("ブラウザを終了します")
        driver.quit()

if __name__ == "__main__":
    sbi_shinsei_bank_transfer()
