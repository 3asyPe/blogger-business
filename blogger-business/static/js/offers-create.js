function previewImage(event){
    var reader = new FileReader();
    reader.onload = function() {
        var output = document.querySelector('#upload-image-icon');
        output.src = reader.result;
    }
    reader.readAsDataURL(event.target.files[0]);
}

fetch("/api/blog-languages")
    .then(response => {
        return response.json()
    })
    .then(data => {
        const languages = data.languages
        let selectEl = document.querySelector("#languages")
        let selectElHTML = selectEl.innerHTML
        for(let language of languages){
            selectElHTML += getLanguageOptionHtml(language)
        }
        selectEl.innerHTML = selectElHTML
    })

fetch("/api/blog-specializations")
    .then(response => {
        return response.json()
    })
    .then(data => {
        const specializations = data.specializations
        let selectEl = document.querySelector("#specializations")
        let selectElHTML = selectEl.innerHTML
        for(let specialization of specializations){
            selectElHTML += getSpecializationOptionHtml(specialization)
        }
        selectEl.innerHTML = selectElHTML
    })

function getLanguageOptionHtml(language){
    return "<option class='language-option' value='" + language.prefix + "'>" + language.language + "</option>"
}

function getSpecializationOptionHtml(specialization){
    return "<option class='specialization-option' value='" + specialization.prefix + "'>" + specialization.specialization + "</option>"
}

// Form submiting

var form = document.querySelector("#offer-creation-form");

form.addEventListener('submit', function(ev) {
    ev.preventDefault()
    var oData = new FormData(form)
    
    if(oData.get('image').size === 0){
        alert("Image field is also required")
        return
    }

    var oReq = new XMLHttpRequest()
    oReq.open("POST", "/api/offers/create/", true)
    oReq.onload = function(oEvent) {
        if (oReq.status == 201) {
            console.log(oReq.response)
            window.location.href = "/offers/?action=created"
        } else {
            console.log("Error " + oReq.status + " occurred when trying to create new offer.")
        }
    };

    oReq.send(oData)
}, false)

// Set limit of choosing specializations to max 5

$("#specializations").on('change', function(e) {
    if (Object.keys($(this).val()).length > 5) {
        $('option[value="' +$(this).val().toString().split(',')[5] + '"]').prop('selected', false);

    }
});