import sys
import time
from config import CONFIG
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    # 設定読み込み
    customer_no = CONFIG['aubankCustomerNo']
    password = CONFIG['aubankLoginPassword']

    if not customer_no or not password:
        print("Error: 設定ファイル 'aubankCustomerNo' または 'aubankLoginPassword' が設定されていません。")
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
        driver.get("https://www.jibunbank.co.jp/")
        
        # 現在のウィンドウハンドルを保存
        main_window_handle = driver.current_window_handle

        # 2. ログインボタンクリック (新しいウィンドウが開く)
        print("ログインボタンをクリック...")
        login_link = driver.find_element(By.LINK_TEXT, "ログイン")
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
        time.sleep(1) # 画面遷移の安定待機
        
        customer_no_input = driver.find_element(By.ID, "customerNo")
        customer_no_input.clear()
        customer_no_input.send_keys(customer_no)
        
        password_input = driver.find_element(By.ID, "loginPW")
        password_input.clear()
        password_input.send_keys(password)
        
        # 4. ログイン実行
        print("ログイン実行...")
        # パスワード入力後のログインボタン (linkText=ログイン)
        # フォーム内のボタンを探すため、少し具体的に指定するか、単にLinkTextで探す
        # .sideファイルでは linkText=ログイン となっていた
        login_submit_btn = driver.find_element(By.LINK_TEXT, "ログイン")
        login_submit_btn.click()

        # ログイン完了待機 (マイページが表示されるのを待つなど)
        # ここでは振込ボタンが表示されるのを待つことにする
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, "振込")))
        print("ログイン成功")

        # 5. 振込ループ処理 (15回)
        payment_count = 14
        amount = "10000"

        for i in range(payment_count):
            print(f"振込処理 {i+1} / {payment_count} 回目開始")
            
            # 振込メニューへ (TOP画面の「振込」ボタン)
            # .side: linkText=振込 (index 3 or 4 in xpath)
            driver.find_element(By.LINK_TEXT, "振込").click()
            
            # さらに振込メニューの中の「振込」などをクリックする必要があるか確認
            # .side line 154: click linkText=振込 again.
            # 画面遷移を待つ
            time.sleep(1)
            
            # もしかしたら2回押す必要がある、あるいはメニュー階層がある
            # 確実に要素が見えるまで待つ
            # 2つ目の「振込」リンクをクリック (振込トップ -> 振込開始)
            # .sideでは2回クリックしている
            sub_transfer_link = WebDriverWait(driver, 10).until(
                 EC.element_to_be_clickable((By.LINK_TEXT, "振込"))
            )
            sub_transfer_link.click()

            # 登録口座から選択
            print("登録口座から選択...")
            # css=li:nth-child(3) > .c-btn-support
            # LinkText="登録口座から選択" が .side の innerText にあるのでそっちのほうが堅牢かも
            # xpath=//a[contains(.,'登録口座から選択')]
            registered_account_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'登録口座から選択')]"))
            )
            registered_account_btn.click()

            # 振込先選択 (一番上)
            print("振込先を選択...")
            # css=.c-box-result-normal-result-item:nth-child(1) .c-box-result-item-bank-branch
            first_account = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".c-box-result-normal-result-item:nth-child(1) .c-box-result-item-bank-branch"))
            )
            first_account.click()

            # 金額入力
            print(f"金額入力: {amount}円")
            amount_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "piaAmt"))
            )
            amount_input.clear()
            amount_input.send_keys(amount)

            # 確認ボタン
            print("確認画面へ...")
            # .side: linkText=確認する
            confirm_btn = driver.find_element(By.LINK_TEXT, "確認する")
            confirm_btn.click()

            # 振込実行ボタン
            print("振込実行...")
            # .side: linkText=振込する
            execute_btn = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "振込する"))
            )
            execute_btn.click()

            # 完了画面からトップへ戻る
            print("トップへ戻る...")
            # .side: linkText=auじぶん銀行トップ
            top_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "auじぶん銀行トップ"))
            )
            top_link.click()
            
            # トップページに戻ったことを確認
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "振込")))
            print(f"振込処理 {i+1} 回目完了")
            time.sleep(1) # 少し待機

        # 6. ログアウト
        print("ログアウト処理...")
        logout_link = driver.find_element(By.LINK_TEXT, "ログアウト")
        logout_link.click()
        
        # ログアウト後の処理待機 (ウィンドウを閉じる前に少し待つ)
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
