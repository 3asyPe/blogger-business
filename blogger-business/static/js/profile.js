const url = new URL(window.location.href)
const confirmed = url.searchParams.get("confirmed")

if (confirmed !== null){
    $.alert({
        title: "Email is confirmed!",
        content: "You have changed your email successfully"
    })
}

let defaultProfileData;

function fetchFullData(){
    fetch("/api/profile-data/")
    .then(response => {
        return response.json()
    })
    .then(data => {
        defaultProfileData = JSON.parse(data)
        console.log(defaultProfileData)
        pullFullDataIntoHtml()
    })
}

fetchFullData()

function previewImage(event){
    var reader = new FileReader();
    reader.onload = function() {
        var output = document.querySelector('#upload-image-icon');
        output.src = reader.result;
    }
    reader.readAsDataURL(event.target.files[0]);
    var saveBtn = document.querySelector(".btn-save-change-image")
    saveBtn.classList.remove("d-none")
}

function fetchImageData(){
    fetch("/api/profile-data/image/")
    .then(response => {
        return response.json()
    })
    .then(data => {
        data = JSON.parse(data)
        console.log(data)
        defaultProfileData.image = data.image

        var image = document.querySelector('#upload-image-icon');
        image.src = defaultProfileData.image

        var imageNavbar = document.querySelector("#profile-image-navbar")
        imageNavbar.src = defaultProfileData.image
    })
}

var imageForm = document.querySelector("#image-form")

imageForm.addEventListener('submit', function(ev) {
    ev.preventDefault()

    var oData = new FormData(imageForm)

    var oReq = new XMLHttpRequest()
    oReq.open("POST", "/api/profile-data/image/edit/", true)

    var saveBtn = document.querySelector(".btn-save-change-image")
    
    oReq.onload = function(oEvent) {
        fetchImageData()
        saveBtn.innerHTML = defaultSaveBtnHtml
        saveBtn.classList.add("d-none")
        if (oReq.status == 200) {
        } else {
            $.alert({
                title: 'An error occured',
                content: "Error " + oReq.status + " occurred when trying to edit your profile image. Please try again.",
                type: 'red',
                typeAnimated: true,
                buttons: {
                    tryAgain: {
                        text: 'Try again',
                        btnClass: 'btn-red',
                        action: function(){
                        }
                    },
                }
            })
        }
    };

    defaultSaveBtnHtml = saveBtn.innerHTML
    saveBtn.innerHTML = 'Loading <i class="fas fa-spinner fa-spin"></i>'

    oReq.send(oData)
}, false)

function addEmailActivationMark(){
    emailActivationDiv = document.querySelector(".email-activation")
    newEmail = defaultProfileData.email_activation.email
    expireTimeLeft = defaultProfileData.email_activation.time_left
    emailActivationHtml = '<i class="fas fa-exclamation-circle" data-toggle="tooltip" data-placement="top" title="This is a username field"></i>' +
                            'Less than ' + expireTimeLeft + ' hours to confirm ' + newEmail
    emailActivationDiv.innerHTML = emailActivationHtml
}
