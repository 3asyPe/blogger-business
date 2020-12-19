const form = document.querySelector("#reactivation-form")
alertDiv = document.querySelector(".custom-alert")

form.addEventListener("submit", function(event){
    event.preventDefault()
    var oData = new FormData(form)
    var oReq = new XMLHttpRequest()
    oReq.open("POST", "/api/email/reactivate/", true)

    reactivateBtn = document.querySelector(".reactivate-btn")
    defaultSaveBtnHtml = reactivateBtn.innerHTML
    reactivateBtn.innerHTML = 'Loading <i class="fas fa-spinner fa-spin"></i>'

    oReq.onload = function(oEvent) {
        reactivateBtn.innerHTML = defaultSaveBtnHtml

        if (oReq.status == 200) {
            console.log(JSON.parse(oReq.response))
            window.location.href = "/login?activated"
        } else if(oReq.status == 404) {
            newAlertHtml = '<div class="alert alert-danger" role="alert">' +
                                'Account with this email doesn\'t exist' +
                            '</div>'
            alertDiv.innerHTML = newAlertHtml
        } else if(oReq.status == 409){
            newAlertHtml = '<div class="alert alert-danger" role="alert">' +
                                'This email is already activated' +
                            '</div>'
            alertDiv.innerHTML = newAlertHtml
        }

    };
    oReq.send(oData)
})
