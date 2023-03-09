import ChessBoard from "./ChessBoard";
import TitleCard from "./TitleCard";

function ChessHome(){
    // var socket = io();
    // socket.on('connect', function() {
    //     socket.emit('my event', {data: 'I\'m connected!'});
    // });
    return (
        <div className="container justify-content-center">
            <div className="row justify-content-center">
                <div className="col-6 border border-dark">
                    <ChessBoard/>
                </div>
                <div className="col-1"></div>
                <TitleCard/>
            </div>
        </div>
    )
};

export default ChessHome;