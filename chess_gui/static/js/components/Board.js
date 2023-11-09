
function Board({width, height, color_map, pieces, callback}) {
    const handleClick = function boardCallback(square_data){
        callback(square_data)
    }
    const board = [];
    for (let i = 0; i < height; i+=1){
        var row = [];
        for (let j = 0; j < width; j += 1){
            var name = i.toString() + " " + j.toString()
            row.push(<Square styler={color_map(i,j)} piece={pieces[i][j]} coordinate={new ChessCoordinate(i, j)} callback={handleClick}></Square>)
        }
        board.push(<div className="row m-0" key={i}>{row}</div>)
    }
    return (
            <div className="p-0">
                <div className="border border-dark">
                    {board}
                </div>
            </div>
    )
};


