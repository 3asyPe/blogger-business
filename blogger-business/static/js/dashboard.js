saw_help = localStorage.getItem('blogger-help')

if (!saw_help){
    $("#myModal").modal()
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
                    '<div class="btn-group row">'+
                        '<button type="button" class="btn btn-sm btn-danger" onclick="rateOffer(false, ' + id + ')">dislike</button>' +
                        '<button type="button" class="btn btn-sm btn-success" onclick="rateOffer(true, ' + id + ')">like</button>' +
                    '</div>' +
                '</div>' +
            '</div>'
}

function rateOffer(upvote, offerId){
    console.log(upvote)
    console.log(offerId)
    data = {
        "offerId": offerId,
        "upvote": upvote,
    }
    sendRequest(url="/api/offers/rate/", data=data)

    deleted_offer = $("#offer-" + offerId)
    deleted_offer.hide()

    $.confirm({
        title: "Some title",
        content: "Some content",
        buttons: {
            Cancel: function(){
                deleted_offer.show()
                sendRequest(url="/api/offers/rate/cancel/", {
                    "offerId": offerId
                })
            },
            Ok: function(){}
        }
    })

    function sendRequest(url, data){
        var request = new XMLHttpRequest()
        request.open("POST", url, true)
        request.onload = function(event) {
            if (request.status == 200) {
                console.log(request.response)
            } else {
                console.log("Error " + request.status + " occurred")
            }
        };
        console.log(data)
        request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        request.setRequestHeader('X-CSRFToken', csrftoken);
        request.send(JSON.stringify(data))
    }
}
