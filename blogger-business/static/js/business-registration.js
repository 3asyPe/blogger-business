var form = document.querySelector("#registration-form");

form.addEventListener('submit', function(ev) {
    ev.preventDefault()
    var oData = new FormData(form)
    oData.append("accountType", "business");

    if(oData.get('image').size === 0){
        $.alert({
            title: 'Image is also required',
            content: "Please fill the image field",
            theme: 'material',
        })
        return
    }

    if(!isValidHttpUrl(oData.get('site'))){
        $.alert({
            title: 'Web-site field is also required',
            content: "Please fill the working url to your web-site",
            theme: 'material',
        })
        return
    }

    if(!isValidInstagramLinkOrUsername(oData.get('instagram'))){
        $.alert({
            title: 'Instagram field is also required',
            content: "Please fill the working url or username of your instagram account",
            theme: 'material',
        })
        return
    }

    if(!isValidHttpUrl(oData.get('facebook'))){
        $.alert({
            title: 'Facebook field is also required',
            content: "Please fill the working url to your facebook account",
            theme: 'material',
        })
        return
    }

    var oReq = new XMLHttpRequest()
    oReq.open("POST", "/api/registration/complete", true)
    oReq.onload = function(oEvent) {
        saveBtn.innerHTML = defaultSaveBtnHtml
        if (oReq.status == 201) {
            $.confirm({
                title: 'You have created your account',
                content: "We sent you new password. Please check your email.",
                type: 'blue',
                typeAnimated: true,
                buttons: {
                    ok: {
                        text: 'OK',
                        btnClass: 'btn-blue',
                        action: function () {
                            window.location.href = "/login/"
                        }
                    }
                }
            })
        } else {
            $.alert({
                title: 'An error occured',
                content: "Error " + oReq.status + " occurred when trying to register your account. Please try again.",
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

    saveBtn = document.querySelector("#save-btn")
    defaultSaveBtnHtml = saveBtn.innerHTML
    saveBtn.innerHTML = 'Loading <i class="fas fa-spinner fa-spin"></i>'

    oReq.send(oData)
}, false)

function previewImage(event){
    var reader = new FileReader();
    reader.onload = function() {
        var output = document.querySelector('#upload-image-icon');
        output.src = reader.result;
    }
    reader.readAsDataURL(event.target.files[0]);
}

function isValidHttpUrl(string) {
    let url;
  
    try {
      url = new URL(string);
    } catch (_) {
      return false;  
    }
  
    return url.protocol === "http:" || url.protocol === "https:";
}

function isValidInstagramLinkOrUsername(string){
    if(isValidHttpUrl(string)){
        var url = string + "?__a=1"
    }
    else{
        var url = "https://www.instagram.com/" + string + "/?__a=1" 
    }
    console.log(url)
    try{
        var request = new XMLHttpRequest()
        request.open("GET", url, false)
        request.send()
        if (request.responseText === "{}"){
            return false
        } else {
            return true
        }
    } catch (_) {
        return false
    }
}