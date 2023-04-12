// Importing modules

function App() {
  
   var socket = io();
    //var socket = io({
        //path: "/chess_gui/"
      //});
    //var socket = io('http://127.0.0.1:5000', {
    //});

    socket.on('connect', function() {
        socket.emit('my event', {data: 'I\'m connected!'});
    });

    return (
        <div className="container justify-content-center margin-md p-5">
            <ChessHome socket={socket}/>
        </div>
    );
}
  