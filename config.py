# ======================================================
# 設定ファイル
# ======================================================
CONFIG = {
  # 使用するブラウザの種類
  'useBrowser': 'Chrome', # "Chrome" or "Firefox"
  # ヘッドレスブラウザを使用するかどうか
  'useHeadlessBrowser': False, # True or False
  # ページ要素が見つかるまでの待機時間（秒）
  'elementWaitTime': 30,
  # デバイス認証の完了を待機する時間（秒）
  'deviceAuthWaitTime': 120,
  # Chromeユーザプロファイルの格納先パス（必須）
  'chromeUserDataDir': '/Users/<Macのユーザ名>/Library/Application Support/Google/Chrome/Selenium', #左記はMacの例
  # Firefoxユーザプロファイルの格納先パス（必須）
  'firefoxUserDataDir': '/Users/<Macのユーザ名>/Library/Application Support/Firefox/Profiles/xxxxxxxx.プロファイル 1', #左記はMacの例
  # 入金金額（全銀行共通）
  'amountOfMoney': 10000,
  # auじぶん銀行の顧客番号
  'aubankCustomerNo': 'xxxxxxxxxx',
  # auじぶん銀行のログインパスワード
  'aubankLoginPassword': 'xxxxxxxx',
  # auじぶん銀行の振込回数
  'aubankPaymentCount': 15,
  # SBI新生銀行の顧客番号
  'shinseibankCustomerNo': 'xxxxxxxxxx',
  # SBI新生銀行のログインパスワード
  'shinseibankLoginPassword': 'xxxxxxxx',
  # SBI新生銀行の振込回数
  'sbishinseibankPaymentCount': 10,
  # あおぞら銀行の顧客番号
  'aozorabankCustomerNo': 'xxxxxxxxxx',
  # あおぞら銀行のログインパスワード
  'aozorabankLoginPassword': 'xxxxxxxx',
  # あおぞら銀行の振込回数
  'aozorabankPaymentCount': 9,
  # 野村信託銀行 店番号
  'nomurabankBranchCode': 'xxx',
  # 野村信託銀行 口座番号
  'nomurabankAccountNum': 'xxxxxxxx',
  # 野村信託銀行 ログインパスワード
  'nomurabankLoginPassword': 'xxxxxxxx',
  # 野村信託銀行 認証用電話番号
  'nomurabankPhone1': 'xxx',
  'nomurabankPhone2': 'xxxx',
  'nomurabankPhone3': 'xxxx',
  # 野村信託銀行 ワンタイム認証セットアップキー
  'nomurabankOTPSecret': 'xxxxxxxxxxxx',
  # 野村信託銀行の振込回数
  'nomurabankPaymentCount': 10,
  # LINE Messaging API情報
  'lineUserId': '<LINE Messaging API設定で払い出したユーザID>',
  'lineChannelToken': '<LINE Messaging API設定で払い出したチャネルアクセストークン（長期）>'
}