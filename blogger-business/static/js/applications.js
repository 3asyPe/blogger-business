function fetchOffers(){
    fetch("/api/offers-for-applications/fetch/")
    .then(response => {
        return response.json()
    })
    .then(data => {
        data = JSON.parse(data)
        offersContainer = document.querySelector(".offers")
        if (data !== {}){
            console.log(data)
            for (let offer of data){
                console.log(offer)
                offerHtml = createOfferDiv(offer)
                offersContainer.innerHTML += offerHtml
                fetchApplicationsForOffer(offer)
            }
        }
    })
}

fetchOffers()

function fetchApplicationsForOffer(offer){
    fetch("/api/applications/fetch/" + offer.id + "/")
    .then(response => {
        return response.json()
    })
    .then(data => {
        data = JSON.parse(data)
        applicationsInner = document.querySelector("#applications-inner-" + offer.id)
        if (data.length != 0){
            console.log(data)
            for (let application of data){
                console.log(application)
                applicationHtml = createApplicationDiv(application)
                applicationsInner.innerHTML += applicationHtml
            }

            for (let application of data){
                applicationHtml = document.querySelector("#application-" + application.id)
                applicationHtml.addEventListener("click", function(){
                    openBloggerProfileModal(application)
                })
            }
        } else {
            checkApplicationsInner(applicationsInner)
        }
    })
}
        
function createOfferDiv(data){
    offer = '<div class="offer" id="offer-' + data.id + '">' +
                '<div class="offer-header">' +
                    '<div class="offer-title">' +
                        data.title +
                    '</div>' +
                '</div>' +
                '<div class="applications-inner" id="applications-inner-' + data.id + '">' +
                '</div>' +
            '</div>'
    return offer
}

function createApplicationDiv(data){
    application = '<div class="application-shell" id="application-' + data.id + '">' +
                    '<div class="application">' +
                        '<div class="stretcher"></div>' +
                        '<div class="application-inner">' +
                            '<div class="application-header">' +
                                '<div class="application-image-div">' +
                                    '<div class="stretcher"></div>' +
                                    '<img src="' + data.blogger.image + '" class="image modal-profile-image">' +
                                '</div> ' +
                                '<div class="application-header-text">' +
                                    '<div class="application-name">' + data.blogger.blog_name + '</div>' +
                                    '<div class="application-links">' +
                                        '<a class="application-link" href="#">' +
                                            '<svg class="application-link-icon">' +
                                                '<use xlink:href="#instagram"></use>' +
                                            '</svg>' +
                                        '</a>' +
                                        '<a class="application-link" href="#">' +
                                            '<svg class="application-link-icon">' +
                                                '<use xlink:href="#youtube"></use>' +
                                            '</svg>' +
                                        '</a>' +
                                    '</div>' +
                                '</div>' +
                            '</div>' +
                            '<div class="application-statistics">' +
                                '<div class="application-statistics-title">' +
                                    '<svg class="application-statistics-title-icon">' +
                                        '<use xlink:href="#instagram"></use>' +
                                    '</svg>' +
                                    '<div class="application-statistics-title-text">Statistics</div>' +
                                '</div>' +
                                '<div class="statistics-inner">' +
                                    '<div class="statistics-block">' +
                                        '<div class="statistics-title">Followers:</div>' +
                                        '<div class="statistics-number">100k</div>' +
                                    '</div>' +
                                    '<div class="statistics-block">' +
                                        '<div class="statistics-title">Comments:</div>' +
                                        '<div class="statistics-number">1.8k</div>' +
                                    '</div>' +
                                    '<div class="statistics-block">' +
                                        '<div class="statistics-title">Likes:</div>' +
                                        '<div class="statistics-number">257k</div>' +
                                    '</div>' +
                                    '<div class="statistics-block">' +
                                        '<div class="statistics-title">Frequency:</div>' +
                                        '<div class="statistics-number"></div>' +
                                    '</div>' +
                                '</div>' +
                            '</div>' +
                        '</div>' +
                    '</div>' +
                '</div>' 
    return application
}

