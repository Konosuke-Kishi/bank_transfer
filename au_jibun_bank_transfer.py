# ======================================================
# ライブラリ
# ======================================================
import time
from config import CONFIG
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ======================================================
# 設定ファイル（config.py）の読み込み
# ======================================================
AMOUNT_OF_MONEY = CONFIG['amountOfMoney']
AU_BANK_CUSTOMER_NO = CONFIG['aubankCustomerNo']
AU_BANK_PASSWORD = CONFIG['aubankLoginPassword']
AU_BANK_PAYMENT_COUNT = CONFIG['aubankPaymentCount']

# ======================================================
# メイン処理
# ======================================================
def main():
    # WebDriverの設定
    options = webdriver.FirefoxOptions()
    # 必要に応じてヘッドレスモードなどのオプションを追加
    # options.add_argument('--headless')
    
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(10)

    try:
        # 1. トップページへアクセス
        print("トップページへアクセス中...")
        driver.get("https://www.jibunbank.co.jp/")
        
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
        
        # お客さま番号入力
        customer_no_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "customerNo"))
        )
        customer_no_input.clear()
        customer_no_input.send_keys(AU_BANK_CUSTOMER_NO)
        
        # パスワード入力
        password_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "loginPW"))
        )
        password_input.clear()
        password_input.send_keys(AU_BANK_PASSWORD)
        
        # ログイン実行
        print("ログイン実行...")
        login_submit_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "ログイン"))
        )
        login_submit_btn.click()

        # ログイン完了待機  (振込ボタンが表示されるのを待つ)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, "振込")))
        print("ログイン成功")
            
        # 振込メニューへ
        print("振込メニューを開く...")
        transfer_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "振込"))
        )
        transfer_link.click()
        
        # 2つ目の「振込」リンクをクリック
        sub_transfer_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "振込"))
        )
        sub_transfer_link.click()

        # 4. 振込ループ処理
        for i in range(AU_BANK_PAYMENT_COUNT):
            print(f"振込処理 {i+1} / {AU_BANK_PAYMENT_COUNT} 回目開始")

            # 登録口座から選択
            print("登録口座から選択...")
            registered_account_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'登録口座から選択')]"))
            )
            registered_account_btn.click()

            # 振込先選択 (一番上)
            print("振込先を選択...")
            first_account = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".c-box-result-normal-result-item:nth-child(1) .c-box-result-item-bank-branch"))
            )
            first_account.click()

            # 金額入力
            print(f"金額入力: {AMOUNT_OF_MONEY}円")
            amount_input = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "piaAmt"))
            )
            amount_input.clear()
            amount_input.send_keys(AMOUNT_OF_MONEY)

            # 確認ボタン
            print("確認画面へ...")
            confirm_btn = driver.find_element(By.LINK_TEXT, "確認する")
            confirm_btn.click()

            # 振込実行ボタン
            print("振込実行(スマホ認証) をクリック。スマホで承認操作を行ってください。")
            execute_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "振込する"))
            )
            execute_btn.click()

            # スマホ承認待機
            # 「続けて振込」ボタンが表示されるまで待つ (完了画面)
            # タイムアウトを少し長めに設定 (60秒)
            print("スマホ承認待ち (最大60秒)...")
            try:
                driver.execute_script("window.scrollTo(0,0)")
                next_transfer_btn = WebDriverWait(driver, 60).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "続けて振込"))
                )
                print("振込完了確認")
                next_transfer_btn.click()            
            except Exception as e:
                print("スマホ承認がタイムアウトしたか、画面遷移に失敗しました。")
                raise e
        
            print(f"振込処理 {i+1} 回目完了")
            time.sleep(1)

        # 5. ログアウト
        print("ログアウト処理...")
        logout_link = driver.find_element(By.LINK_TEXT, "ログアウト")
        logout_link.click()
        time.sleep(2)

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        print("ブラウザを終了します")
        driver.quit()

if __name__ == "__main__":
    main()
