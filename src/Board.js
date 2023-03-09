import ChessCoordinate from "./Coordinate";
import Square from "./Square";

function Board({width, height, color_map, pieces, callback}) {
    const handleClick = function boardCallback(coordinate){
        callback(coordinate)
    }
    const board = [];
    for (let i = 0; i < height; i+=1){
        var row = [];
        for (let j = 0; j < width; j += 1){
            var name = i.toString() + " " + j.toString()
            row.push(<Square name={name} styler={color_map(i,j)} piece={pieces[i][j]} key={j} coordinate={new ChessCoordinate(i, j)} callback={handleClick}></Square>)
        }
        board.push(<div className="row m-0" key={i}>{row}</div>)
    }
    return (
            <div className="col-9 p-0 border border-dark">
                {board}
            </div>
    )
};

export default Board;

