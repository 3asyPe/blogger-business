const saw_help = localStorage.getItem('business-help')
const action = new URL(window.location.href).searchParams.get("action")

if (!saw_help){
    $.alert({
        title: 'Help title',
        content: "Help content",
    })
    localStorage.setItem('business-help', true)
}

if (action === "created"){
    $.alert({
        title: 'You have created new offer!',
        content: "We will let you know when someone will create a request for you.",
        buttons: {
            ok: function(){}
        }
    })
} else if (action === "edited"){
    $.alert({
        title: 'You have edited your offer!',
        content: "We will let you know when someone will create a request for you.",
        buttons: {
            ok: function(){}
        }
    })
} else if (action === "deleted"){
    $.alert({
        title: 'You have deleted your offer!',
        content: "Now it's time to create some more!",
        buttons: {
            ok: function(){}
        }
    })
}

function fetchData(){
    fetch("/api/offers/fetch/")
    .then(response => {
        return response.json()
    })
    .then(data => {
        data = JSON.parse(data)
        offers_container = document.querySelector("#offers-container")
        if (data !== {}){
            console.log(data)
            for (let offer of data){
                console.log(offer)
                offer_html = createOfferDiv(offer)
                offers_container.innerHTML += offer_html
            }
            for (let offer of data){
                let topPart = document.querySelector("#top-part-" + offer.offer_id)
                topPart.addEventListener("click", function(){
                    window.location.href = "/offers/edit/" + offer.offer_id
                })

                let validityDiv = document.querySelector("#validity-div-" + offer.offer_id)
                validityDiv.addEventListener("click", function(){
                    window.location.href = "/offers/edit/" + offer.offer_id
                })

                let applicationsCountDiv = document.querySelector("#applications-count-div-" + offer.offer_id)
                
                applicationsCountDiv.addEventListener("click", function(){
                    window.location.href = "/applications?sc=" + offer.id
                })
            }

            let createCard = document.querySelector(".create-card")
            
            createCard.addEventListener("click", function(){
                window.location.href = "/offers/create/"
            })
        }
    })
}

fetchData()
        
function createOfferDiv(data){
    if (data.applications_count == 0){
        applicationsCountHtml = 'No <i class="fas fa-envelope-open"></i> yet'
    } else {
        applicationsCountHtml = data.applications_count + ' new <i class="fas fa-envelope-open"></i>'
    }

    validity = data.validity
    const d = new Date(validity);
    const ye = new Intl.DateTimeFormat('en', { year: 'numeric' }).format(d);
    const mo = new Intl.DateTimeFormat('en', { month: 'short' }).format(d);
    const da = new Intl.DateTimeFormat('en', { day: '2-digit' }).format(d);
    new_validity = `${da}-${mo}-${ye}`

    return '<div class="offer-card-shell col-6">' +
                '<div class="offer-card offer-' + data.offer_id + '">' +
                    '<div class="offer-card-inner">' +
                        '<div class="top-part" id="top-part-' + data.offer_id + '">' +
                            '<div class="image-div col-4">' +
                                '<img src="' + data.image + '" class="image img-fluid">' +
                            '</div>' +
                            '<div class="top-right-part col-8">' +
                                '<div class="title-div">' +
                                    '<div class="title-inner title">' +
                                        data.title +
                                    '</div>' +
                                '</div>' +
                                '<div class="description-div">' +
                                    '<div class="description">' + data.description + '</div>' +
                                '</div>' +
                            '</div>' +
                        '</div>' +
                        '<div class="bottom-part">' +
                            '<div class="applications-count-div col-4" id="applications-count-div-' + data.offer_id + '">' +
                                '<div class="applications-count">' +
                                    applicationsCountHtml +
                                '</div>' +
                            '</div>' +
                            '<div class="validity-div col-8" id="validity-div-' + data.offer_id + '">' +
                                '<div class="validity-label">Expires&nbsp</div>' +
                                '<div class="validity">' + new_validity + '</div>' +
                            '</div>' +
                        '</div>' +
                    '</div>' + 
                '</div>'+
            '</div>'
            
    
}

