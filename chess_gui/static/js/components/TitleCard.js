
function TitleCard({socket}){
    const [player, setPlayer] = React.useState("White");
    const [fen, setFen] = React.useState("");
    const [moves, setMoves] = React.useState("");
    const [possible, setPossible] = React.useState("");
    React.useEffect (() => {
        socket.on("update", (recv) => {
            setFen(recv)
            if (recv.split(" ")[1] == "w") {
                setPlayer("White");
            } else {
                setPlayer("Black");
            }
        });
    });
    const handleReset = () => {
        socket.emit('reset');
    };
    const handleUndo = () => {
        socket.emit('undo');
    };

	React.useEffect (() => {
		socket.on("move_data", (recv) => {
			setMoves(recv);
		});
        socket.on("possible", (recv) => {
            setPossible(recv);
        })
	});

    return (
            <div className="col-3">
                <div className="row text-center">
                    <h3>Game Data</h3>
                    <h4>Player: {player} </h4>
                </div>
                <div className="row text-center">
                    <button className="btn btn-primary" onClick={handleUndo}>Undo</button>
                    <button className="btn btn-danger" onClick={handleReset}>Reset</button>
                </div>
                <div className="row text-center">
                    <p> Possible Moves: {possible} </p>
                </div>
                <div className="row text-center">
                    <p> Move History: {moves} </p>
                </div>
            </div>
    )
};
