const inspect = obj => {
    for (const prop in obj) {
        if (obj.hasOwnProperty(prop)) {
            console.log(`${prop}: ${obj[prop]}`)
        }
    }
}
function $(x) { return document.getElementById(x); }
var HOST = location.origin.replace(/^http/, 'ws');
//- HOST += ':' + port
console.log(HOST);


var socket = new WebSocket(HOST);
socket.onopen = function (e) {
    console.log("[open] Connection established");
    console.log("Sending to server");
    socket.send("Hi");
};
function updateTable(tableId, data) {
    //$('#' + tableId).empty(); //not really necessary
    var columnNames = [];
    Object.keys(data).forEach(function (key) {
        columnNames.push(data[key])
    });
    console.log(columnNames);
    table = $(tableId);
    table.deleteRow(1);
    var count = Object.keys(data).length;
    data = Object.keys(data);
    console.log(count);
    row = table.insertRow(-1);
    for (var i = 1; i < columnNames.length; i++) {
        var cell = row.insertCell(-1);
        cell.innerHTML = columnNames[i];
        console.log(columnNames[i])
    }
    // columnNames.forEach(function (columnName) {
    //     var cell = row.insertCell(-1);
    //     cell.innerHTML = columnNames[columnName];
    //     console.log(columnNames[columnName])
    // });
}
socket.onmessage = function (event) {
    console.log(typeof event.data);
    console.log(`[message] Data received from server: ${event.data}`);
    if (typeof event.data === typeof "") {
        //create a JSON object
        var jsonObject = JSON.parse(event.data);
        updateTable('display', jsonObject);
    }

};

socket.onclose = function (event) {
    if (event.wasClean) {
        console.log(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
    } else {
        // e.g. server process killed or network down
        // event.code is usually 1006 in this case
        console.log('[close] Connection died');
    }
};

socket.onerror = function (error) {
    //- console.log(`[error] ${error}`);
    inspect(error);
};






