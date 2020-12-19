alertDiv = document.querySelector(".custom-alert")
const url = new URL(window.location.href)
const activated = url.searchParams.get("activated")

if (activated !== null){
    newAlertHtml = '<div class="alert alert-success text-center" role="alert">' +
                        'You have activated your new account. Please login' +
                    '</div>'
    alertDiv.innerHTML = newAlertHtml
}

const form = document.querySelector("#login-form")
const next = url.searchParams.get("next")

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
            newAlertHtml = '<div class="alert alert-danger" role="alert">' +
                                'Username or password is wrong or your account isn\'t activated (please check your email)' +
                            '</div>'
            alertDiv.innerHTML = newAlertHtml
        }
    };
    oReq.send(oData)
})