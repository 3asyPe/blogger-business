var form = document.querySelector("#registration-form");

form.addEventListener('submit', function(ev) {
    var oData = new FormData(form)
    oData.append("accountType", "business");

    var oReq = new XMLHttpRequest()
    oReq.open("POST", "/api/registration/complete", true)
    oReq.onload = function(oEvent) {
        if (oReq.status == 201) {
            console.log(oReq.response)
        } else {
            console.log("Error " + oReq.status + " occurred when trying to register your account.")
        }
    };

    oReq.send(oData)
    ev.preventDefault()
}, false)

function previewImage(event){
    var reader = new FileReader();
    reader.onload = function() {
        var output = document.querySelector('#upload-image-icon');
        output.src = reader.result;
    }
    reader.readAsDataURL(event.target.files[0]);
}
