# ======================================================
# ライブラリ
# ======================================================
import time
import os
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
# 野村信託銀行情報
AMOUNT_OF_MONEY = CONFIG["amountOfMoney"]
NOMURA_TRUST_BANK_BRANCH_CODE = CONFIG["nomuraTrustBankBranchCode"]
NOMURA_TRUST_BANK_ACCOUNT_NUM = CONFIG["nomuraTrustBankAccountNum"]
NOMURA_TRUST_BANK_PAYMENT_COUNT = CONFIG["nomuraTrustBankPaymentCount"]
NOMURA_TRUST_BANK_LOGIN_PASSWORD = CONFIG["nomuraTrustBankLoginPassword"]
NOMURA_TRUST_BANK_TRANS_PASSWORD = CONFIG["nomuraTrustBankTransPassword"]
NOMURA_TRUST_BANK_PHONE1 = CONFIG["nomuraTrustBankPhone1"]
NOMURA_TRUST_BANK_PHONE2 = CONFIG["nomuraTrustBankPhone2"]
NOMURA_TRUST_BANK_PHONE3 = CONFIG["nomuraTrustBankPhone3"]
# 認証番号入力用のJavaScriptファイル
JSPATH = CONFIG["inputJSFilePath"] 

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
        # 1. ログイン画面へアクセス
        print("ログイン画面へアクセス中...")
        driver.get("https://hometrade.nomura.co.jp/web/rmfCmnEtcExcSso8Action.do")
        
        # ウィンドウサイズ設定
        driver.set_window_size(1475, 1060)

        # 2. ログイン情報入力
        print("ログイン情報を入力中...")
        
        # 店番号
        branch_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "btnCd"))
        )
        branch_input.clear()
        branch_input.send_keys(NOMURA_TRUST_BANK_BRANCH_CODE)
            
        # 口座番号
        account_input = driver.find_element(By.NAME, "kuzNo")
        account_input.clear()               
        account_input.send_keys(NOMURA_TRUST_BANK_ACCOUNT_NUM)
            
        # パスワード
        password_input = driver.find_element(By.NAME, "gnziLoginPswd")
        password_input.clear()
        password_input.send_keys(NOMURA_TRUST_BANK_LOGIN_PASSWORD)
            
        # 3. ログイン実行
        print("ログイン実行...")
        login_btn = driver.find_element(By.NAME, "_ActionID")
        login_btn.click()
        print("ログイン成功")

        # ===========================================================
        # 初回のみここでワンタイムパスワード認証と野村信託銀行の合言葉認証が入る
        # ===========================================================
                
        # 振込メニューへ
        transfer_link = WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.LINK_TEXT, "振込")))
        transfer_link.click()

        # 4. 振込ループ処理
        for i in range(NOMURA_TRUST_BANK_PAYMENT_COUNT):
            print(f"振込処理 {i+1} / {NOMURA_TRUST_BANK_PAYMENT_COUNT} 回目開始")

            # 振込先選択 (「選択」リンク)
            print("振込先を選択...")
            select_payee_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "選"))
            )
            select_payee_link.click()

            # 電話番号入力
            print("電話番号入力...")
            tel1_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "CMCTN_DEST_TEL_NUM1"))
            )
            tel1_input.clear()
            tel1_input.send_keys(NOMURA_TRUST_BANK_PHONE1)
                
            tel2_input = driver.find_element(By.NAME, "CMCTN_DEST_TEL_NUM2")
            tel2_input.clear()
            tel2_input.send_keys(NOMURA_TRUST_BANK_PHONE2)
                
            tel3_input = driver.find_element(By.NAME, "CMCTN_DEST_TEL_NUM3")
            tel3_input.clear()
            tel3_input.send_keys(NOMURA_TRUST_BANK_PHONE3)

            # 金額入力
            print(f"金額入力: {AMOUNT_OF_MONEY}円")
            amount_input = driver.find_element(By.NAME, "PIA_AMT_INPUT")
            amount_input.clear()
            amount_input.send_keys(AMOUNT_OF_MONEY)

            # 確認へ
            print("確認画面へ...")
            confirm_btn = driver.find_element(By.NAME, "ACT_doConfirm")
            confirm_btn.click()

            # 認証番号入力画面
            print("認証番号を入力します...")
            # 取引パスワード入力欄が表示されるまで待つ
            trans_password_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "MASK_INC_TRANS_PWD"))
            )
                
            # input_pin.js を読み込んで実行
            js_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), JSPATH)
            with open(js_path, "r", encoding="utf-8") as f:
                js_content = f.read()
                driver.execute_script(js_content)
            print(f"{JSPATH} を実行しました。")
            time.sleep(1) # JSの反映待ち
                
            # 取引パスワード入力欄にパスワードを入力
            trans_password_input.clear()
            trans_password_input.send_keys(NOMURA_TRUST_BANK_TRANS_PASSWORD)

            # 実行
            print("実行...")
            decide_btn = driver.find_element(By.NAME, "ACT_doDecide")
            decide_btn.click()

            # 完了確認 & 次の振込へ
            print("完了確認中...")
            next_url_link = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "続けて振込をする"))
            )
            print(f"振込処理 {i+1} 回目完了")
            next_url_link.click()
            time.sleep(1)

        # 5. ログアウト
        print("ログアウト処理...")
        logout_link = driver.find_element(By.LINK_TEXT, "ログアウト")
        logout_link.click()
        close_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "button"))
        )
        close_btn.click()

    except Exception as e:
        print(f"ステータス: エラー - {e}")
        import traceback
        traceback.print_exc()
            
    finally:
        print("ブラウザを終了します")
        driver.quit()

if __name__ == "__main__":
    main()
