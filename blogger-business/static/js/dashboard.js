saw_help = localStorage.getItem('blogger-help')

if (!saw_help){
    // $("#myModal").modal()
    localStorage.setItem('blogger-help', true)
}

function fetchData(){
    fetch("/api/dashboard/fetch/")
    .then(response => {
        return response.json()
    })
    .then(data => {
        data = JSON.parse(data)
        offers_container = document.querySelector("#offers-container")
        if (data !== {}){
            offers = ""
            console.log(data)
            for (let offer of data){
                console.log(offer)
                offer_html = createOfferDiv(offer)
                offers_container.innerHTML += offer_html
            }
        }
    })
}

fetchData()
        
function createOfferDiv(data){
    validity = data.validity
    const d = new Date(validity);
    const ye = new Intl.DateTimeFormat('en', { year: 'numeric' }).format(d);
    const mo = new Intl.DateTimeFormat('en', { month: 'short' }).format(d);
    const da = new Intl.DateTimeFormat('en', { day: '2-digit' }).format(d);

    addressHtml = ""
    deliveryAdditionalClass = ""
    deliveryIconAdditionalClass = ""
    
    if (data.receiving_model.address){
        addressHtml = '<div class="address-label">Pickup:&nbsp</div>' +
        '<div class="address">' + data.receiving_model.address + '</div>'
    } else{
        deliveryAdditionalClass = "centered-delivery"
        deliveryIconAdditionalClass = "centered-delivery-icon"
    }
    
    if(data.receiving_model.delivery){
        deliveryIcon = '<i class="fas fa-check receiving-method-icon ' + deliveryIconAdditionalClass + ' "></i>'
    } else {
        deliveryIcon = '<i class="fas fa-times receiving-method-icon ' + deliveryIconAdditionalClass + ' "></i>'
    }
    
    priceDiv = ""

    if (data.price){
        priceDiv = '<div class="additional-price">' +
                        '$<div class="price">' + data.price + '</div>' +
                    '</div>'
    }

    new_validity = `${da}-${mo}-${ye}`
    defaultOffer =  '<div class="offer-card offer-' + data.offer_id + ' col-lg-12 col-12">' +
                priceDiv +
                '<div class="offer-card-inner">' +
                    '<div class="media-part col-4">' +
                        '<div class="media-top-part">' +
                            '<div class="image-div">' +
                                '<img src="' + data.image + '" class="image img-fluid">' +
                            '</div>' +
                        '</div>' +
                        '<div class="media-bottom-part">' +
                            '<a class="name col-6" href="#">' +
                                '<div class="name-text name">' + data.business.business_name + '</div>' +
                            '</a>' +
                            '<div class="logo-div col-6">' +
                                '<img src="' + data.business.image + '" class="img-fluid">' +
                            '</div>' +
                        '</div>' +
                    '</div>' +
                    '<div class="text-part col-8">' +
                        '<div class="title-div">' +
                            '<div class="title-inner title">' +
                                data.title +
                            '</div>' +
                        '</div>' +
                        '<div class="main-details-div">' +
                            '<div class="description-div col-6">' +
                                '<div class="column-title">' +
                                    'Decription' +
                                '</div>' +
                                '<div class="column-content">' +
                                    '<div class="column-content-inner description">' +
                                        data.description +
                                    '</div>' +
                                '</div>' +
                            '</div>' +
                            '<div class="conditions-div col-6">' +
                                '<div class="column-title">' +
                                    'Conditions' +
                                '</div>' +
                                '<div class="column-content">' +
                                    '<div class="column-content-inner conditions">'+ 
                                        data.conditions +
                                    '</div>' +
                                '</div>' +
                            '</div>' +
                        '</div>' +
                        '<div class="secondary-details-div">' +
                            '<div class="receiving-method col-6">' +
                                '<div class="delivery-div ' + deliveryAdditionalClass + '">' +
                                    '<div class="delivery-label">Delivery</div>' +
                                    deliveryIcon +
                                '</div>' +
                                '<div class="address-div">' +
                                    addressHtml + 
                                '</div>' +
                            '</div>' +
                            '<div class="validity-div col-6">' +
                                '<div class="validity-inner">' +
                                    '<div class="validity-label">Expires&nbsp</div>' +
                                    '<div class="validity">' + new_validity + '</div>' +
                                '</div>' +
                            '</div>' +
                        '</div>' +
                    '</div>' +
                '</div>' +
                '<div class="offer-action-buttons">' +
                    '<button class="action-btn"><i class="fas fa-times action-icon" onclick="rateOffer(false, \'' + data.offer_id + '\')"></i></button>' +
                    '<div class="offer-action-title">Send a request?</div>' +
                    '<button class="action-btn"><i class="fas fa-check action-icon" onclick="rateOffer(true, \'' + data.offer_id + '\')"></i></button>' +
                '</div>' +
            '</div>'
    
    return defaultOffer
}

function rateOffer(upvote, offerId){
    console.log(upvote)
    console.log(offerId)
    data = {
        "offerId": offerId,
        "upvote": upvote,
    }
    
    if (upvote){
        $.confirm({
            title: "Confirmation",
            content: "Are you sure you want to send a request to the business about this offer?",
            buttons: {
                No: function(){},
                Yes: function(){
                    sendRequest(url="/api/offers/rate/", data=data)
                }
            }
        })
    } else{
        $.confirm({
            title: "Confirmation",
            content: "Are you sure you want to cancel this offer?",
            buttons: {
                No: function(){},
                Yes: function(){
                    sendRequest(url="/api/offers/rate/", data=data)
                }
            }
        })
    }

    function sendRequest(url, data){
        var request = new XMLHttpRequest()
        request.open("POST", url, true)
        request.onload = function(event) {
            if (request.status == 200) {
                deleted_offer = $(".offer-" + offerId)
                deleted_offer.hide()
                if(upvote){
                    $.confirm({
                        title: "Thanks",
                        content: "Your request was sent. If you want to cancel it click CANCEL",
                        buttons: {
                            Cancel: function(){
                                deleted_offer.show()
                            },
                            Ok: function(){}
                        }
                    })
                } else {
                    $.confirm({
                        title: "Confirmation",
                        content: "The offer was canceled. If you want to get it back click GET IT BACK",
                        buttons: {
                            "Get it back": function(){
                                deleted_offer.show()
                            },
                            Ok: function(){}
                        }
                    })
                }
            } else {
                $.alert({
                    title: 'An error occured',
                    content: "Error " + request.status + " occurred when trying to send request. Please try again.",
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
        console.log(data)
        request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        request.setRequestHeader('X-CSRFToken', csrftoken);
        request.send(JSON.stringify(data))
    }
}
