// Importing modules

function App() {
    var socket = io();
    socket.on('connect', function () {
        socket.emit("collect_data");
    })
    //var socket = io({
        //path: "/chess_gui/"
      //});
    //var socket = io('http://127.0.0.1:5000', {
    //});

    return (
        <div className="container justify-content-center margin-md p-5">
            <ChessHome socket={socket}/>
            <Settings socket={socket}/>
        </div>
    );
}
  