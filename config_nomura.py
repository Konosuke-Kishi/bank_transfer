# ======================================================
# 野村信託銀行の設定ファイル
# ======================================================
CONFIG = {
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
  'nomurabankOTPSecret': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
  # 野村信託銀行の振込回数
  'nomurabankPaymentCount': 10,
  # 野村信託銀行の架電する電話番号のXPath
  'nomurabankXPath': '/html/body/div[1]/div/div/form[1]/table[3]/tbody/tr/td/table/tbody/tr[2]/td/div/input',
  # 野村信託銀行のログインURL
  'nomurabankLoginUrl': 'https://hometrade.nomura.co.jp/web/rmfCmnEtcExcSso8Action.do'
}