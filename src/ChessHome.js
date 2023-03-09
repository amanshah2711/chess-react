import ChessBoard from "./ChessBoard";
import TitleCard from "./TitleCard";

function ChessHome({socket}){
    return (
            <div className="row justify-content-center g-5">
                <ChessBoard socket={socket}/>
                <TitleCard socket={socket}/>
                <div className="col-1"></div>
            </div>
    )
};

export default ChessHome;