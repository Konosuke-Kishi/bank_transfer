// ======================================================
// 野村信託銀行の認証番号入力自動化スクリプト
// ======================================================

(function () {
  'use strict';

  const columns = ["あ", "い", "う", "え"];
  const directCardNumbers = [ // ダイレクト番号をここに入力
    ["xx", "xx", "xx", "xx"], // A列
    ["xx", "xx", "xx", "xx"], // B列
    ["xx", "xx", "xx", "xx"], // C列
    ["xx", "xx", "xx", "xx"], // D列
  ];

  /**
   * 確認番号のマッピングデータを作成する
   *
   * @return {Object} mappedCardNumbers - 列ごとに整理した確認番号一覧
   */
  function makeDirectNumberMaps () {
    const mappedCardNumbers = {};
    columns.forEach((col, index) => {
      const rowNumbers = directCardNumbers.map(row => row[index]);
      mappedCardNumbers[col] = rowNumbers; // e.g. { "あ": ["01", "11", "21", "31"] }
    });
    return mappedCardNumbers;
  }

  /**
   * 全角文字を半角文字に変換する
   *
   * @param {String} str - 変換対象の文字列
   * @return {String} halfWidthText - 変換された半角文字列
   */
  function zenkaku2Hankaku (str) {
    const halfWidthText = str.replace(/[Ａ-Ｚａ-ｚ０-９－]/g, function (s) {
      return String.fromCharCode(s.charCodeAt(0) - 0xfee0);
    });
    return halfWidthText;
  }

  /**
   * 現在求められている確認番号のキーを配列で返す
   *
   * @return {Array} currentKeys - 確認番号のキー配列 e.g. ["えB", "あC"]
   */
  function getCurrentKeys () {
    let currentKeys = [];
    const areas = document.querySelectorAll('div.normalArea:nth-child(2), div.normalArea:nth-child(3)');

    areas.forEach(area => {
      let labelText = area.textContent.replace(/[\s&nbsp;‐]/g, "").trim(); // 不要な空白や特殊文字を削除
      labelText = labelText.replace(/^.*?は/, ""); // 「ひとつめは」「ふたつめは」などの不要な部分を削除

      const columnLetter = labelText.charAt(0); // 最初の文字が列名に相当 e.g. "え"
      const rowLetter = zenkaku2Hankaku(labelText.charAt(1)); // 2文字目が行名に相当 e.g. "B"
      const currentKey = `${columnLetter}-${rowLetter}`; // e.g. "え-B"

      currentKeys.push(currentKey);
    });

    console.log("currentKeys:", currentKeys);
    return currentKeys;
  }

  /**
   * 現在求められている確認番号の値を配列で返す
   *
   * @param {Array} currentKeys - 確認番号のキー配列 e.g. ["あ-A", "い-B"]
   * @return {Array} currentNumbers - 現在の確認番号の値配列 e.g. ["01", "12"]
   */
  function getCurrentNumbers (currentKeys) {
    let currentNumbers = [];
    const directNumbers = makeDirectNumberMaps();

    currentKeys.map(currentKey => {
      const [columnLetter, rowLetter] = currentKey.split('-');
      const rowIdx = rowLetter.charCodeAt(0) - 'A'.charCodeAt(0); // A->0, B->1, C->2, D->3

      if (directNumbers[columnLetter] && rowIdx >= 0 && rowIdx < 4) {
        const currentNumber = directNumbers[columnLetter][rowIdx];
        currentNumbers.push(currentNumber);
      }
    });

    console.log("currentNumbers:", currentNumbers);
    return currentNumbers;
  }

  /**
   * 入力欄に確認番号をセットする
   */
  function autoFillNumbers () {
    const currentKeys = getCurrentKeys();
    const currentNumbers = getCurrentNumbers(currentKeys);
    const passwordFields = document.querySelectorAll('input[type="password"]');

    // ひとつめの認証番号欄
    if (passwordFields[1]) {
      passwordFields[1].value = currentNumbers[0] || ''; // ひとつめの番号
    }

    // ふたつめの認証番号欄
    if (passwordFields[2]) {
      passwordFields[2].value = currentNumbers[1] || ''; // ふたつめの番号
    }
  }

  // スクリプト実行
  autoFillNumbers();
})();