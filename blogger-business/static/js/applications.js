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
    fetch("/api/applications/fetch/" + offer.offer_id + "/")
    .then(response => {
        return response.json()
    })
    .then(data => {
        data = JSON.parse(data)
        applicationsInner = document.querySelector("#applications-inner-" + offer.offer_id)
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
    offer = '<div class="offer" id="offer-' + data.offer_id + '">' +
                '<div class="offer-header">' +
                    '<div class="offer-title">' +
                        data.title +
                    '</div>' +
                '</div>' +
                '<div class="applications-inner" id="applications-inner-' + data.offer_id + '">' +
                '</div>' +
            '</div>'
    return offer
}

function createApplicationDiv(data){
    youtube = data.blogger.youtube
    if (youtube && youtube.channel_id){
        youtubeStatisticsHtml = '' +
            `<div class="statistics-block">
                <div class="statistics-title">Followers:</div>
                <div class="statistics-number">` + toShortenNumber(youtube.statistics.subscribers) + `</div>
            </div>
            <div class="statistics-block">
                <div class="statistics-title">Videos:</div>
                <div class="statistics-number">` + toShortenNumber(youtube.statistics.total_video_count) + `</div>
            </div>
            <div class="statistics-block">
                <div class="statistics-title">Views:</div>
                <div class="statistics-number">` + toShortenNumber(youtube.statistics.total_views) + `</div>
            </div>`
    }

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
                                            '<svg class="application-link-icon" id="youtube-application-icon">' +
                                                '<use xlink:href="#youtube"></use>' +
                                            '</svg>' +
                                        '</a>' +
                                    '</div>' +
                                '</div>' +
                            '</div>' +
                            '<div class="application-statistics">' +
                                '<div class="application-statistics-title">' +
                                    '<svg class="application-statistics-title-icon">' +
                                        '<use xlink:href="#youtube"></use>' +
                                    '</svg>' +
                                    '<div class="application-statistics-title-text">Statistics</div>' +
                                '</div>' +
                                '<div class="statistics-inner">' +
                                    youtubeStatisticsHtml +
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

    let youtube = application.blogger.youtube
    let youtubeHtml = '' + 
        `<div class="statistics-title-link-div no-hover-link" id="youtube-link-div">
            <div class="statistics-title-link">
                <svg class="statistics-title-icon youtube">
                    <use xlink:href="#youtube"></use>
                </svg>
                <div class="statistics-title-text">youtube</div>
            </div>
        </div>
        <div class="statistics-disabled" id="google-is-not-connected">
            <div class="statistics-disabled-text">Account isn't connected</div>
        </div>`
    let youtubeUrlHtml = ""
    if (youtube && youtube.channel_id){
        youtubeHtml = '' + 
            `<div class="statistics-title-link-div" id="youtube-link-div">
                <a href="` + application.blogger.youtube.url + `" class="statistics-title-link">
                    <svg class="statistics-title-icon youtube">
                        <use xlink:href="#youtube"></use>
                    </svg>
                    <div class="statistics-title-text">youtube</div>
                </a>
            </div>
            <div class="statistics-total" id ="youtube-total-statistics">
                <div class="statistics-block-item">
                    <svg class="statistics-item-icon youtube">
                        <use xlink:href="#subscribers"></use>
                    </svg>
                    <div class="statistics-item-total" id="youtube-subscribers">` + toShortenNumber(youtube.statistics.subscribers) + `</div>
                </div>
                <div class="statistics-block-item">
                    <svg class="statistics-item-icon youtube">
                        <use xlink:href="#videos"></use>
                    </svg>
                    <div class="statistics-item-total" id="youtube-videos">` + toShortenNumber(youtube.statistics.total_video_count) + `</div>
                </div>
                <div class="statistics-block-item">
                    <svg class="statistics-item-icon youtube">
                        <use xlink:href="#views"></use>
                    </svg>
                    <div class="statistics-item-total" id="youtube-views">` + toShortenNumber(youtube.statistics.total_views) + `</div>
                </div>
            </div>
            <div class="statistics-month" id="youtube-month-statistics">
                <div class="statistics-month-title">December</div>
                <div class="statistics-block-item-month">
                    <div class="statistics-item-title-month col-6">New subscribers: </div>
                    <div class="statistics-item-month" id="youtube-month-subscribers">` + toShortenNumber(youtube.statistics.month_subscribers_gained) + `</div>
                </div>
                <div class="statistics-block-item-month">
                    <div class="statistics-item-title-month col-6">Views: </div>
                    <div class="statistics-item-month" id="youtube-month-views">` + toShortenNumber(youtube.statistics.month_views) + `</div>
                </div>
                <div class="statistics-block-item-month">
                    <div class="statistics-item-title-month col-6">Comments: </div>
                    <div class="statistics-item-month" id="youtube-month-comments">` + toShortenNumber(youtube.statistics.month_comments) + `</div>
                </div>
                <div class="statistics-block-item-month">
                    <div class="statistics-item-title-month col-6">Likes: </div>
                    <div class="statistics-item-month" id="youtube-month-likes">` + toShortenNumber(youtube.statistics.month_likes) + `</div>
                </div>
                <div class="statistics-block-item-month">
                    <div class="statistics-item-title-month col-6">Dislikes: </div>
                    <div class="statistics-item-month" id="youtube-month-dislikes">` + toShortenNumber(youtube.statistics.month_dislikes) + `</div>
                </div>
            </div>`

        youtubeUrlHtml = '' +
        `<div class="profile-block-item">
            <div class="block-item-title">Youtube:</div>
            <a class="email" target="_blank" id="youtube" href="` + application.blogger.youtube.url + `">` + application.blogger.youtube.name + `</a>
        </div>`
    }

    instagramUrlHtml = ''
    $.confirm({
        title: application.blogger.blog_name,
        closeIcon: true,
        columnClass: "col-9",
        backgroundDismiss: true,
        draggable: false,
        theme: 'material',
        content: '' +
            `<div class="profile-container-inner">
                <div class="profile-top-part">
                    <div class="modal-profile-image-div">
                        <div class="stretcher"></div>
                        <img src="` + application.blogger.image + `" id="modal-profile-image" class="image img-fluid">
                    </div>
                    <div class="profile-block">
                        <div class="profile-block-item">
                            <div class="block-item-title">Location:</div>
                            <div class="block-item" id="location">
                                <div class="location-item" id="country">` + application.blogger.location.country +`</div>
                                <span>,&nbsp</span>
                                <div class="location-item" id="city">` + application.blogger.location.city + `</div>
                            </div>
                        </div>
                        <div class="profile-block-item">
                            <div class="block-item-title">Birthday:</div>
                            <div class="block-item" id="birthday">` + application.blogger.birthday + `</div>
                        </div>
                        <div class="profile-block-item">
                            <div class="block-item-title">Languages:</div>
                            <div class="block-items" id="languages">` +
                                languagesHtml +
                            `</div>
                        </div>
                        <div class="profile-block-item">
                            <div class="block-item-title">Specializations:</div>
                            <div class="block-items" id="specializations">` +
                                specializationsHtml +
                            `</div>
                        </div>
                        <div class="profile-block-item">
                            <div class="block-item-title">Phone:</div>
                            <div class="block-item" id="phone">` + application.blogger.phone + `</div>
                        </div>
                        <div class="profile-block-item">
                            <div class="block-item-title">Email:</div>
                            <div class="email" id="email">` + application.blogger.email + `</div>
                        </div>
                    </div>
                </div>
                <div class="bottom-part">
                    <div class="profile-statistics">
                        <div class="block-title">Statistics</div>
                        <div class="profile-statistics-content">
                            <div class="media-statistics" id="youtube-statistics">` +
                                youtubeHtml +
                            `</div>
                            <div class="media-statistics instagram-statistics disabled-block">
                                <div class="statistics-title-link-div" id="instagram-link-div">
                                    <div class="statistics-title-link no-hover-link">
                                        <svg class="statistics-title-icon instagram">
                                            <use xlink:href="#instagram"></use>
                                        </svg>
                                        <div class="statistics-title-text">instagram</div>
                                    </div>
                                </div>
                                <div class="statistics-disabled" id="facebook-is-not-connected">
                                    <div class="statistics-disabled-text">Account isn't connected</div>
                                </div>
                            </div>
                        </div>
                        <div class="application-buttons">
                        </div>
                    </div>
                </div>
            </div>`,
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
                            `<div class="profile-block-item">
                                <div class="block-item-title">Phone:</div>
                                <div class="block-item" id="phone">` + application.blogger.phone + `</div>
                            </div>
                            <div class="profile-block-item">
                                <div class="block-item-title">Email:</div>
                                <div class="email" id="email">` + application.blogger.email + `</div>
                            </div>` +
                            instagramUrlHtml +
                            youtubeUrlHtml +
                            `If you are working with this blogger and have contacts you can hide this application.`,

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
