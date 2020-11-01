var form = document.querySelector("#registration-form");

form.addEventListener('submit', function(ev) {
    ev.preventDefault()
    var oData = new FormData(form)
    oData.append("accountType", "business");

    if(oData.get('image').size === 0){
        alert("Image field is also required")
        return
    }

    if(!isValidHttpUrl(oData.get('site'))){
        alert("Site field must contain working url")
        return
    }

    if(!isValidInstagramLinkOrUsername(oData.get('instagram'))){
        alert("Instagram field must contain available instagram link or username")
        return
    }

    if(!isValidHttpUrl(oData.get('facebook'))){
        alert("Facebook field must contain working url")
        return
    }

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