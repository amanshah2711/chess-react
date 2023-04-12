"use strict";

function ChessCoordinate(row, col) {
    this.row = 8 - row;
    this.col = String.fromCharCode(97 + col);
}
ChessCoordinate.prototype.toString = function CoordinateToString() {
    return "" + this.col + this.row;
};


"use strict";

function Board(_ref) {
    var width = _ref.width,
        height = _ref.height,
        color_map = _ref.color_map,
        pieces = _ref.pieces,
        callback = _ref.callback;

    var handleClick = function boardCallback(coordinate) {
        callback(coordinate);
    };
    var board = [];
    for (var i = 0; i < height; i += 1) {
        var row = [];
        for (var j = 0; j < width; j += 1) {
            var name = i.toString() + " " + j.toString();
            row.push(React.createElement(Square, { name: name, styler: color_map(i, j), piece: pieces[i][j], key: j, coordinate: new ChessCoordinate(i, j), callback: handleClick }));
        }
        board.push(React.createElement(
            "div",
            { className: "row m-0", key: i },
            row
        ));
    }
    return React.createElement(
        "div",
        { className: "col-9 p-0 border border-dark" },
        board
    );
};


"use strict";

var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

function TitleCard(_ref) {
    var socket = _ref.socket;

    var _React$useState = React.useState("White"),
        _React$useState2 = _slicedToArray(_React$useState, 2),
        player = _React$useState2[0],
        setPlayer = _React$useState2[1];

    var _React$useState3 = React.useState(""),
        _React$useState4 = _slicedToArray(_React$useState3, 2),
        fen = _React$useState4[0],
        setFen = _React$useState4[1];

    var _React$useState5 = React.useState(""),
        _React$useState6 = _slicedToArray(_React$useState5, 2),
        moves = _React$useState6[0],
        setMoves = _React$useState6[1];

    var _React$useState7 = React.useState(""),
        _React$useState8 = _slicedToArray(_React$useState7, 2),
        possible = _React$useState8[0],
        setPossible = _React$useState8[1];

    React.useEffect(function () {
        socket.on("update", function (recv) {
            setFen(recv);
            if (recv.split(" ")[1] == "w") {
                setPlayer("White");
            } else {
                setPlayer("Black");
            }
        });
    });
    var handleReset = function handleReset() {
        socket.emit('reset');
    };
    var handleUndo = function handleUndo() {
        socket.emit('undo');
    };

    React.useEffect(function () {
        socket.on("move_data", function (recv) {
            setMoves(recv);
        });
        socket.on("possible", function (recv) {
            setPossible(recv);
        });
    });

    return React.createElement(
        "div",
        { className: "col-3" },
        React.createElement(
            "div",
            { className: "row text-center" },
            React.createElement(
                "h3",
                null,
                "Game Data"
            ),
            React.createElement(
                "h4",
                null,
                "Player: ",
                player,
                " "
            )
        ),
        React.createElement(
            "div",
            { className: "row text-center" },
            React.createElement(
                "button",
                { className: "btn btn-primary", onClick: handleUndo },
                "Undo"
            ),
            React.createElement(
                "button",
                { className: "btn btn-danger", onClick: handleReset },
                "Reset"
            )
        ),
        React.createElement(
            "div",
            { className: "row text-center" },
            React.createElement(
                "p",
                null,
                " Possible Moves: ",
                possible,
                " "
            )
        ),
        React.createElement(
            "div",
            { className: "row text-center" },
            React.createElement(
                "p",
                null,
                " Move History: ",
                moves,
                " "
            )
        )
    );
};


"use strict";

function Square(props) {
    var onClick = function onClick(e) {
        return props.callback(props.coordinate);
    };
    var divStyle = {
        padding: "2\%"
    };
    for (var key in props.styler) {
        divStyle[key] = props.styler[key];
    }

    return React.createElement(
        "div",
        { className: "col", style: divStyle, onClick: onClick },
        React.createElement("img", { src: props.piece, style: { maxWidth: "100\%", maxHeight: "100\%" }, alt: "" })
    );
};


"use strict";

function ChessHome(_ref) {
    var socket = _ref.socket;

    return React.createElement(
        "div",
        { className: "row justify-content-center g-5" },
        React.createElement(ChessBoard, { socket: socket }),
        React.createElement(TitleCard, { socket: socket }),
        React.createElement("div", { className: "col-1" })
    );
};


