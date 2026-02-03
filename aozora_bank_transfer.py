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
AMOUNT_OF_MONEY = CONFIG["amountOfMoney"]
AOZORA_BANK_CUST_NUM = CONFIG["aozorabankCustomerNo"]
AOZORA_BANK_PASSWORD = CONFIG["aozorabankLoginPassword"]
AOZORA_BANK_PAYMENT_COUNT = CONFIG["aozorabankPaymentCount"]

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
        # 1. ログイン画面へアクセス
        print("ログイン画面へアクセス中...")
        driver.get("https://www.ib2.aozorabank.co.jp/ib/index.do?PT=BS&CCT0080=0398")
        
        # ウィンドウサイズ設定
        driver.set_window_size(1475, 1060)

        # 2. ログイン情報入力
        print("ログイン情報を入力中...")
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "BTX0010"))
        )
        username_input.clear()
        username_input.send_keys(AOZORA_BANK_CUST_NUM)
        
        # パスワード
        password_input = driver.find_element(By.NAME, "BPW0020")
        password_input.clear()
        password_input.send_keys(AOZORA_BANK_PASSWORD)
        
        # 3. ログイン実行
        print("ログイン実行...")
        login_btn = driver.find_element(By.NAME, "forward_BSM2010")
        login_btn.click()

        # ログイン完了待機
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "btn002-1")))
        print("ログイン成功")
            
        # 振込メニュー選択
        transfer_menu_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "btn002-1"))
        )
        transfer_menu_btn.click()

        # 4. 振込ループ処理
        for i in range(AOZORA_BANK_PAYMENT_COUNT):
            print(f"振込処理 {i+1} / {AOZORA_BANK_PAYMENT_COUNT} 回目開始")

            # 振込先選択画面へ
            print("振込先を選択...")
            select_payee_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "btn558-1"))
            )
            select_payee_btn.click()

            # 金額入力
            print(f"金額入力: {AMOUNT_OF_MONEY}円")
            amount_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".inputA02"))
            )
            amount_input.clear()
            amount_input.send_keys(AMOUNT_OF_MONEY)

            # 次へ
            print("次へ...")
            next_btn = driver.find_element(By.ID, "btn001")
            next_btn.click()

            # 取引確認画面
            print("取引確認画面。実行ボタンをクリックします...")
            execute_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".ui-button"))
            )
            execute_btn.click()

            # スマホ承認待機
            print("スマホ承認待ち (約30秒)...")
            try:
                next_loop_btn = WebDriverWait(driver, 60).until(
                    EC.element_to_be_clickable((By.ID, "btn006"))
                )
                print("振込完了を確認しました。")
                
                # 次の振込へ (選択画面へ戻る)
                next_loop_btn.click()
                
            except Exception as e:
                print("スマホ承認がタイムアウトしたか、画面遷移に失敗しました。")
                raise e

            print(f"振込処理 {i+1} 回目完了")
            # 少し待機
            time.sleep(1)

        # 5. ログアウト
        print("ログアウト処理...")
        logout_btn_img = driver.find_element(By.CSS_SELECTOR, "#cs_globalButton_logout > img")
        logout_btn_img.click()
        time.sleep(2)
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
