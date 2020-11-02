application =  {
    "id": 2,
    "blogger": {
        "id": 1,
        "image": "/media/blogger/2642282/2642282.png",
        "blog_name": "lox",
        "email": "lox123@gmail.com",
        "instagram": "@lox",
        "youtube": "https://www.youtube.com/",
        "phone": "+375445425221",
        "location": null,
        "sex": "M",
        "birthday": "2004-04-13"
    },
    "offer": 6,
    "timestamp": "2020-11-01T15:42:21.005393Z"
}

function fetchData(){
    fetch("/api/applications/fetch/")
    .then(response => {
        return response.json()
    })
    .then(data => {
        data = JSON.parse(data)
        applicationsContainer = document.querySelector("#applications-container")
        if (data !== {}){
            applications = ""
            console.log(data)
            for (let application of data){
                console.log(application)
                blogger = application.blogger
                applicationHtml = createApplicationDiv(
                    id=application.id,
                    image=blogger.image,
                    blog_name=blogger.blog_name,
                    instagram=blogger.instagram,
                    youtube=blogger.youtube,
                )
                applications += applicationHtml
            }
            applicationsContainer.innerHTML = applications
        }
    })
}

fetchData()
        
function createApplicationDiv(id, image, blog_name, instagram, youtube){
    return '<div class="card" id="application-' + id + '" style="width: 18rem;">' +
                '<img src="' + image + '" class="card-img-top">' +
                '<div class="card-body">' +
                    '<h5 class="card-title">' + blog_name + '</h5>' +
                    '<div class="row">'+
                        '<a href="' + instagram + '">Instagram</a>' +
                        '<a href="' + youtube + '">Youtube</a>' +
                    '</div>' +
                    '<div class="btn-group row">'+
                        '<button type="button" class="btn btn-sm btn-danger" onclick="rateApplication(false, ' + id + ')">dislike</button>' +
                        '<button type="button" class="btn btn-sm btn-success" onclick="rateApplication(true, ' + id + ')">like</button>' +
                    '</div>' +
                '</div>' +
            '</div>'
}

function rateOffer(upvote, offerId){
    // console.log(upvote)
    // console.log(offerId)
    // data = {
    //     "offerId": offerId,
    //     "upvote": upvote,
    // }
    // sendRequest(url="/api/offers/rate/", data=data)

    // deleted_offer = $("#offer-" + offerId)
    // deleted_offer.hide()

    // $.confirm({
    //     title: "Some title",
    //     content: "Some content",
    //     buttons: {
    //         Cancel: function(){
    //             deleted_offer.show()
    //             sendRequest(url="/api/offers/rate/cancel/", {
    //                 "offerId": offerId
    //             })
    //         },
    //         Ok: function(){}
    //     }
    // })

    // function sendRequest(url, data){
    //     var request = new XMLHttpRequest()
    //     request.open("POST", url, true)
    //     request.onload = function(event) {
    //         if (request.status == 200) {
    //             console.log(request.response)
    //         } else {
    //             console.log("Error " + request.status + " occurred")
    //         }
    //     };
    //     console.log(data)
    //     request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    //     request.setRequestHeader('X-CSRFToken', csrftoken);
    //     request.send(JSON.stringify(data))
    // }
}
