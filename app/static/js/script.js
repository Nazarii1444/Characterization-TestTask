let fileData = null;

async function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    const response = await fetch('api/v1/stdf/decode', {
        method: 'POST',
        body: formData
    });

    if (response.ok) {
        const data = await response.json();
        fileData = data;
        displayTable(data);
    } else {
        alert('Failed to upload file');
    }
}

function displayTable(data) {
    const tableBody = document.getElementById('fileTable').getElementsByTagName('tbody')[0];
    tableBody.innerHTML = '';

    data.parts.forEach(part => {
        part.tests.forEach(test => {
            const row = tableBody.insertRow();
            row.innerHTML = `
                <td><input type="text" value="${test.test_name}" onchange="updateTestName(this, '${test.test_name}')"></td>
                <td><input type="number" value="${test.test_value}" onchange="updateTestValue(this, ${test.test_value})"></td>
                <td><input type="number" value="${test.low_limit}" onchange="updateLowLimit(this, ${test.low_limit})"></td>
                <td><input type="number" value="${test.high_limit}" onchange="updateHighLimit(this, ${test.high_limit})"></td>
                <td><input type="checkbox" ${test.passed ? 'checked' : ''} onchange="updateTestStatus(this, ${test.passed})"></td>
            `;
        });
    });
}

function updateTestName(input, testName) {
    const test = fileData.parts.flatMap(part => part.tests).find(t => t.test_name === testName);
    if (test) {
        test.test_name = input.value;
    }
}

function updateTestValue(input, oldValue) {
    const test = fileData.parts.flatMap(part => part.tests).find(t => t.test_value === oldValue);
    if (test) {
        test.test_value = parseFloat(input.value);
    }
}

function updateLowLimit(input, oldValue) {
    const test = fileData.parts.flatMap(part => part.tests).find(t => t.low_limit === oldValue);
    if (test) {
        test.low_limit = parseFloat(input.value);
    }
}

function updateHighLimit(input, oldValue) {
    const test = fileData.parts.flatMap(part => part.tests).find(t => t.high_limit === oldValue);
    if (test) {
        test.high_limit = parseFloat(input.value);
    }
}

function updateTestStatus(input, passed) {
    const test = fileData.parts.flatMap(part => part.tests).find(t => t.passed === passed);
    if (test) {
        test.passed = input.checked;
    }
}

function gatherTableData() {
    const tableBody = document.getElementById('fileTable').getElementsByTagName('tbody')[0];
    const rows = Array.from(tableBody.rows);

    fileData.parts.forEach((part, partIndex) => {
        part.tests.forEach((test, testIndex) => {
            const row = rows.shift();
            const inputs = row.getElementsByTagName('input');

            test.test_name = inputs[0].value;
            test.test_value = parseFloat(inputs[1].value);
            test.low_limit = parseFloat(inputs[2].value);
            test.high_limit = parseFloat(inputs[3].value);
            test.passed = inputs[4].checked;
        });
    });

    // console.log('Updated fileData:', fileData);
}

async function downloadFile() {
    const filename = document.getElementById('filenameInput').value || 'encoded.bin';

    gatherTableData();

    const response = await fetch(`api/v1/stdf/encode?filename=${encodeURIComponent(filename)}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(fileData)
    });

    if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    } else {
        alert('Failed to download file');
    }
}