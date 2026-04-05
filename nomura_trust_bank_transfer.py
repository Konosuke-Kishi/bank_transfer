# ======================================================
# ライブラリ
# ======================================================
from notify import line_notify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyotp, chromedriver_autoinstaller, geckodriver_autoinstaller
from config import CONFIG

# ======================================================
# 設定ファイル（config.py）の読み込み
# ======================================================
# 使用するブラウザの種類
USE_BROWSER = CONFIG['useBrowser']
# ヘッドレスブラウザを使用するかどうか
USE_HEADLESS_BROWSER = CONFIG['useHeadlessBrowser']
# Chromeユーザプロファイルの格納先パス
CHROME_USER_DATA_DIR = CONFIG['chromeUserDataDir']
# Firefoxユーザプロファイルの格納先パス
FIREFOX_USER_DATA_DIR = CONFIG['firefoxUserDataDir']
# 野村信託銀行情報
AMOUNT_OF_MONEY = CONFIG["amountOfMoney"]
NOMURA_TRUST_BANK_PHONE1 = CONFIG["nomuraTrustBankPhone1"]
NOMURA_TRUST_BANK_PHONE2 = CONFIG["nomuraTrustBankPhone2"]
NOMURA_TRUST_BANK_PHONE3 = CONFIG["nomuraTrustBankPhone3"]
NOMURA_TRUST_BANK_BRANCH_CODE = CONFIG["nomuraTrustBankBranchCode"]
NOMURA_TRUST_BANK_ACCOUNT_NUM = CONFIG["nomuraTrustBankAccountNum"]
NOMURA_TRUST_BANK_PAYMENT_COUNT = CONFIG["nomuraTrustBankPaymentCount"]
NOMURA_TRUST_BANK_LOGIN_PASSWORD = CONFIG["nomuraTrustBankLoginPassword"]
NOMURA_TRUST_BANK_OTP_SECRET = CONFIG["nomuraTrustBankOTPSecret"]
# 待機時間
ELEMENT_WAIT_TIME = 30
DEVICE_AUTH_WAIT_TIME = 120

