
function Square(props) {
    const onClick = (e) => props.callback(props.coordinate)
    const divStyle = {
        padding : "2\%",
    };
    for (let key in props.styler) {
        divStyle[key] = props.styler[key];
    }

    return (
        <div className="col" style={divStyle} onClick={onClick}>
            <img src={props.piece} style={{maxWidth:"100\%", maxHeight:"100\%"}} alt=""/>
        </div>
    )
};

