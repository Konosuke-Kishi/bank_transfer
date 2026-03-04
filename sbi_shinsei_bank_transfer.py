# ======================================================
# ライブラリ
# ======================================================
import time
from config import CONFIG
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import geckodriver_autoinstaller

# ======================================================
# 設定ファイル（config.py）の読み込み
# ======================================================
# 使用するブラウザの種類
USE_BROWSER = CONFIG['useBrowser']
# Chromeユーザプロファイルの格納先パス
CHROME_USER_DATA_DIR = CONFIG['chromeUserDataDir']
# Firefoxユーザプロファイルの格納先パス
FIREFOX_USER_DATA_DIR = CONFIG['firefoxUserDataDir']
# SBI新生銀行情報
AMOUNT_OF_MONEY = CONFIG["amountOfMoney"]
SBISHINSEIBANK_CUSTOMER_NO = CONFIG["sbishinseibankCustomerNo"]
SBISHINSEIBANK_PASSWORD = CONFIG["sbishinseibankLoginPassword"]
SBISHINSEIBANK_PAYMENT_COUNT = CONFIG["sbishinseibankPaymentCount"]

# ======================================================
# ドライバの設定
# ======================================================
# 使用するブラウザのバージョンと一致するdriverをダウンロードし
# ブラウザごとにオプション・プロファイルを設定する
if(USE_BROWSER == "Firefox"):
  executable_path = geckodriver_autoinstaller.install()
  options = webdriver.FirefoxOptions()
  options.add_argument('--disable-popup-blocking')
  options.add_argument("-profile")
  options.add_argument(FIREFOX_USER_DATA_DIR)
  service = webdriver.firefox.service.Service(executable_path=executable_path)
else:
  executable_path = chromedriver_autoinstaller.install()
  options = webdriver.ChromeOptions()
  options.add_argument('--disable-popup-blocking')
  options.add_argument("--user-data-dir=" + CHROME_USER_DATA_DIR)
  service = webdriver.chrome.service.Service(executable_path=executable_path)


# ======================================================
# メイン処理
# ======================================================
def main():
    # 使用するブラウザによって分岐
    if(USE_BROWSER == "Firefox"):
        driver = webdriver.Firefox(service=service, options=options)
    else:
        driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)

    try:
        # 1. トップページへアクセス
        print("トップページへアクセス中...")
        driver.get("https://www.sbishinseibank.co.jp/")
        
        # 現在のウィンドウハンドルを保存
        main_window_handle = driver.current_window_handle

        # 2. ログインボタンクリック (新しいウィンドウが開く)
        print("ログインボタンをクリック...")
        login_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "ログイン"))
        )
        login_link.click()

        # 新しいウィンドウが開くのを待つ
        WebDriverWait(driver, 20).until(EC.number_of_windows_to_be(2))
        
        # 新しいウィンドウへ切り替え
        for handle in driver.window_handles:
            if handle != main_window_handle:
                driver.switch_to.window(handle)
                break
        
        print("ログイン画面へ切り替え完了")

        # 3. ログイン処理
        print("ログイン情報を入力中...")
        time.sleep(1)

        # 店番号・口座番号入力
        customer_no_input = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.NAME, "nationalId"))
        )
        customer_no_input.clear()
        customer_no_input.send_keys(SBISHINSEIBANK_CUSTOMER_NO)
        
        # パスワード入力
        password_input = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "loginPassword"))
        )
        password_input.clear()
        password_input.send_keys(SBISHINSEIBANK_PASSWORD)
        
        # ログイン実行
        print("ログイン実行...")
        login_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'ログイン')]"))
        )
        login_btn.click()

        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        # ログイン完了待機 (振込ボタンが表示されるのを待つ)
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.LINK_TEXT, "振込")))
        print("ログイン成功")

        # 振込メニューへ
        print("振込メニューを開く...")
        transfer_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "振込"))
        )
        transfer_link.click()

        # 4. 振込ループ処理
        for i in range(SBISHINSEIBANK_PAYMENT_COUNT):
            print(f"振込処理 {i+1} / {SBISHINSEIBANK_PAYMENT_COUNT} 回目開始")

            # 振込を行う
            print("振込を行うを選択...")
            do_transfer_link = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'振込を行う')]"))
            )
            do_transfer_link.click()

            # 振込先選択 (1番目)
            print("振込先(1番目)を選択...")
            first_payee_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[1]/section[2]/div/table/tbody/tr/td[6]/button/span"))
            )
            first_payee_btn.click()

            # 金額入力
            print(f"金額入力: {AMOUNT_OF_MONEY}円")
            amount_input = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.NAME, "amount"))
            )
            amount_input.clear()
            amount_input.send_keys(AMOUNT_OF_MONEY)

            # 次へ
            print("次へ...")
            next_btn = driver.find_element(By.XPATH, "//button[contains(.,'次へ')]")
            next_btn.click()
            
            # スクロール (必要なら)
            driver.execute_script("window.scrollTo(0,0)")

            # 実行 (スマホ認証)
            print("実行 (スマホ認証) をクリック。スマホで承認操作を行ってください。")
            execute_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "spAuth"))
            )
            execute_btn.click()

            # スマホ承認待機
            # 「他の振込を行う」ボタンが表示されるまで待つ (完了画面)
            # タイムアウトを少し長めに設定 (30秒)
            print("スマホ承認待ち (最大30秒)...")
            try:
                other_transfer_btn = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'他の振込を行う')]"))
                )
                print("振込完了確認")
                time.sleep(1)
                other_transfer_btn.click()
            except Exception as e:
                print("スマホ承認がタイムアウトしたか、画面遷移に失敗しました。")
                raise e

            print(f"振込処理 {i+1} 回目完了")
            time.sleep(1)

        # 5. ログアウト
        print("ログアウト処理...")
        logout_link = driver.find_element(By.LINK_TEXT, "ログアウト")
        logout_link.click()
        
        print("ログアウト確認...")
        yes_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'はい')]"))
        )
        yes_btn.click()

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        print("ブラウザを終了します")
        driver.quit()

if __name__ == "__main__":
    main()
