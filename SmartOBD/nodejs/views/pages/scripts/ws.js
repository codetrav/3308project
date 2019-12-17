const inspect = obj => {
    for (const prop in obj) {
        if (obj.hasOwnProperty(prop)) {
            console.log(`${prop}: ${obj[prop]}`)
        }
    }
}
function $(x) { return document.getElementById(x); }
var HOST = location.origin.replace(/^http/, 'ws');
console.log(HOST);


var socket = new WebSocket(HOST);
socket.onopen = function (e) {
    console.log("[open] Connection established");
    console.log("Sending to server");
    socket.send("Hi");
};
function updateTable(tableId, data) {
    var columnNames = [];
    Object.keys(data).forEach(function (key) {
        columnNames.push(data[key])
    });
    console.log(columnNames);
    table = $(tableId);
    console.log(table.rows.length)
    // if (table.rows.length > 3) {
    //     for (var i = 0; i < columnNames.length; i++) {
    //         table.deleteRow(i);
    //     }
    // }
    // else {
    //     table.deleteRow(1);
    // }
    var count = Object.keys(data).length;
    data = Object.keys(data);
    console.log(count);
    for (var i = 0; i < columnNames.length; i++) {
        row = table.rows[i]
        var cell = row.cells[0];
        cell.innerHTML = columnNames[i+1];
        console.log(columnNames[i+1])
    }

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
    inspect(error);
};






