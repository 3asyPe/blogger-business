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