const express = require('express');
const clientIo = require("socket.io-client");
const clientSocket = clientIo(`http://localhost:8000`);

clientSocket.on('connect', () => {
  console.log('python server connected');
  // clientSocket.emit('tokenize', 'やめよう、とてもではないが小手先だけでは言いくるめられる様子ではない。エルディスも女王としての責務をこなしていく内、随分と口先が達者になったらしい。塔にいた頃と違い、やけにその舌が回る。下手に踏み込めば手痛い仕返しを食らうかもしれない。');
})

// clientSocket.on('tokenize_result', async (result) => {
//   result = await JSON.parse(result)
//   console.log(result)
// })

const http = require("http");
const proxy = require('express-http-proxy');
const socketIo = require('socket.io');
const rikai = require('./rikai');
var app = express();

// const port = process.env.PORT;
const port = 7001;
const front_path = process.env.FRONT_PATH;
// const port = 8005
// const front_path='http://localhost:8006'

app.use('/', front_path.includes('localhost') ? proxy(front_path) : express.static(front_path));

const server = http.createServer(app);
const io = socketIo(server)

var clients = {};

let dict = new rikai();
dict.init(false)

io.on('connection', (socket) => {
  console.log(`user ${socket.id} connected`)
  clients[socket.id] = socket
  socket.emit('message', 'you have sucessfully connected')
  socket.on('tokenize', (data) => {
    // console.log(`receiving tokenize request for ${data}`)
    clientSocket.emit('tokenize', {id: socket.id, data})
  });
  socket.on('tokenizeFragment', (data) => {
    // console.log(`receiving tokenizeFragment request for ${data}`)
    clientSocket.emit('tokenizeFragment', {id: socket.id, data})
  });
  socket.on('rikai', async (data) => {
    console.log(`receiving rikai request for ${data}`)
    e = dict.wordSearch(data, false);
    console.log(e)
    socket.emit('rikaiResult', e)
  });
  socket.on('rikaiMini', async (data) => {
    console.log(`receiving rikaiMini request for ${data}`)
    e = dict.wordSearch(data, false);
    console.log(e)
    socket.emit('rikaiMiniResult', e)
  });
  socket.on('hasOnlyHiragana', async (data) => {
    console.log(`receiving hasOnlyHiragana request for ${data}`)
    clientSocket.emit('hasOnlyHiragana', {id: socket.id, data})
  });
  socket.on('hasJapanese', async (data) => {
    console.log(`receiving hasJapanese request for ${data}`)
    clientSocket.emit('hasJapanese', {id: socket.id, data})
  });
  socket.on('disconnect', () => {
    console.log('user disconnected')
    delete clients[socket.id]
  })
});

clientSocket.on('hasOnlyHiraganaRes', async (result) => {
  result = await JSON.parse(result)
  let id = result[0]
  let data = result[1]
  console.log(`hasOnlyHiraganaRes: ${result}`);
  clients[id].emit('hasOnlyHiraganaRes', data)
})

clientSocket.on('hasJapaneseRes', async (result) => {
  result = await JSON.parse(result)
  let id = result[0]
  let test = result[1]
  let data = result[2]
  console.log(`hasJapaneseRes for ${data}: ${test}`);
  clients[id].emit('hasJapaneseRes', {test, data});
})

clientSocket.on('tokenizeResult', async (result) => {
  result = await JSON.parse(result)
  let id = result[0]
  let data = result[1]
  clients[id].emit('tokenizeResult', data)
})

clientSocket.on('tokenizeFragmentResult', async (result) => {
  result = await JSON.parse(result)
  // console.log(result)
  let id = result[0]
  let data = result[1]
  clients[id].emit('tokenizeFragmentResult', data)
})

server.listen(port, () => console.log(`Listening on port ${port}`));