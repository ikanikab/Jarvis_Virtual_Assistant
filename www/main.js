$(document).ready(function () {
    $('.text').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "bounceIn",
        },
        out: {
            effect: "bounceOut",
        }
    })

    // siri wave configuration
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 800,
        height: 200,
        autostart: true,
        style: 'ios9',
        amplitude: 1,
        speed: 0.3
    });

    // Siri message animation
    $('.siri-message').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "fadeInUp",
            sync: true,
        },
        out: {
            effect: "fadeOutUp",
            sync: true,
        },

    });

    // mic button click event

    $("#MicBtn").click(function () {
        eel.playAssistantSound();
        $("#Oval").attr("hidden", true);
        $("#SiriWave").removeAttr("hidden");
        eel.allCommands()();
    });

    function doc_keyUp(e) {
        // this would test for whichever key is 40 (down arrow) and the ctrl key at the same time

        if (e.key === 'j' && e.metaKey) {
            eel.playAssistantSound();
            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands()();
        }
    }
    document.addEventListener('keyup', doc_keyUp, false);

    function PlayAssistant(message) {
        if (message != "") {
            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands(message);
            $("#chatbox").val("");
            $("#MicBtn").attr("hidden", false);
            $("#SendBtn").attr("hidden", true);
        }
    }

    function ShowHideButton(message) {
        if (message.length == 0) {
            $("#MicBtn").attr("hidden", false);
            $("#SendBtn").attr("hidden", true);
        }
        else {
            $("#MicBtn").attr("hidden", true);
            $("#SendBtn").attr("hidden", false);
        }
    }
    // Listen for user typing
    $("#chatbox").keyup(function () {
        let message = $("#chatbox").val();
        ShowHideButton(message);
    });

    // On send button click
    $("#SendBtn").click(function () {
        let message = $("#chatbox").val();
        PlayAssistant(message);
    })

    //Attaches an event listener to the input field 
    $("#chatbox").keydown(function (e) {
        let key = e.which;
        // 13 is the ASII code for enter key
        if (key == 13) {
            let message = $("#chatbox").val()
            PlayAssistant(message)
        }
    })

});

eel.displaySysCommand()();
eel.displayWebCommand()();

// Display System Command Method
eel.expose(displaySysCommand)
function displaySysCommand(array) {

    let data = JSON.parse(array);
    console.log(data)

    let placeholder = document.querySelector("#TableData");
    let out = "";
    let index = 0
    for (let i = 0; i < data.length; i++) {
        index++
        out += `
                    <tr>
                        <td class="text-light"> ${index} </td>
                        <td class="text-light"> ${data[i][1]} </td>
                        <td class="text-light"> ${data[i][2]} </td>
                        <td class="text-light"> <button id="${data[i][0]}" onClick="SysDeleteID(this.id)" class="btn btn-sm btn-glow-red">Delete</button></td>
                        
                    </tr>
            `;

        // console.log(data[i][0])
        // console.log(data[i][1])


    }

    placeholder.innerHTML = out;

}

// Add System Command Button
$("#SysCommandAddBtn").click(function () {

    let key = $("#SysCommandKey").val();
    let value = $("#SysCommandValue").val();

    if (key.length > 0 && value.length) {
        eel.addSysCommand(key, value)

        swal({
            title: "Updated Successfully",
            icon: "success",
        });
        eel.displaySysCommand()();
        $("#SysCommandKey").val("");
        $("#SysCommandValue").val("");


    }
    else {
        const toastLiveExample = document.getElementById('liveToast')
        const toast = new bootstrap.Toast(toastLiveExample)

        $("#ToastMessage").text("All Fields Medatory");

        toast.show()
    }

});

// Display Web Commands Table
eel.expose(displayWebCommand)
function displayWebCommand(array) {

    let data = JSON.parse(array);
    console.log(data)

    let placeholder = document.querySelector("#WebTableData");
    let out = "";
    let index = 0
    for (let i = 0; i < data.length; i++) {
        index++
        out += `
                    <tr>
                        <td class="text-light"> ${index} </td>
                        <td class="text-light"> ${data[i][1]} </td>
                        <td class="text-light"> ${data[i][2]} </td>
                        <td class="text-light"> <button id="${data[i][0]}" onClick="WebDeleteID(this.id)" class="btn btn-sm btn-glow-red">Delete</button></td>
                        
                    </tr>
            `;

        // console.log(data[i][0])
        // console.log(data[i][1])


    }

    placeholder.innerHTML = out;

}


// Add Web Commands

$("#WebCommandAddBtn").click(function () {

    let key = $("#WebCommandKey").val();
    let value = $("#WebCommandValue").val();

    if (key.length > 0 && value.length) {
        eel.addWebCommand(key, value)

        swal({
            title: "Updated Successfully",
            icon: "success",
        });
        eel.displayWebCommand()();
        $("#WebCommandKey").val("");
        $("#WebCommandValue").val("");


    }
    else {
        const toastLiveExample = document.getElementById('liveToast')
        const toast = new bootstrap.Toast(toastLiveExample)

        $("#ToastMessage").text("All Fields Medatory");

        toast.show()
    }

});

function SysDeleteID(clicked_id) {


    // console.log(clicked_id);
    eel.deleteSysCommand(clicked_id)
    eel.displaySysCommand()();
}

function WebDeleteID(clicked_id) {


    // console.log(clicked_id);
    eel.deleteWebCommand(clicked_id)
    eel.displayWebCommand()();


}
