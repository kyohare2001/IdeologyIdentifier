
document.getElementById('submitBtn').addEventListener('click', async function(event) {
    var inputValue = document.getElementById('userInput').value;
    var data = {data: inputValue};

    try {
        // As a JSON file send data to the server
        const res = await fetch('/api/data', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });
        // async function は非同期処理を行うための関数です。await キーワードを使用して、Promiseが解決されるのを待ちます。
        const json = await res.json();
        console.log('サーバー応答:', json);
      } catch (err) {
        console.error('送信エラー:', err);
      }
})