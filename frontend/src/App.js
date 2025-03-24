document.addEventListener('DOMContentLoaded', () => {
    // ユーザー入力を格納する配列
    const inputArray = [];
  
    // DOM要素の取得
    const userInputElem = document.getElementById('userInput');
    const submitBtn = document.getElementById('submitBtn');
    const resultContainer = document.getElementById('resultContainer');
  
    // 送信ボタンがクリックされたときの処理
    submitBtn.addEventListener('click', () => {
      const userInputValue = userInputElem.value;
      // 入力が空の場合は何もしない
      if (userInputValue.trim() === '') return;
  
      // 必要に応じてユーザー入力を加工（例: トリム処理）
      const processedValue = userInputValue.trim();
  
      // 配列に加工済みの入力を追加
      inputArray.push(processedValue);
  
      // 入力欄をクリア
      userInputElem.value = '';
  
      // 配列の内容をレンダー
      renderResults(inputArray, resultContainer);
    });
  });
  
  /**
   * 配列の内容をレンダーする関数
   * @param {Array} array - ユーザー入力の配列
   * @param {HTMLElement} container - レンダー先のコンテナ要素
   */
  function renderResults(array, container) {
    // 既存のコンテンツをクリア
    container.innerHTML = '';
  
    // 結果をリスト形式で表示
    const ul = document.createElement('ul');
    array.forEach(item => {
      const li = document.createElement('li');
      li.textContent = item;
      ul.appendChild(li);
    });
    container.appendChild(ul);
  }