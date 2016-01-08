/**
 * Created by DELL on 2015/12/15.
 */

var socketConn = new WebSocket("ws://192.168.234.139:5050/wssh/192.168.233.2/root");
//socketConn.open=function(event){
//    socketConn.send('i am ok');
//    socketConn.onmessage=function(event){
//        console.log('client received a message',event);
//    }
//      // 监听Socket的关闭
//  socketConn.onclose = function(event) {
//    console.log('Client notified socket has closed',event);
//  };

//};