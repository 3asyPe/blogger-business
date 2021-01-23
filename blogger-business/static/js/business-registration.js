var form = document.querySelector("#registration-form");

form.addEventListener('submit', async function(ev) {
    ev.preventDefault()
    saveBtn = document.querySelector("#save-btn")
    defaultSaveBtnHtml = saveBtn.innerHTML
    saveBtn.innerHTML = 'Loading <i class="fas fa-spinner fa-spin"></i>'

    var oData = new FormData(form)

    if(oData.get('image').size === 0){
        imageDiv = document.querySelector(".label-image")
        if (!imageDiv.classList.contains("invalid-field")){
            imageDiv.classList.add("invalid-field")
        }
        imageDiv.scrollIntoView({
            behavior: "smooth",
            block: "center",
        })
        saveBtn.innerHTML = defaultSaveBtnHtml
        return
    }

    const re = /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
    let email = document.querySelector("#email")
    if (!re.test(email.value)){
        if (!email.classList.contains("invalid-field")){
            email.classList.add("invalid-field")
        }
        email.scrollIntoView({
            behavior: "smooth",
            block: "center",
        })
        console.log("email")
        saveBtn.innerHTML = defaultSaveBtnHtml
        return
    }

    if(!isValidHttpUrl(oData.get('site'))){
        let site = document.querySelector("#site")
        if (!site.classList.contains("invalid-field")){
            site.classList.add("invalid-field")
            $('[data-toggle="site-popover"]').popover("show")
        }
        site.scrollIntoView({
            behavior: "smooth",
            block: "center",
        })
        saveBtn.innerHTML = defaultSaveBtnHtml
        return
    }

    if(!isValidInstagramLinkOrUsername(oData.get('instagram'))){
        let instagram = document.querySelector("#instagram")
        if (!instagram.classList.contains("invalid-field")){
            instagram.classList.add("invalid-field")
            $('[data-toggle="instagram-popover"]').popover("show")
        }
        instagram.scrollIntoView({
            behavior: "smooth",
            block: "center",
        })
        console.log("insta")
        saveBtn.innerHTML = defaultSaveBtnHtml
        return
    }

    if(!isValidHttpUrl(oData.get('facebook'))){
        let facebook = document.querySelector("#facebook")
        if (!facebook.classList.contains("invalid-field")){
            facebook.classList.add("invalid-field")
            $('[data-toggle="facebook-popover"]').popover("show")
        }
        facebook.scrollIntoView({
            behavior: "smooth",
            block: "center",
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

var elements = $("input[type=text]");
elements.each(function(index){
    $(this).on("invalid", function(e){
        e.preventDefault();
        if (!e.target.classList.contains("invalid-field")){
            e.target.classList.add("invalid-field")
        }
        $(this).get(0).scrollIntoView({
            behavior: "smooth",
            block: "center",
        })
    })
    $(this).on("focus", function(e) {
        if (e.target.classList.contains("invalid-field")){
            e.target.classList.remove("invalid-field")
        }
    });
})

document.querySelector("#business_name").onfocus = function(e){
    $('[data-toggle="username-popover"]').popover("hide")
    if (e.target.classList.contains("invalid-field")){
        e.target.classList.remove("invalid-field")
    }
}

document.querySelector("#site").onfocus = function(e){
    $('[data-toggle="site-popover"]').popover("hide")
    if (e.target.classList.contains("invalid-field")){
        e.target.classList.remove("invalid-field")
    }
}

document.querySelector("#instagram").onfocus = function(e){
    $('[data-toggle="instagram-popover"]').popover("hide")
    if (e.target.classList.contains("invalid-field")){
        e.target.classList.remove("invalid-field")
    }
}

document.querySelector("#facebook").onfocus = function(e){
    $('[data-toggle="facebook-popover"]').popover("hide")
    if (e.target.classList.contains("invalid-field")){
        e.target.classList.remove("invalid-field")
    }
}
