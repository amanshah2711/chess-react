import React, { useState, useEffect } from "react";
import Board from "./Board";
import ChessCoordinate from "./Coordinate";

import K from './img/wK.png';
import Q from './img/wQ.png';
import B from './img/wB.png';
import N from './img/wN.png';
import R from './img/wR.png';
import P from './img/wP.png';
import k from './img/bK.png';
import q from './img/bQ.png';
import b from './img/bB.png';
import n from './img/bN.png';
import r from './img/bR.png';
import p from './img/bP.png';
import blank from './img/blank.png';

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
	const [activePieces, setActivePieces] = useState({"startPos": null, "endPos": null});
	const [grid, setGrid] = useState(generateBoard("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"));
	const handleClick = function chessCallback(coordinate){
		if (activePieces["startPos"] == null) {
			setActivePieces({"startPos" : coordinate.toString(), "endPos" : null});
			socket.emit("selected", coordinate.toString())
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

	useEffect (() => {
		socket.on("update", (recv) => {
			setGrid(generateBoard(recv));
		});
	});

	return (
			<Board width={BOARD_DIM} height={BOARD_DIM} color_map={chess_styler} pieces={grid} callback={handleClick}></Board>
	)
};

export default ChessBoard;
