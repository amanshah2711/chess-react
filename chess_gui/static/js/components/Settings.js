
function Settings({socket}) {

    React.useEffect (() => {
        $("#settingModal").modal("hide");
		const reveal = () =>{
            $("#settingModal").modal("show");
		};
        socket.on("show_options", reveal)
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
                        <button type="submit" class="btn btn-info" data-bs-dismiss="modal" name="opponent" value="User">Human</button>
                        &nbsp;&nbsp;&nbsp; 
                        <button type="submit" class="btn btn-info" data-bs-dismiss="modal" name="opponent" value="Random">Random AI</button>
                        &nbsp;&nbsp;&nbsp; 
                        <button type="submit" class="btn btn-info" data-bs-dismiss="modal" name="opponent" value="Minimax" >Minimax AI</button>
                    </form> 
                </div>
                </div>
                </div>
            </div>
            </div>
    )
}