
function ChessHome({socket}){
    const [player, setPlayer] = React.useState("");
	React.useEffect (() => {
        const onFinish = (mssg) => {
            $("#exampleModalCenter").modal("show");
            const color = (mssg == "b") ? "White" : "Black";
            setPlayer(color);
        }
		socket.on("game_over", onFinish);
        socket.emit("reset");
        return ()=>{
            socket.off("game_over", onFinish);
        }
	});
    return (
            <div className="row justify-content-center g-5">
                <ChessBoard socket={socket}/>
                <TitleCard socket={socket}/>
                <div class="modal fade" id="exampleModalCenter" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered" role="document">
                        <div class="modal-content">
                        <div class="modal-body text-center">
                           {player} has won! 
                        </div>
                        </div>
                    </div>
                </div>
            </div>
    )
};
