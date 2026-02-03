# ======================================================
# 設定ファイル
# ======================================================
CONFIG = {
  # 使用するブラウザの種類
  'useBrowser': 'Chrome',
  # Chromeユーザプロファイルの格納先パス（必須）
  'chromeUserDataDir': '/Users/<Macのユーザ名>/Library/Application Support/Google/Chrome/Selenium', #左記はMacの例
  # Firefoxユーザプロファイルの格納先パス（必須）
  'firefoxUserDataDir': '/Users/<Macのユーザ名>/Library/Application Support/Firefox/Profiles/xxxxxxxx.selenium-client.profile', #左記はMacの例
  # 入金金額（全銀行共通）
  'amountOfMoney': 10000,
  # auじぶん銀行の顧客番号
  'aubankCustomerNo': 'xxxxxxxxxx',
  # auじぶん銀行のログインパスワード
  'aubankLoginPassword': 'xxxxxxxx',
  # SBI新生銀行の顧客番号
  'sbishinseibankCustomerNo': 'xxxxxxxxxx',
  # SBI新生銀行のログインパスワード
  'sbishinseibankLoginPassword': 'xxxxxxxx',
  # あおぞら銀行の顧客番号
  'aozorabankCustomerNo': 'xxxxxxxxxx',
  # あおぞら銀行のログインパスワード
  'aozorabankLoginPassword': 'xxxxxxxx',
  # 野村信託銀行 店番号
  'nomuraTrustBankBranchCode': 'xxx',
  # 野村信託銀行 口座番号
  'nomuraTrustBankAccountNum': 'xxxxxxxx',
  # 野村信託銀行 ログインパスワード
  'nomuraTrustBankLoginPassword': 'xxxxxxxx',
  # 野村信託銀行 取引パスワード
  'nomuraTrustBankTransPassword': 'xxxxxxxx',
  # 野村信託銀行 認証用電話番号
  'nomuraTrustBankPhone1': 'xxx',
  'nomuraTrustBankPhone2': 'xxxx',
  'nomuraTrustBankPhone3': 'xxxx',
  # 認証番号入力用のJavaScriptファイルパス
  'inputJSFilePath': 'input_pin.js',
  # auじぶん銀行の振込回数
  'aubankPaymentCount': 15,
  # SBI新生銀行の振込回数
  'sbishinseibankPaymentCount': 10,
  # あおぞら銀行の振込回数
  'aozorabankPaymentCount': 9,
  # 野村信託銀行の振込回数
  'nomuraTrustBankPaymentCount': 10,
}