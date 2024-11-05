function postRequest(apiUrl, data) {
    const request = new Request(
        apiUrl
    );

    return fetch(request,
        {
            method: 'POST',
            // body: JSON.stringify(data),
            body: data,
        },
    )
}

function writeToPage(parentNode, jsonData) {
    parentNode.innerHTML = '';
    Object.entries(jsonData).forEach(entry => {
        console.log(entry)
        const childNode = document.createElement('li');
        childNode.textContent = entry[0] + ": " + entry[1];
        parentNode.appendChild(childNode)
    })
}

document.getElementById('analyzeForm').addEventListener('submit', ev => {
    // stop page reloading on form submit
    ev.preventDefault();
})

document.getElementById('analyze').addEventListener('click', async (e) => {
    if (document.getElementById('formFile').value !== '') {
        const fileInput = document.getElementById('formFile');
        const analyzeButton = document.getElementById('analyze');
        const resetButton = document.getElementById('reset');
        const url = document.location.origin + '/api/analyze';
        const fileObject = fileInput.files[0];
        // const data = await fileObject.text(); //read data from file as text

        fileInput.classList.add('disabled');
        fileInput.disabled = 'disabled';
        analyzeButton.classList.add('disabled');

        resetButton.classList.remove('disabled');

        console.log(fileObject.type)
        // console.log(data)

        // post data to server to be analyzed and wait for result
        const result = await (await postRequest(url, fileObject)).json();
        console.log(result)
        const responseDataNode = document.getElementById('fileContents');
        // responseDataNode.innerHTML =  result;
        writeToPage(responseDataNode, result)
    }
})


document.getElementById('reset').addEventListener('click', ev => {
    const analyzeButton = document.getElementById('analyze');
    const fileInput = document.getElementById('formFile');
    const grades= document.getElementById("fileContents");
    ev.target.classList.add('disabled');

    analyzeButton.classList.remove('disabled');
    fileInput.classList.remove('disabled');
    fileInput.disabled = '';
    grades.innerHTML = '';
})




