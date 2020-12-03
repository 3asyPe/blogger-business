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
        } else {
            applicationsInner.innerHTML = '<div class="applications-alert">' +
                                                '<div class="applications-alert-text">You don\'t have any applications for this offer yet.</div>' +
                                            '</div>'
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
    application = '<div class="application-shell">' +
                    '<div class="application" id="application-' + data.id + '">' +
                        '<div class="stretcher"></div>' +
                        '<div class="application-inner">' +
                            '<div class="application-header">' +
                                '<div class="application-image-div">' +
                                    '<img src="' + data.blogger.image + '" class="application-image img-fluid">' +
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

function rateOffer(upvote, offerId){
    
}
