
document.getElementById('submitBtn').addEventListener('click', function(event) {
    var inputValue = document.getElementById('userInput').value;
    var data = {data: inputValue};

    console.log(data.data);cd 
})

app.get('/api/data', (req, res) => {
    res.send(data.data);
})