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
        title: 'Thanks!',
        content: "You have created new offer. We will let you know when someone will create a request for you.",
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
                '<div class="offer-card offer-' + data.id + '">' +
                    '<div class="offer-card-inner">' +
                        '<div class="top-part">' +
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
                            '<div class="applications-count-div col-4">' +
                                '<div class="applications-count">' +
                                    applicationsCountHtml +
                                '</div>' +
                            '</div>' +
                            '<div class="validity-div col-8">' +
                                '<div class="validity-label">Expires&nbsp</div>' +
                                '<div class="validity">' + new_validity + '</div>' +
                            '</div>' +
                        '</div>' +
                    '</div>' + 
                '</div>'+
            '</div>'
}

topPart = document.querySelector(".top-part")
topPart.addEventListener("click", function(){
    window.location.href = "https://www.google.by/"
})

validityDiv = document.querySelector(".validity-div")
validityDiv.addEventListener("click", function(){
    window.location.href = "https://www.google.by/"
})

applicationsCountDiv = document.querySelector(".applications-count-div")
applicationsCountDiv.addEventListener("click", function(){
    window.location.href = "/applications"
})