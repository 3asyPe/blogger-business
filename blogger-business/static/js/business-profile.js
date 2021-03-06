function fetchBusinessInfoData(){
    fetch("/api/business-profile-data/info")
    .then(response => {
        return response.json()
    })
    .then(data => {
        data = JSON.parse(data)
        console.log(data)

        defaultProfileData.business_name = data.business_name
        defaultProfileData.business_owner_name = data.business_owner_name
        defaultProfileData.location.country = data.location.country
        defaultProfileData.location.city = data.location.city

        pullBusinessInfoDataIntoHtml()
    })
}

function fetchBusinessContactData(){
    fetch("/api/business-profile-data/contact")
    .then(response => {
        return response.json()
    })
    .then(data => {
        data = JSON.parse(data)
        console.log(data)

        defaultProfileData.site = data.site
        defaultProfileData.facebook = data.facebook
        defaultProfileData.instagram = data.instagram
        defaultProfileData.email = data.email
        defaultProfileData.email_activation = data.email_activation
        defaultProfileData.phone = data.phone

        pullBusinessContactDataIntoHtml()
    })
}

function pullFullDataIntoHtml(){
    var image = document.querySelector("#upload-image-icon")
    image.src = defaultProfileData.image

    pullBusinessInfoDataIntoHtml()
    
    pullBusinessContactDataIntoHtml()
}

function pullBusinessInfoDataIntoHtml(){
    business_name = document.querySelector("#business_name")
    business_name.innerHTML = defaultProfileData.business_name

    business_owner_name = document.querySelector("#business_owner_name")
    business_owner_name.innerHTML = defaultProfileData.business_owner_name

    country = document.querySelector("#country")
    country.innerHTML = defaultProfileData.location.country

    city = document.querySelector("#city")
    city.innerHTML = defaultProfileData.location.city
}

function pullBusinessContactDataIntoHtml(){
    site = document.querySelector("#site")
    site.innerHTML = defaultProfileData.site

    facebook = document.querySelector("#facebook")
    facebook.innerHTML = defaultProfileData.facebook

    instagram = document.querySelector("#instagram")
    instagram.innerHTML = defaultProfileData.instagram

    email = document.querySelector("#email")
    email.innerHTML = defaultProfileData.email

    phone = document.querySelector("#phone")
    phone.innerHTML = defaultProfileData.phone

    if (defaultProfileData.email_activation){
        addEmailActivationMark()
    } else {
        emailActivationDiv = document.querySelector(".email-activation")
        emailActivationDiv.innerHTML = ''
    }
}

