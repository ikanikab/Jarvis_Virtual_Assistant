$(document).ready(function () {
    // Display Speak Message
    eel.expose(DisplayMessage)
    function DisplayMessage(message) {
        $(".siri-message .texts li").text(message);
        $('.siri-message').textillate('start');
    }

    //Display hood
    eel.expose(ShowHood)
    function ShowHood() {
        $("#Oval").attr("hidden", false);
        $("#SiriWave").attr("hidden", true);
    }

    eel.expose(senderText)
    function senderText(message){
        var chatBox = document.getElementById("chat-canvas-body");
        if (message.trim()!==""){
            chatBox.innerHTML += `<div class="row justify-content-end mb-2"> 
            <div class="width-size">
            <div class="sender_message"> ${message} </div>
            </div>
            </div>`;

            //Scroll to the bottom of the chatbox
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }

    eel.expose(receiverText)
    function receiverText(message){
        var chatBox = document.getElementById("chat-canvas-body");
        if (message.trim()!==""){
            chatBox.innerHTML += `<div class="row justify-content-start mb-2"> 
            <div class="width-size">
            <div class="receiver_message"> ${message} </div>
            </div>
            </div>`;

            //Scroll to the bottom of the chatbox
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }
});
