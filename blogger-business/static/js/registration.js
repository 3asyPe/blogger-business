$('[data-toggle="tooltip"]').tooltip()

async function check_exists(){
    async function username_check(username){
        let response = await fetch('/api/username/check/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8',
                'X-CSRFToken': csrf_token,
            },
            body: JSON.stringify({
                "username": username
            })
        });
          
        let result = await response.json().then(response => {
            return response.exists
        });
        return await result
    }

    async function email_check(email){
        let response = await fetch('/api/email/check/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8',
                'X-CSRFToken': csrf_token,
            },
            body: JSON.stringify({
                "email": email
            })
        });
          
        let result = await response.json().then(response => {
            return response.exists
        });
        return await result
    }

    username_exists = await username_check(getUsernameField().value)
    email_exists = await email_check(form.elements.namedItem("email").value)

    result = false
    if (username_exists){
        addCustomValidityUsername()
        result = true
    }

    if (email_exists){
        addCustomValidityEmail()
        result = true
    }

    return result
}

function addCustomValidityUsername(){
    usernameField = getUsernameField()
    if (!usernameField.classList.contains("invalid-field")){
        usernameField.classList.add("invalid-field")
        $('[data-toggle="username-popover"]').popover("show")
    }
    usernameField.scrollIntoView({
        behavior: "smooth",
        block: "center",
    })
}

function addCustomValidityEmail(){
    emailField = document.querySelector("#email")
    if (!emailField.classList.contains("invalid-field")){
        emailField.classList.add("invalid-field")
        $('[data-toggle="email-popover"]').popover("show")
    }
    emailField.scrollIntoView({
        behavior: "smooth",
        block: "center",
    })
}

document.querySelector("#email").onfocus = function(e){
    $('[data-toggle="email-popover"]').popover("hide")
    if (e.target.classList.contains("invalid-field")){
        e.target.classList.remove("invalid-field")
    }
}

function previewImage(event){
    var reader = new FileReader();
    reader.onload = function() {
        showImage(reader.result)
    }
    reader.readAsDataURL(event.target.files[0]);
}

function showImage(source){
    var output = $('.image')
    output.attr("src", source)
    output.show()
    var imagePlaceholder = $('.image-placeholder')
    imagePlaceholder.hide()
}