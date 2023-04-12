
function ChessCoordinate(row, col) {
    this.row = 8 - row;
    this.col = String.fromCharCode(97+col);
}
ChessCoordinate.prototype.toString = function CoordinateToString() {
    return `${this.col}${this.row}`;
};

