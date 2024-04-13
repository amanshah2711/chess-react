
function TitleCard({socket}){
    const [player, setPlayer] = React.useState("White");
    const [moves, setMoves] = React.useState("");
    const [possible, setPossible] = React.useState("");
    const handleReset = () => {
        socket.emit('reset');
    };
    const handleUndo = () => {
        socket.emit('undo');
    };

	React.useEffect (() => {
        const onMove = (recv) => setMoves(recv);
        const onPossible = (recv) => setPossible(recv);
        const onUpdate = (recv) => {
            if (recv.split(" ")[1] == "w") {
                setPlayer("White");
            } else {
                setPlayer("Black");
            }
        }
		socket.on("move_data", onMove);
        socket.on("possible", onPossible);
        socket.on("update", onUpdate);
        return ()=>{
            socket.off("move_data", onMove);
            socket.off("possible", onPossible);
            socket.off("update", onUpdate);
        }
	});

    return (
            <div className="col-3">
                <div className="row text-center">
                    <h3>Game Data</h3>
                    <h4>Player: {player} </h4>
                </div>
                <div className="row text-center">
                    &nbsp; 
                    <button className="btn btn-primary" onClick={handleUndo}>Undo</button>
                    &nbsp; 
                    <button className="btn btn-danger" onClick={handleReset}>Reset</button>
                </div>
                &nbsp; 
                <div className="row text-center">
                    <p> Possible Moves: {possible} </p>
                </div>
                <div className="row text-center">
                    <p> Move History: {moves} </p>
                </div>
            </div>
    )
};
