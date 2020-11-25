const form = document.querySelector("#login-form")
const next = new URL(window.location.href).searchParams.get("next")

form.addEventListener("submit", function(event){
    event.preventDefault()
    var oData = new FormData(form)
    var oReq = new XMLHttpRequest()
    oReq.open("POST", "/api/login/complete", true)
    oReq.onload = function(oEvent) {
        if (oReq.status == 200) {
            console.log(JSON.parse(oReq.response))
            window.location.href = next !== null ? next : JSON.parse(oReq.response).next_url
        } else if(oReq.status == 401) {
            alertDiv = document.querySelector(".alert-inner")
            newAlertHtml = '<div class="alert alert-danger" role="alert">' +
                                'Username or password is wrong or your account isn\'t activated (please check your email)' +
                            '</div>'
            alertDiv.innerHTML = newAlertHtml
        }
    };
    oReq.send(oData)
})