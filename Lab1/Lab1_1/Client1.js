const sget = require('sget');
const net = require("net");

const IP = sget("IP: ");
const PORT = sget("PORT: ");
console.log(IP + ":" + PORT);

var client = new net.Socket();
client.connect(parseInt(PORT, 10), IP.trim(), function() {
	console.log('Connected');
	client.write('Hello, server!');
});


client.on('data', function(data) {
	console.log('Received: ' + data);
	let mes = sget();
	client.write(mes);


	if(mes.trim() == "exit")
			client.destroy();//client.write('q');
	//client.destroy(); // kill client after server's response
});


client.on('close', function() {
	client.destroy();
	console.log('Connection closed');
});
