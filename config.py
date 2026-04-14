# ======================================================
# 共通設定ファイル
# ======================================================
CONFIG = {
  # ブラウザウィンドウの幅
  'windowWidth': 1475,
  # ブラウザウィンドウの高さ
  'windowHeight': 1060,
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
  # LINE Messaging API情報
  'lineUserId': '<LINE Messaging API設定で払い出したユーザID>',
  'lineChannelToken': '<LINE Messaging API設定で払い出したチャネルアクセストークン（長期）>',
  # Chromeのパスとバージョン取得コマンド
  'chromePath': "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  'cmdOptions': "--version"
}