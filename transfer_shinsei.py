# ======================================================
# ライブラリ
# ======================================================
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import subprocess, re, undetected_chromedriver as uc
from config import CONFIG

# ======================================================
# 設定ファイル（config.py）の読み込み
# ======================================================
# 入金金額
AMOUNT_OF_MONEY = CONFIG["amountOfMoney"]
# ヘッドレスブラウザを使用するかどうか
USE_HEADLESS_BROWSER = CONFIG['useHeadlessBrowser']
# 待機時間
ELEMENT_WAIT_TIME = CONFIG["elementWaitTime"]
DEVICE_AUTH_WAIT_TIME = CONFIG["deviceAuthWaitTime"]
# Chromeユーザプロファイルの格納先パス
CHROME_USER_DATA_DIR = CONFIG['chromeUserDataDir']
# SBI新生銀行情報
SHINSEIBANK_PASSWORD = CONFIG["shinseibankLoginPassword"]
SHINSEIBANK_CUSTOMER_NO = CONFIG["shinseibankCustomerNo"]
SHINSEIBANK_PAYMENT_COUNT = CONFIG["shinseibankPaymentCount"]
# Chromeのパスとバージョン取得コマンド
CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
CMD_OPTIONS = "--version"

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
    options = uc.ChromeOptions()
    options.headless = USE_HEADLESS_BROWSER
    options.add_argument('--disable-popup-blocking')
    options.add_argument(f"--user-data-dir={CHROME_USER_DATA_DIR}")
    return uc.Chrome(options=options, version_main=int(get_chrome_version_mac()))


# ======================================================
# メイン処理
# ======================================================
def sbi_shinsei_bank_transfer():
    # driverの設定
    driver = create_driver()
    driver.implicitly_wait(10)

    try:
        # 1. トップページへアクセス
        print("トップページへアクセス中...")
        driver.get("https://www.sbishinseibank.co.jp/")
        
        # 現在のウィンドウハンドルを保存
        main_window_handle = driver.current_window_handle

        # 2. ログインボタンクリック (新しいウィンドウが開く)
        print("ログインボタンをクリック...")
        login_link = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "ログイン"))
        )
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

        # 店番号・口座番号入力
        customer_no_input = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
            EC.element_to_be_clickable((By.NAME, "nationalId")))
        customer_no_input.clear()
        customer_no_input.send_keys(SHINSEIBANK_CUSTOMER_NO)
        
        # パスワード入力
        password_input = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
            EC.element_to_be_clickable((By.ID, "loginPassword")))
        password_input.clear()
        password_input.send_keys(SHINSEIBANK_PASSWORD)

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

        # 4. 振込ループ処理
        for i in range(SHINSEIBANK_PAYMENT_COUNT):
            print(f"振込処理 {i+1} / {SHINSEIBANK_PAYMENT_COUNT} 回目開始")

            # 振込を行う
            print("振込を行うを選択...")
            do_transfer_link = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'振込を行う')]")))
            do_transfer_link.click()

            # 振込先選択 (1番目)
            print("振込先(1番目)を選択...")
            first_payee_btn = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[1]/section[2]/div/table/tbody/tr/td[6]/button/span")))
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

        # 5. ログアウト
        print("ログアウト処理...")
        logout_link = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "ログアウト")))
        logout_link.click()
        
        print("ログアウト確認...")
        yes_btn = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'はい')]")))
        yes_btn.click()
        print("ログアウトしました。")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        print("ブラウザを終了します")
        driver.quit()

if __name__ == "__main__":
    sbi_shinsei_bank_transfer()
