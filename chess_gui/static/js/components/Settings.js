
function Settings({socket}) {

    const handleReset = () => {
        socket.emit('reset');
    };
    const handleUndo = () => {
        socket.emit('undo');
    };

    React.useEffect (() => {
        $("#settingModal").modal("show")
    });
    return (
            <div class="modal fade" id="settingModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="staticBackdropLabel">Choose Your Opponent</h5>
                </div>
                <div class="modal-body text-center">
                <div class="btn-group" role="group" aria-label="Basic example">
                    <form action="/options">
                        <button type="submit" class="btn btn-info" data-bs-dismiss="modal" name="opponent" value="User">GUI Player</button>
                        <button type="submit" class="btn btn-info" data-bs-dismiss="modal" name="opponent" value="Random">Random Player</button>
                        <button type="submit" class="btn btn-info" data-bs-dismiss="modal" name="opponent" value="Minimax" >Minimax Player</button>
                    </form> 


                </div>
                </div>
                </div>
            </div>
            </div>
    )
}