# ======================================================
# ドライバの設定
# ======================================================
def create_driver():
  if(USE_BROWSER == "Firefox"):
    executable_path = geckodriver_autoinstaller.install()
    options = webdriver.FirefoxOptions()
    options.add_argument('--disable-popup-blocking')
    options.add_argument("-profile")
    options.add_argument(FIREFOX_USER_DATA_DIR)
    options.headless = USE_HEADLESS_BROWSER
    service = webdriver.firefox.service.Service(executable_path)
    return webdriver.Firefox(service=service, options=options)
  if(USE_BROWSER == "Chrome"):
    executable_path = chromedriver_autoinstaller.install()
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-popup-blocking')
    options.add_argument(f"--user-data-dir={CHROME_USER_DATA_DIR}")
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
        # 1. ログイン画面へアクセス
        print("ログイン画面へアクセス中...")
        driver.get("https://hometrade.nomura.co.jp/web/rmfCmnEtcExcSso8Action.do")
        
        # ウィンドウサイズ設定
        driver.set_window_size(1475, 1060)

        # 2. ログイン情報入力
        print("ログイン情報を入力中...")
        
        # 店番号
        branch_input = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
        EC.presence_of_element_located((By.NAME, "btnCd"))
        )
        branch_input.clear()
        branch_input.send_keys(NOMURA_TRUST_BANK_BRANCH_CODE)
            
        # 口座番号
        account_input = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
            EC.presence_of_element_located((By.NAME, "kuzNo"))
        )
        account_input.clear()               
        account_input.send_keys(NOMURA_TRUST_BANK_ACCOUNT_NUM)
            
        # パスワード
        password_input = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
            EC.presence_of_element_located((By.NAME, "gnziLoginPswd"))
        )
        password_input.clear()
        password_input.send_keys(NOMURA_TRUST_BANK_LOGIN_PASSWORD)
            
        # 3. ログイン実行
        print("ログイン実行...")
        login_btn = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
            EC.element_to_be_clickable((By.NAME, "_ActionID"))
        )
        login_btn.click()
        print(f"ログイン成功\n\"初回のみ野村信託銀行TOPまで手動操作してください")

        # ===================================================================
        # TODO: 初回のみここでワンタイムパスワード認証と野村信託銀行の合言葉認証が入る
        # ===================================================================
                
        # 次の画面へ
        print("次の画面へ...")
        next_btn = WebDriverWait(driver, DEVICE_AUTH_WAIT_TIME).until(
            EC.element_to_be_clickable((By.NAME, "ACT_doNext"))
        )
        next_btn.click()

        # 振込メニューへ
        transfer_link = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "振込"))
        )
        transfer_link.click()

        # 4. 振込ループ処理
        for i in range(NOMURA_TRUST_BANK_PAYMENT_COUNT):
            print(f"振込処理 {i+1} / {NOMURA_TRUST_BANK_PAYMENT_COUNT} 回目開始")

            # 振込先選択 (「選択」リンク)
            print("振込先を選択...")
            select_payee_link = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
                EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "選")))
            select_payee_link.click()

            # 電話番号入力
            print("電話番号入力...")
            tel1_input = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
                EC.presence_of_element_located((By.NAME, "CMCTN_DEST_TEL_NUM1")))
            tel1_input.clear()
            tel1_input.send_keys(NOMURA_TRUST_BANK_PHONE1)
                
            tel2_input = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
                EC.presence_of_element_located((By.NAME, "CMCTN_DEST_TEL_NUM2")))
            tel2_input.clear()
            tel2_input.send_keys(NOMURA_TRUST_BANK_PHONE2)
                
            tel3_input = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
                EC.presence_of_element_located((By.NAME, "CMCTN_DEST_TEL_NUM3")))
            tel3_input.clear()
            tel3_input.send_keys(NOMURA_TRUST_BANK_PHONE3)

            # 金額入力
            print(f"金額入力: {AMOUNT_OF_MONEY}円")
            amount_input = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
                EC.presence_of_element_located((By.NAME, "PIA_AMT_INPUT")))
            amount_input.clear()
            amount_input.send_keys(AMOUNT_OF_MONEY)

            # 確認へ
            print("確認画面へ...")
            confirm_btn = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
                EC.element_to_be_clickable((By.NAME, "ACT_doConfirm")))
            confirm_btn.click()

            # 架電する電話番号を選択
            print("架電する電話番号を選択...")
            tel_checkbox = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/form[1]/table[3]/tbody/tr/td/table/tbody/tr[2]/td/div/input")))
            tel_checkbox.send_keys(Keys.SPACE)

            # 電話をかけて認証ボタンを押下
            print("電話をかけて認証ボタンを押下...")
            confirm_btn = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "電話をかけて認証")))
            confirm_btn.click()

            # 認証用電話番号取得
            print(f"認証用電話番号取得...")
            auth_tel_no = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
                EC.presence_of_element_located((By.ID, "AUTHENTIC_NUMBER")))
            auth_tel_text = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
                lambda d: d.find_element(By.ID, "AUTHENTIC_NUMBER").text.strip() or False)
            WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
                EC.text_to_be_present_in_element((By.ID, "AUTHENTIC_NUMBER"), auth_tel_text))

            # 認証用電話番号をLINEでスマホに通知
            msg = f"認証用電話番号は\n{auth_tel_no.text}"
            line_notify(msg)
            print(f"電話認証完了待機:{DEVICE_AUTH_WAIT_TIME}秒...")

            # ワンタイムパスワード入力
            print("ワンタイムパスワード入力...")
            otp_input = WebDriverWait(driver, DEVICE_AUTH_WAIT_TIME).until(
                EC.element_to_be_clickable((By.NAME, "MASK_INC_SPOTP_PWD")))
            otp_input.clear()
            otp_input.send_keys(pyotp.TOTP(NOMURA_TRUST_BANK_OTP_SECRET).now())

            # 実行ボタン押下
            print("実行ボタン押下...")
            execute_btn = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
                EC.element_to_be_clickable((By.NAME, "ACT_doDecide")))
            execute_btn.click()

            # 次の振込へ
            next_url_link = WebDriverWait(driver, DEVICE_AUTH_WAIT_TIME).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "続けて振込をする")))
            print(f"振込処理 {i+1} 回目完了")

            # 次の振込へ
            next_url_link.click()

        # 5. ログアウト
        print("ログアウト処理...")
        logout_link = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "ログアウト")))
        logout_link.click()
        
        print("ログアウト確認...")
        close_btn = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
            EC.element_to_be_clickable((By.ID, "button")))
        close_btn.click()
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
