var form = document.querySelector("#registration-form");

form.addEventListener('submit', async function(ev) {
    ev.preventDefault()
    saveBtn = document.querySelector("#save-btn")
    defaultSaveBtnHtml = saveBtn.innerHTML
    saveBtn.innerHTML = 'Loading <i class="fas fa-spinner fa-spin"></i>'

    var oData = new FormData(form)

    if(oData.get('image').size === 0){
        $.alert({
            title: 'Image is also required',
            content: "Please fill the image field",
            theme: 'material',
        })
        saveBtn.innerHTML = defaultSaveBtnHtml
        return
    }

    if(!isValidHttpUrl(oData.get('site'))){
        $.alert({
            title: 'Web-site field is also required',
            content: "Please fill the working url to your web-site",
            theme: 'material',
        })
        saveBtn.innerHTML = defaultSaveBtnHtml
        return
    }

    if(!isValidInstagramLinkOrUsername(oData.get('instagram'))){
        $.alert({
            title: 'Instagram field is also required',
            content: "Please fill the working url or username of your instagram account",
            theme: 'material',
        })
        saveBtn.innerHTML = defaultSaveBtnHtml
        return
    }

    if(!isValidHttpUrl(oData.get('facebook'))){
        $.alert({
            title: 'Facebook field is also required',
            content: "Please fill the working url to your facebook account",
            theme: 'material',
        })
        saveBtn.innerHTML = defaultSaveBtnHtml
        return
    }

    exists = await check_exists()
    if (exists){
        saveBtn.innerHTML = defaultSaveBtnHtml
        return false
    }

    oData.append("accountType", "business");

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

    oReq.send(oData)
}, false)

function getUsernameField(){
    return document.querySelector("#business_name")
}

document.querySelector("#business_name").onfocus = function(e){
    $('[data-toggle="username-popover"]').popover("hide")
    if (e.target.classList.contains("invalid-field")){
        e.target.classList.remove("invalid-field")
    }
}
