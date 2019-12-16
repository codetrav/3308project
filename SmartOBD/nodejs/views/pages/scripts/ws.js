const inspect = obj => {
    for (const prop in obj) {
        if (obj.hasOwnProperty(prop)) {
            console.log(`${prop}: ${obj[prop]}`)
        }
    }
}
var HOST = location.origin.replace(/^http/, 'ws')
port = '#{ port }'
HOST += port
console.log(HOST)
var socket = new WebSocket(HOST);
socket.onopen = function (e) {
    console.log("[open] Connection established");
    console.log("Sending to server");
    socket.send("My name is John");
};

socket.onmessage = function (event) {
    if (typeof (event.data) === String) {
        //create a JSON object
        var jsonObject = JSON.parse(event.data);
        var speed = jsonObject["SPEED KMPH"]
        console.log(speed);
    }
    console.log(`[message] Data received from server: ${event.data}`);
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
    console.log(`[error] ${error}`);
    inspect(error);
};






