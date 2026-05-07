# ======================================================
# auじぶん銀行の設定ファイル
# ======================================================
CONFIG = {
  # 使用するブラウザの種類
  'useBrowser': 'Chrome', # "Chrome" or "Firefox"
  # ページ要素が見つかるまでの待機時間（秒）
  'elementWaitTime': 5,
  # デバイス認証の完了を待機する時間（秒）
  'deviceAuthWaitTime': 120,
  # auじぶん銀行の顧客番号
  'aubankCustomerNo': 'xxxxxxxxxx',
  # auじぶん銀行のログインパスワード
  'aubankLoginPassword': 'xxxxxxxx',
  # auじぶん銀行の振込回数
  'aubankPaymentCount': 15,
  # auじぶん銀行の振込先選択のCSSセレクタ
  'aubankCssSelector': '.c-box-result-normal-result-item:nth-child(1) .c-box-result-item-bank-branch',
  # auじぶん銀行のログインURL
  'aubankLoginUrl': 'https://www.jibunbank.co.jp/redirect/login.html?cid=tpkv_pc'
}