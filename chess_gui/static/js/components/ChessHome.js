
function ChessHome({socket}){
    return (
            <div className="row justify-content-center g-5">
                <ChessBoard socket={socket}/>
                <TitleCard socket={socket}/>
            </div>
    )
};
