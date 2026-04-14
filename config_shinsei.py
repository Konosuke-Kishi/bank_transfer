# ======================================================
# SBI新生銀行の設定ファイル
# ======================================================
CONFIG = {
  # SBI新生銀行の顧客番号
  'shinseibankCustomerNo': 'xxxxxxxxxx',
  # SBI新生銀行のログインパスワード
  'shinseibankLoginPassword': 'xxxxxxxx',
  # SBI新生銀行の振込回数
  'shinseibankPaymentCount': 10,
  # SBI新生銀行の振込先選択のXPath
  'shinseibankXPath': '/html/body/div[1]/div[2]/div[1]/section[2]/div/table/tbody/tr/td[6]/button/span',
  # SBI新生銀行のログインURL
  'shinseibankLoginUrl': 'https://bk.web.sbishinseibank.co.jp/SFC/apps/services/www/SFC/desktopbrowser/default/login?mode=1&intcid=login_mega'
}