function editBusinessInfo(){
    var business_name = defaultProfileData.business_name
    var business_owner_name = defaultProfileData.business_owner_name
    var country = defaultProfileData.location.country
    var city = defaultProfileData.location.city
    
    $.confirm({
        title: 'Edit personal info',
        columnClass: "medium",
        content: '' +
        '<form action="" method="POST" class="formName" id="editInfoForm">' +
            '<div class="form-group">' +
                '<label for="edit-business-name">' +
                    '<i class="fas fa-exclamation-circle" data-toggle="tooltip" data-placement="top" title="This is a username field"></i>' +
                    'Business name:' +
                '</label>' +
                '<input type="text" id="edit-business-name" name="business_name" value="' + business_name + '" class="business_name form-control" required data-toggle="username-popover" data-trigger="focus" data-placement="top"  data-content="Username is already taken" />' +
            '</div>' +
            '<div class="form-group">' +
                '<label for="edit-business-owner-name">Owner name:</label>' +
                '<input type="text" id="edit-business-owner-name" name="business_owner_name" value="' + business_owner_name + '" class="business_owner_name form-control" required />' +
            '</div>' +
            '<div class="form-group">' +
                '<label for="edit-country">Your country:</label>' +
                '<input type="text" id="edit-country" name="country" value="' + country + '" class="country form-control" required />' +
            '</div>' +
            '<div class="form-group">' +
                '<label for="edit-city">Your city:</label>' +
                '<input type="text" id="edit-city" name="city" value="' + city + '" class="city form-control" required />' +
            '</div>' +
        '</form>',
        buttons: {
            formSubmit: {
                text: 'Submit',
                btnClass: 'btn-blue',
                action: function () {
                    send(this)
                    async function send(that){
                        var editInfoForm = document.querySelector("#editInfoForm")

                        var oData = new FormData(editInfoForm)
                        
                        var oReq = new XMLHttpRequest()
                        oReq.open("POST", "/api/business-profile-data/info/edit/", true)
                        oReq.setRequestHeader('X-CSRFToken', csrftoken)
                        
                        username = editInfoForm.elements.namedItem("business_name").value
                        if (defaultProfileData.business_name != username){
                            usernameExists = await username_check(username)
                            if (usernameExists){
                                $('[data-toggle="username-popover"]').popover("show")
                                return false
                            }
                        }

                        oReq.onload = function(oEvent) {
                            fetchBusinessInfoData()
                            if (oReq.status == 200) {
                            } else {
                                $.alert({
                                    title: 'An error occured',
                                    content: "Error " + oReq.status + " occurred when trying to edit your business info. Please try again.",
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
                        that.close()
                    }
                    return false
                }
            },
            cancel: function () {
                //close
                $('[data-toggle="username-popover"]').popover("hide")
            },
        },
        onContentReady: function () {
            $('[data-toggle="tooltip"]').tooltip()

            document.querySelector("#edit-business-name").onfocus = function(e){
                $('[data-toggle="username-popover"]').popover("hide")
            }
        }
    })
}

function editBusinessContact(){
    var site = defaultProfileData.site
    var facebook = defaultProfileData.facebook
    var instagram = defaultProfileData.instagram
    var email = defaultProfileData.email
    var phone = defaultProfileData.phone
    
    $.confirm({
        title: 'Edit personal info',
        columnClass: "medium",
        content: '' +
        '<form action="" method="POST" class="formName" id="editContactForm">' +
            '<div class="form-group">' +
                '<label for="edit-site">Your Web-site:</label>' +
                '<input type="text" id="edit-site" name="site" value="' + site + '" class="stie form-control" required />' +
            '</div>' +
            '<div class="form-group">' +
                '<label for="edit-facebook">Your Facebook:</label>' +
                '<input type="text" id="edit-facebook" name="facebook" value="' + facebook + '" class="facebook form-control" required />' +
            '</div>' +
            '<div class="form-group">' +
                '<label for="edit-instagram">Your Instagram:</label>' +
                '<input type="text" id="edit-instagram" name="instagram" value="' + instagram + '" class="instagram form-control" required />' +
            '</div>' +
            '<div class="form-group">' +
                '<label for="edit-phone">Your phone:</label>' +
                '<input type="text" id="edit-phone" name="phone" value="' + phone + '" class="phone form-control" required />' +
            '</div>' +
            '<div class="form-group">' +
                '<label for="edit-email">' +
                    '<i class="fas fa-exclamation-circle" data-toggle="tooltip" data-placement="top" title="You will need to confirm the new email address"></i>' +    
                    'Your email:' +
                '</label>' +
                '<input type="text" id="edit-email" name="email" value="' + email + '" class="email form-control" required data-toggle="email-popover" data-trigger="focus" data-placement="top" data-content="Email is already taken" />' +
            '</div>' +
        '</form>',
        buttons: {
            formSubmit: {
                text: 'Submit',
                btnClass: 'btn-blue',
                action: function () {
                    send(this)
                    async function send(that){
                        var editContactForm = document.querySelector("#editContactForm")

                        var oData = new FormData(editContactForm)

                        site = oData.get('site')
                        if (defaultProfileData.site != site){
                            if(!isValidHttpUrl(site)){
                                $.alert({
                                    title: 'Web-site field is also required',
                                    content: "Please fill the working url to your web-site",
                                    theme: 'material',
                                })
                                return false
                            }
                        }
                    
                        instagram = oData.get('instagram')
                        if (defaultProfileData.instagram != instagram){
                            if(!isValidInstagramLinkOrUsername()){
                                $.alert({
                                    title: 'Instagram field is also required',
                                    content: "Please fill the working url or username of your instagram account",
                                    theme: 'material',
                                })
                                return false
                            }
                        }
                        
                        facebook = oData.get('facebook')
                        if (defaultProfileData.facebook != facebook){
                            if(!isValidHttpUrl()){
                                $.alert({
                                    title: 'Facebook field is also required',
                                    content: "Please fill the working url to your facebook account",
                                    theme: 'material',
                                })
                                return false
                            }
                        }

                        email = editContactForm.elements.namedItem("email").value
                        if (defaultProfileData.email != email){
                            emailExists = await email_check(email)
                            if (emailExists){
                                $('[data-toggle="email-popover"]').popover("show")
                                return false
                            }
                        }
                        
                        var oReq = new XMLHttpRequest()
                        oReq.open("POST", "/api/business-profile-data/contact/edit/", true)
                        oReq.setRequestHeader('X-CSRFToken', csrftoken)
                        
                        oReq.onload = function(oEvent) {
                            fetchBusinessContactData()
                            if (oReq.status == 200) {
                            } else {
                                $.alert({
                                    title: 'An error occured',
                                    content: "Error " + oReq.status + " occurred when trying to edit your business contact. Please try again.",
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
                        that.close()
                    }
                    return false
                }
            },
            cancel: function () {
                $('[data-toggle="email-popover"]').popover("hide")
            },
        },
        onContentReady: function () {
            $('[data-toggle="tooltip"]').tooltip()

            document.querySelector("#edit-email").onfocus = function(e){
                $('[data-toggle="email-popover"]').popover("hide")
            }
        }
    })
}