'use strict';

var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

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

var manhattanDistance = function manhattanDistance(x, y) {
	return Math.abs(x) + Math.abs(y);
};
var BOARD_DIM = 8;

function isNumber(char) {
	return (/^\d$/.test(char)
	);
}

var nameToPiece = {
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
};

function generateBoard(fen) {
	var arr = new Array(BOARD_DIM);
	for (var i = 0; i < BOARD_DIM; i += 1) {
		arr[i] = new Array(BOARD_DIM);
	}
	var board = fen.split(" ")[0];
	var index = 0;
	var _iteratorNormalCompletion = true;
	var _didIteratorError = false;
	var _iteratorError = undefined;

	try {
		for (var _iterator = board[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
			var piece = _step.value;

			if (piece != "/") {
				if (isNumber(piece)) {
					for (var _k = 0; _k < piece; _k += 1) {
						var _i = Math.floor(index / 8);
						var j = index % 8;
						arr[_i][j] = nameToPiece["blank"];
						index += 1;
					}
				} else {
					var _i2 = Math.floor(index / 8);
					var _j = index % 8;
					arr[_i2][_j] = nameToPiece[piece];
					index += 1;
				}
			}
		}
	} catch (err) {
		_didIteratorError = true;
		_iteratorError = err;
	} finally {
		try {
			if (!_iteratorNormalCompletion && _iterator.return) {
				_iterator.return();
			}
		} finally {
			if (_didIteratorError) {
				throw _iteratorError;
			}
		}
	}

	return arr;
}

function ChessBoard(_ref) {
	var socket = _ref.socket;

	var _React$useState = React.useState({ "startPos": null, "endPos": null }),
	    _React$useState2 = _slicedToArray(_React$useState, 2),
	    activePieces = _React$useState2[0],
	    setActivePieces = _React$useState2[1];

	var _React$useState3 = React.useState(generateBoard("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")),
	    _React$useState4 = _slicedToArray(_React$useState3, 2),
	    grid = _React$useState4[0],
	    setGrid = _React$useState4[1];

	var handleClick = function chessCallback(coordinate) {
		if (activePieces["startPos"] == null) {
			setActivePieces({ "startPos": coordinate.toString(), "endPos": null });
			socket.emit("chess_gui/selected", coordinate.toString());
		} else if (activePieces["startPos"] == coordinate) {
			setActivePieces({ "startPos": null, "endPos": null });
			socket.emit('selected', '');
		} else {
			setActivePieces({ "startPos": activePieces["startPos"], "endPos": coordinate.toString() });
			socket.emit('make_move', activePieces["startPos"].toString() + coordinate.toString());
			socket.emit('selected', '');
			setActivePieces({ "startPos": null, "endPos": null });
		}
	};

	var tile_styler = function tile_styler(i, j) {
		return manhattanDistance(i, j) % 2 === 0 ? { backgroundColor: "#93602B" } : { backgroundColor: "#EACFB6" };
	};
	var augmented_styler = function augmented_styler(i, j) {
		return activePieces["startPos"] == new ChessCoordinate(i, j).toString() ? { backgroundColor: "turquoise" } : {};
	};
	var chess_styler = function chess_styler(i, j) {
		return Object.assign({}, tile_styler(i, j), augmented_styler(i, j));
	};

	React.useEffect(function () {
		socket.on("update", function (recv) {
			setGrid(generateBoard(recv));
		});
	});

	return React.createElement(Board, { width: BOARD_DIM, height: BOARD_DIM, color_map: chess_styler, pieces: grid, callback: handleClick });
};


'use strict';

// Importing modules

function App() {

    var socket = io();
    //var socket = io({
    //path: "/chess_gui/"
    //});
    //var socket = io('http://127.0.0.1:5000', {
    //});

    socket.on('connect', function () {
        socket.emit('my event', { data: 'I\'m connected!' });
    });

    return React.createElement(
        'div',
        { className: 'container justify-content-center margin-md p-5' },
        React.createElement(ChessHome, { socket: socket })
    );
}


'use strict';

var app = ReactDOM.render(React.createElement(App, null), document.getElementById('content'));

