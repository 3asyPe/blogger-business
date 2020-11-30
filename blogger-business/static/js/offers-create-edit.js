function fetchProfileData(){
    fetch("/api/profile-data/")
    .then(response => {
        return response.json()
    })
    .then(data => {
        data = JSON.parse(data)
        if (data !== {}){
            console.log(data)
            
            logo = document.querySelector(".logo")
            logo.src = data.image

            business_name = document.querySelector(".name-text")
            business_name.innerHTML = data.business_name
        }
    })
}

fetchProfileData()

var offersTitleDiv = document.querySelector(".offers-title")
if(window.location.pathname == "/offers/create/"){
    offersTitleDiv.innerHTML = "Create offer"
} else {
    offersTitleDiv.innerHTML = "Edit your offer"
}

var additionalPriceDiv = document.querySelector(".additional-price")

function changeBackground(){
    priceInput = document.querySelector(".price")
    if (priceInput.value == ""){
        additionalPriceDiv.style.backgroundColor = "#ffffff"
        priceInput.style.backgroundColor = "#ffffff"
    } else{
        additionalPriceDiv.style.backgroundColor = "#f8f9fa"
        priceInput.style.backgroundColor = "#f8f9fa"
    }
}

var deliveryIcon = document.querySelector("#delivery-icon")
deliveryIcon.addEventListener("click", function(){
    console.log('CLICKED')
    if (deliveryIcon.classList.contains("fa-check")){
        deliveryIcon.classList.remove("fa-check")
        deliveryIcon.classList.add("fa-times")
    } else {
        deliveryIcon.classList.remove("fa-times")
        deliveryIcon.classList.add("fa-check")
    }
})

var pickupIcon = document.querySelector("#pickup-icon")
var addressInput = $(".address")
pickupIcon.addEventListener("click", function(){
    if (pickupIcon.classList.contains("fa-check")){
        pickupIcon.classList.remove("fa-check")
        pickupIcon.classList.add("fa-times")
        addressInput.hide()
    } else {
        pickupIcon.classList.remove("fa-times")
        pickupIcon.classList.add("fa-check")
        addressInput.show()
        addressInput.focus()
    }
})

function previewImage(event){
    var reader = new FileReader();
    reader.onload = function() {
        var output = document.querySelector('.image');
        output.src = reader.result;
        output.classList.remove("d-none")
        var imagePlaceholder = document.querySelector('.image-placeholder')
        imagePlaceholder.classList.add("d-none")
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

function enterDay(){
    var kcyear = document.getElementsByName("year")[0],
    kcmonth = document.getElementsByName("month")[0],
    kcday = document.getElementsByName("day")[0];
        
    var d = new Date();
    var n = d.getFullYear();
    for (var i = n; i <= 2023; i++) {
        var opt = new Option();
        opt.value = opt.text = i;
        kcyear.add(opt);
    }
    kcyear.addEventListener("change", validate_date);
    kcmonth.addEventListener("change", validate_date);

    function validate_date() {
        var y = +kcyear.value, m = kcmonth.value, d = kcday.value;
        if (m === "2")
            var mlength = 28 + (!(y & 3) && ((y % 100) !== 0 || !(y & 15)));
        else var mlength = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1];
        kcday.length = 0;
        for (var i = 1; i <= mlength; i++) {
            var opt = new Option();
            opt.value = opt.text = i;
            if (i == d) opt.selected = true;
            kcday.add(opt);
        }
    }
    validate_date();
}

enterDay()