function openBloggerProfileModal(application){
    languagesHtml = ""
    for (let language of application.blogger.languages){
        languagesHtml += '<div class="block-item">' + language.language + '</div>'
    }

    specializationsHtml = ""
    for (let specialization of application.blogger.specializations){
        specializationsHtml += '<div class="block-item">' + specialization.specialization + '</div>'
    }

    $.confirm({
        title: application.blogger.blog_name,
        closeIcon: true,
        columnClass: "col-9",
        backgroundDismiss: true,
        draggable: false,
        theme: 'material',
        content: '' +
            '<div class="profile-container-inner">' +
                '<div class="profile-top-part">' +
                    '<div class="modal-profile-image-div">' +
                        '<div class="stretcher"></div>' +
                        '<img src="' + application.blogger.image + '" id="modal-profile-image" class="image img-fluid">' +
                    '</div>' +
                    '<div class="profile-block">' +
                        '<div class="profile-block-item">' +
                            '<div class="block-item-title">Location:</div>' +
                            '<div class="block-item" id="location">' +
                                '<div class="location-item" id="country">' + application.blogger.location.country +'</div>' +
                                '<span>,&nbsp</span>' +
                                '<div class="location-item" id="city">' + application.blogger.location.city + '</div>' +
                            '</div>' +
                        '</div>' +
                        '<div class="profile-block-item">' +
                            '<div class="block-item-title">Birthday:</div>' +
                            '<div class="block-item" id="birthday">' + application.blogger.birthday + '</div>' +
                        '</div>' +
                        '<div class="profile-block-item">' +
                            '<div class="block-item-title">Languages:</div>' +
                            '<div class="block-items" id="languages">' +
                                languagesHtml +
                            '</div>' +
                        '</div>' +
                        '<div class="profile-block-item">' +
                            '<div class="block-item-title">Specializations:</div>' +
                            '<div class="block-items" id="specializations">' +
                                specializationsHtml +
                            '</div>' +
                        '</div>' +
                        '<div class="profile-block-item">' +
                            '<div class="block-item-title">Phone:</div>' +
                            '<div class="block-item" id="phone">' + application.blogger.phone + '</div>' +
                        '</div>' +
                        '<div class="profile-block-item">' +
                            '<div class="block-item-title">Email:</div>' +
                            '<div class="email" id="email">' + application.blogger.email + '</div>' +
                        '</div>' +
                    '</div>' +
                '</div>' +
                '<div class="bottom-part">' +
                    '<div class="profile-statistics">' +
                        '<div class="block-title">Statistics</div>' +
                        '<div class="profile-statistics-content">' +
                            '<div class="media-statistics">' +
                                '<a href="' + application.blogger.instagram + '" class="media-title-link">' +
                                    '<svg class="block-title-icon instagram">' +
                                        '<use xlink:href="#instagram"></use>' +
                                    '</svg>' +
                                    '<div class="block-title-text">instagram</div>' +
                                '</a>' +
                                '<div class="media-data">' +
                                    '<div class="media-block-item">' +
                                        '<div class="block-item-title">Followers:</div>' +
                                        '<div class="block-item">100k</div>' +
                                    '</div>' +
                                    '<div class="media-block-item">' +
                                        '<div class="block-item-title">Comments:</div>' +
                                        '<div class="block-item">1.8k</div>' +
                                    '</div>' +
                                    '<div class="media-block-item">' +
                                        '<div class="block-item-title">Likes:</div>' +
                                        '<div class="block-item">257k</div>' +
                                    '</div>' +
                                    '<div class="media-block-item">' +
                                        '<div class="block-item-title">Frequency:</div>' +
                                        '<div class="block-item"></div>' +
                                    '</div>' +
                                '</div>' +
                            '</div>' +
                            '<div class="media-statistics">' +
                                '<a href="' + application.blogger.youtube + '" class="media-title-link">' +
                                    '<svg class="block-title-icon youtube">' +
                                        '<use xlink:href="#youtube"></use>' +
                                    '</svg>' +
                                    '<div class="block-title-text">youtube</div>' +
                                '</a>' +
                                '<div class="media-data">' +
                                    '<div class="media-block-item">' +
                                        '<div class="block-item-title">Followers:</div>' +
                                        '<div class="block-item">100k</div>' +
                                    '</div>' +
                                    '<div class="media-block-item">' +
                                        '<div class="block-item-title">Comments:</div>' +
                                        '<div class="block-item">1.8k</div>' +
                                    '</div>' +
                                    '<div class="media-block-item">' +
                                        '<div class="block-item-title">Likes:</div>' +
                                        '<div class="block-item">257k</div>' +
                                    '</div>' +
                                    '<div class="media-block-item">' +
                                        '<div class="block-item-title">Frequency:</div>' +
                                        '<div class="block-item"></div>' +
                                    '</div>' +
                                '</div>' +
                            '</div>' +
                        '</div>' +
                        '<div class="application-buttons">' +
                        '</div>' +
                    '</div>' +
                '</div>' +
            '</div>',
        buttons: {
            "refuse": {
                btnClass: "btn-red",
                action: function(){
                    $.alert({
                        title: "Refuse application",
                        content: "Are you sure you want to refuse this application?",
                        buttons: {
                            yes: {
                                btnClass: "btn-red",
                                action: function(){
                                    rateApplication(false, application)
                                }
                            },
                            no: function(){

                            }
                        }
                    })
                }
            },
            "contact blogger": {
                btnClass: "btn-green",
                action: function(){
                    $.alert({
                        closeIcon: true,
                        columnClass: "col-6",
                        backgroundDismiss: true,
                        draggable: false,
                        title: "Contacts of blogger",
                        content: "" +
                            '<div class="profile-block-item">' +
                                '<div class="block-item-title">Phone:</div>' +
                                '<div class="block-item" id="phone">' + application.blogger.phone + '</div>' +
                            '</div>' +
                            '<div class="profile-block-item">' +
                                '<div class="block-item-title">Email:</div>' +
                                '<div class="email" id="email">' + application.blogger.email + '</div>' +
                            '</div>' +
                            '<div class="profile-block-item">' +
                                '<div class="block-item-title">Instagram:</div>' +
                                '<a class="block-item" id="instagram" href="' + application.blogger.instagram + '">' + application.blogger.instagram + '</a>' +
                            '</div>' +
                            '<div class="profile-block-item">' +
                                '<div class="block-item-title">youtube:</div>' +
                                '<a class="email" id="youtube" href="' + application.blogger.youtube + '">' + application.blogger.youtube + '</a>' +
                            '</div>' +
                            'If you are working with this blogger and have contact you can hide this application.',

                        buttons: {
                            close: function(){},
                            hide: {
                                text: "hide application",
                                btnClass: "btn-red",
                                action: function(){
                                    $.confirm({
                                        title: "Hide application",
                                        content: "Are you sure you want to hide this application?",
                                        buttons: {
                                            yes:{
                                                btnClass: "btn-red",
                                                action: function(){
                                                    rateApplication(true, application)
                                                }
                                            },
                                            no: {}
                                        }
                                    })
                                }
                            }
                        }
                    })
                }
            }
        }
    })
}

function checkApplicationsInner(applicationsInner){
    if (applicationsInner.innerHTML == ""){
        applicationsInner.innerHTML = '<div class="applications-alert">' +
        '<div class="applications-alert-text">You don\'t have any applications for this offer yet.</div>' +
        '</div>'
    }
}

function rateApplication(upvote, application){
    request = new XMLHttpRequest()
    data = new FormData()
    data.append("upvote", upvote)
    request.open("POST", "/api/applications/rate/" + application.id + "/", true)
    request.setRequestHeader('X-CSRFToken', csrftoken)
    request.onload = function(event){
        if(request.status == 200){
            applicationHtml = document.querySelector("#application-" + application.id)
            applicationHtml.remove()
            applicationsInner = document.querySelector("#applications-inner-"+ application.offer)
            checkApplicationsInner(applicationsInner)
        } else {
            $.alert({
                type: "error",
                title: "Error",
                content: "Error " + request.status + " occurred when trying to hide your offer."
            })
        }
    }
    request.send(data)
}


