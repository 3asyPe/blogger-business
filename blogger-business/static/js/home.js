function login(event){
    window.location.href='/login'
}

function blogger_login(event){
    window.location.href='/registration?type=bl'
}


function business_login(event){
    window.location.href='/registration?type=bu'
}

function downloadAndroidApp(){
    $.alert({
        title: "Sorry",
        content: "We don't have an android app yet.",
        backgroundDismiss: true,
    })
}

function downloadIOSApp(){
    $.alert({
        title: "Sorry",
        content: "We don't have an IOS app yet.",
        backgroundDismiss: true,
    })
}
