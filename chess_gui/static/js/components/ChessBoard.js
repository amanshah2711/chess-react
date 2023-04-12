
var K = 'chess_gui/static/img/wK.png';
var Q = 'chess_gui/static/img/wQ.png';
var B = 'chess_gui/static/img/wB.png';
var N = 'chess_gui/static/img/wN.png';
var R = 'chess_gui/static/img/wR.png';
var P = 'chess_gui/static/img/wP.png';
var k = 'chess_gui/static/img/bK.png';
var q = 'chess_gui/static/img/bQ.png';
var b = 'chess_gui/static/img/bB.png';
var n = 'chess_gui/static/img/bN.png';
var r = 'chess_gui/static/img/bR.png';
var p = 'chess_gui/static/img/bP.png';
var blank = 'chess_gui/static/img/blank.png';

const manhattanDistance = (x,y) => Math.abs(x) + Math.abs(y);
const BOARD_DIM = 8

function isNumber(char) {
	return /^\d$/.test(char);
  }

const nameToPiece = {
    "K": K,
    "Q": Q,
    "B": B,
    "N": N,
    "R": R,
    "P": P,
    "k": k,
    "q": q,
    "b": b,
    "n": n,
    "r": r,
    "p": p,
    "blank": blank
}

function generateBoard(fen){
	var arr = new Array(BOARD_DIM)
	for (let i = 0; i < BOARD_DIM; i += 1){
		arr[i] = new Array(BOARD_DIM);
	}
	let board = fen.split(" ")[0];
	let index = 0;
	for (const piece of board) {
		if (piece != "/"){
			if (isNumber(piece)){
				for (let k = 0; k < piece; k += 1){
					let i = Math.floor(index / 8);
					let j = index % 8;
					arr[i][j] = nameToPiece["blank"];
					index += 1
				}

			} else {
				let i = Math.floor(index / 8);
				let j = index % 8;
				arr[i][j] = nameToPiece[piece];
				index += 1;
			}
		}
	}
	return arr;
}

function ChessBoard({socket}){
	const [activePieces, setActivePieces] = React.useState({"startPos": null, "endPos": null});
	const [grid, setGrid] = React.useState(generateBoard("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"));
	const handleClick = function chessCallback(coordinate){
		if (activePieces["startPos"] == null) {
			setActivePieces({"startPos" : coordinate.toString(), "endPos" : null});
			socket.emit("chess_gui/selected", coordinate.toString())
		} else if (activePieces["startPos"] == coordinate) {
			setActivePieces({"startPos" : null, "endPos" : null});
			socket.emit('selected', '')
		} else {
			setActivePieces({"startPos" : activePieces["startPos"], "endPos" : coordinate.toString()});
			socket.emit('make_move', activePieces["startPos"].toString() + coordinate.toString());
			socket.emit('selected', '')
			setActivePieces({"startPos" : null, "endPos" : null});
		}

	}

	const tile_styler = (i,j) => (manhattanDistance(i,j) % 2 === 0) ? {backgroundColor : "#93602B"} : {backgroundColor: "#EACFB6"}
	const augmented_styler = (i,j) => (activePieces["startPos"] == new ChessCoordinate(i,j).toString()) ? {backgroundColor: "turquoise"} : {};
	const chess_styler = (i,j) => Object.assign({}, tile_styler(i,j), augmented_styler(i,j));

	React.useEffect (() => {
		socket.on("update", (recv) => {
			setGrid(generateBoard(recv));
		});
	});

	return (
			<Board width={BOARD_DIM} height={BOARD_DIM} color_map={chess_styler} pieces={grid} callback={handleClick}></Board>
	)
};

