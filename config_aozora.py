# ======================================================
# あおぞら銀行の設定ファイル
# ======================================================
CONFIG = {
  # 使用するブラウザの種類
  'useBrowser': 'Chrome', # "Chrome" or "Firefox"
  # ページ要素が見つかるまでの待機時間（秒）
  'elementWaitTime': 5,
  # デバイス認証の完了を待機する時間（秒）
  'deviceAuthWaitTime': 10,
  # あおぞら銀行の顧客番号
  'aozorabankCustomerNo': 'xxxxxxxxxx',
  # あおぞら銀行のログインパスワード
  'aozorabankLoginPassword': 'xxxxxxxx',
  # あおぞら銀行の振込回数
  'aozorabankPaymentCount': 9,
  # あおぞら銀行のログアウトボタンのCSSセレクタ
  'aozorabankCssSelector': '#cs_globalButton_logout > img',
  # あおぞら銀行のログインURL
  'aozorabankLoginUrl': 'https://www.ib2.aozorabank.co.jp/ib/index.do?PT=BS&CCT0080=0398'
}