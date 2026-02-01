import sys
import time
from config import CONFIG
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    # 設定読み込み
    customer_no = CONFIG["sbishinseibankCustomerNo"]
    password = CONFIG["sbishinseibankLoginPassword"]

    if not customer_no or not password:
        print("Error: 設定ファイル 'sbishinseibankCustomerNo' または 'sbishinseibankLoginPassword' が設定されていません。")
        sys.exit(1)

    # WebDriverの設定
    options = webdriver.FirefoxOptions()
    # 必要に応じてヘッドレスモードなどのオプションを追加
    # options.add_argument('--headless')
    
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(10)

    try:
        # 1. トップページへアクセス
        print("トップページへアクセス中...")
        driver.get("https://www.sbishinseibank.co.jp/")
        
        main_window_handle = driver.current_window_handle

        # 2. ログインボタンクリック (新しいウィンドウが開く)
        print("ログインボタンをクリック...")
        # .side: linkText=ログイン
        login_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "ログイン"))
        )
        login_link.click()

        # 新しいウィンドウが開くのを待つ
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        
        # 新しいウィンドウへ切り替え
        for handle in driver.window_handles:
            if handle != main_window_handle:
                driver.switch_to.window(handle)
                break
        
        print("ログイン画面へ切り替え完了")

        # 3. ログイン情報入力
        print("ログイン情報を入力中...")
        time.sleep(5)
        # 店番号・口座番号 (name=nationalId)
        customer_no_input = driver.find_element(By.NAME, "nationalId")
        customer_no_input.clear()
        customer_no_input.send_keys(customer_no)
        
        # パスワード (id=loginPassword)
        password_input = driver.find_element(By.ID, "loginPassword")
        password_input.clear()
        password_input.send_keys(password)
        
        # 4. ログイン実行
        print("ログイン実行...")
        # ボタン: xpath=//button[contains(.,'ログイン')]
        login_btn = driver.find_element(By.XPATH, "//button[contains(.,'ログイン')]")
        login_btn.click()

        # ログイン完了待機 (振込メニューが表示されるのを待つ)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, "振込")))
        print("ログイン成功")

        # 5. 振込ループ処理 (10回)
        payment_count = 6
        amount = "10000"

        for i in range(payment_count):
            print(f"振込処理 {i+1} / {payment_count} 回目開始")
            
            # 振込メニューへ
            print("振込メニューを開く...")
            transfer_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "振込"))
            )
            transfer_link.click()
            time.sleep(5)
            # 振込を行う
            print("振込を行うを選択...")
            # css=tr:nth-child(1) a > .ng-binding or text check
            do_transfer_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'振込を行う')]"))
            )
            do_transfer_link.click()
            time.sleep(5)
            # 振込先選択 (1番目)
            print("振込先(1番目)を選択...")
            # .side: css=.ng-scope:nth-child(2) > td .ng-binding or button inside td
            # テーブルの行を探してボタンを押す
            # 登録口座のボタン。通常 "選択" というテキストあるいはアイコン
            # xpath=//tr[2]/td[6]/button/span (side file)
            # tr[2]なのはheaderがあるからかも。
            first_payee_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[1]/section[2]/div/table/tbody/tr/td[6]/button/span"))
            )
            first_payee_btn.click()
            time.sleep(5)
            # 金額入力
            print(f"金額入力: {amount}円")
            amount_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "amount"))
            )
            amount_input.clear()
            amount_input.send_keys(amount)

            # 次へ
            print("次へ...")
            # css=.inputAmountBtnSpace > button:nth-child(2) (side file)
            # "次へ" というテキストを含むボタン
            next_btn = driver.find_element(By.XPATH, "//button[contains(.,'次へ')]")
            next_btn.click()
            
            # スクロール (必要なら)
            driver.execute_script("window.scrollTo(0,0)")

            # 実行 (スマホ認証)
            print("実行 (スマホ認証) をクリック。スマホで承認操作を行ってください。")
            # css=.spAuth
            execute_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "spAuth"))
            )
            execute_btn.click()

            # スマホ承認待機
            # 「他の振込を行う」ボタンが表示されるまで待つ (完了画面)
            # タイムアウトを少し長めに設定 (60秒)
            print("スマホ承認待ち (最大60秒)...")
            try:
                other_transfer_btn = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'他の振込を行う')]"))
                )
                print("振込完了確認")
                
                # ループ継続のため「他の振込を行う」をクリックするか、TOPに戻るか
                # .sideファイルでは「他の振込を行う」 -> 「TOP」 -> ループ先頭(振込ボタン) となっている
                other_transfer_btn.click()
                time.sleep(5)
                
                # TOPへ戻る
                print("TOPへ戻る...")
                driver.execute_script("window.scrollTo(0,0)")
                top_link = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "TOP"))
                )
                top_link.click()
                time.sleep(5)
                
                # TOP画面待機
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "振込")))
                
            except Exception as e:
                print("スマホ承認がタイムアウトしたか、画面遷移に失敗しました。")
                raise e

            print(f"振込処理 {i+1} 回目完了")
            time.sleep(1)

        # 6. ログアウト
        print("ログアウト処理...")
        logout_link = driver.find_element(By.LINK_TEXT, "ログアウト")
        logout_link.click()
        
        # ログアウト確認ダイアログなどが出る場合がある
        # .side: click css=.btnCenter > button:nth-child(2) ("はい")
        try:
            print("ログアウト確認...")
            yes_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'はい')]"))
            )
            yes_btn.click()
            
            # "ログイン画面へ" ボタンなどを確認して終了
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(.,'ログイン画面へ')]"))
            )
        except:
            print("ログアウト確認ダイアログが出なかったか、すでにログアウトしています。")

    except Exception as e:
        print(f"ステータス: エラー - {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        print("ブラウザを終了します")
        driver.quit()

if __name__ == "__main__":
    main()
