const saw_help = localStorage.getItem('business-help')
const action = new URL(window.location.href).searchParams.get("action")

if (!saw_help){
    $("#myModalHelp").modal()
    localStorage.setItem('business-help', true)
}

if (action === "created"){
    $("#myModalCreated").modal()
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
            offers = ""
            console.log(data)
            for (let offer of data){
                console.log(offer)
                offer_html = createOfferDiv(
                    id=offer.pk,
                    image=offer.fields.image,
                    title=offer.fields.title,
                    description=offer.fields.description,
                    )
                    offers += offer_html
                }
                offers_container.innerHTML = offers
            }
        })
}

fetchData()
        
function createOfferDiv(id, image, title, decription){
    return '<div class="card" id="offer-' + id + '" style="width: 18rem;">' +
                '<a href="/offers/' + id + '">' +
                    '<img src="/media/' + image + '" class="card-img-top">' +
                '</a>' +
                '<div class="card-body">' +
                    '<h5 class="card-title">' + title + '</h5>' +
                    '<p class="card-text">' + description + '</p>' +
                '</div>' +
            '</div>'
}