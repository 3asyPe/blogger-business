var offersTitleDiv = document.querySelector(".offers-title")
var editMode = window.location.pathname !== "/offers/create/"
if (!editMode){
    offersTitleDiv.innerHTML = "Create offer"
} else {
    offersTitleDiv.innerHTML = "Edit your offer"
    fetchOfferData(window.location.pathname.split("/")[3])
}

var defaultProperties;

function fetchOfferData(offer_id){
    console.log(offer_id)
    fetch("/api/offers/" + offer_id + "/")
    .then(response => {
        return response.json()
    })
    .then(data => {
        data = JSON.parse(data)
        if (data !== {}){
            console.log(data)

            defaultProperties = data

            fetchLanguages()
            fetchSpecializations()
            selectGroupOfSubscribers()
            selectSex()
            let ageGroupSelect = document.querySelector("#age_group")
            ageGroupSelect.value = data.blogger_model.age_group

            if (data.price){
                let priceInput = document.querySelector("#price")
                priceInput.value = data.price
            }

            showImage(data.image)

            let titleInput = document.querySelector("#title")
            titleInput.value = data.title

            let descriptionInput = document.querySelector("#description")
            descriptionInput.value = data.description

            let conditionsInput = document.querySelector("#conditions")
            conditionsInput.value = data.conditions

            let deliveryIcon = document.querySelector("#delivery-icon")
            if (data.receiving_model.delivery == true){
                if (deliveryIcon.classList.contains("fa-times")){
                    deliveryIcon.classList.remove("fa-times")
                    deliveryIcon.classList.add("fa-check")
                }
            } else {
                if (deliveryIcon.classList.contains("fa-check")){
                    deliveryIcon.classList.remove("fa-check")
                    deliveryIcon.classList.add("fa-times")
                }
            }
            
            let pickupIcon = document.querySelector("#pickup-icon")
            if (data.receiving_model.address){
                let addressInput = $("#address")
                if (pickupIcon.classList.contains("fa-times")){
                    pickupIcon.classList.remove("fa-times")
                    pickupIcon.classList.add("fa-check")
                }
                addressInput.attr("value", data.receiving_model.address)
                addressInput.show()
            } else {
                if (pickupIcon.classList.contains("fa-check")){
                    pickupIcon.classList.remove("fa-check")
                    pickupIcon.classList.add("fa-times")
                }
                addressInput.val = ""
                addressInput.hide()
            }

            let validity = data.validity
            const date = new Date(validity);
            const year = new Intl.DateTimeFormat('en', { year: 'numeric' }).format(date);
            const month = new Intl.DateTimeFormat('en', { month: 'numeric' }).format(date);
            const day = new Intl.DateTimeFormat('en', { day: 'numeric' }).format(date);

            let dayInput = document.querySelector("#day")
            dayInput.value = day

            let monthInput = document.querySelector("#month")
            monthInput.value = month

            let yearInput = document.querySelector("#year")
            yearInput.value = year

            let validityDiv = document.querySelector(".validity-div")
            if (validity <= new Date()){
                addWarning(validityDiv)
            } 

            let blogger_model = data.blogger_model

        }
    })
}

var additionalPriceDiv = document.querySelector(".additional-price")

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

// Form submiting

var form = document.querySelector("#offer-form");

form.addEventListener('submit', function(ev) {
    ev.preventDefault()
    var oData = new FormData(form)
    console.log(new FormData(form))
    oData = getDataFromExampleCard(oData)

    if (oData == false){
        $.alert({
            title: "Warning!",
            content: "Please fill out right info"
        })
        return false
    }

    console.log(oData)

    var oReq = new XMLHttpRequest()

    if (editMode){
        url = "/api/offers/edit/" + defaultProperties.id + "/"
    } else {
        url = "/api/offers/create/"
    }
    oReq.open("POST", url, true)
    oReq.onload = function(oEvent) {
        if (oReq.status == 201) {
            console.log(oReq.response)
            window.location.href = "/offers/?action=created"
        } else if(oReq.status == 200){
            console.log(oReq.response)
            window.location.href = "/offers/?action=edited"
        } else {
            console.log("Error " + oReq.status + " occurred when trying to create new offer.")
        }
    };

    oReq.send(oData)
}, false)

function getDataFromExampleCard(data){
    console.log(data)
    valid = true

    let priceInput = document.querySelector("#price")
    if (priceInput.value != 0){
        data.append("price", priceInput.value)
    }

    let image = document.querySelector("#image")
    let imagePlaceholder = document.querySelector(".image-placeholder")
    if (image.src != ""){
        removeWarning(imagePlaceholder)
    } else {
        addWarning(imagePlaceholder)
        valid = false
    }

    let titleInput = document.querySelector("#title")
    if (titleInput.value != ""){
        data.append("title", titleInput.value)
        removeWarning(titleInput)
    } else {
        addWarning(titleInput)
        valid = false
    }

    let descriptionInput = document.querySelector("#description")
    if (descriptionInput.value != ""){
        data.append("description", descriptionInput.value)
        data.description = descriptionInput.value
        removeWarning(descriptionInput)
    } else {
        addWarning(descriptionInput)
        valid = false
    }

    let conditionsInput = document.querySelector("#conditions")
    if (conditionsInput.value != ""){
        data.append("conditions", conditionsInput.value)
        removeWarning(conditionsInput)
    } else {
        addWarning(conditionsInput)
        valid = false
    }

    let deliveryIcon = document.querySelector("#delivery-icon")
    if (deliveryIcon.classList.contains("fa-check")){
        data.append("delivery", true)
    } else {
        data.append("delivery", false)
    }

    let pickupIcon = document.querySelector("#pickup-icon")
    let addressInput = document.querySelector("#address")
    if (pickupIcon.classList.contains("fa-check")){
        if (addressInput.value != ""){
            data.append("address", addressInput.value)
            removeWarning(addressInput)            
        } else {
            addWarning(addressInput)
            valid = false
        }   
    } else {
        removeWarning(addressInput)
    }

    let validityDiv = document.querySelector(".validity-div")

    let dayInput = document.querySelector("#day")
    let monthInput = document.querySelector("#month")
    let yearInput = document.querySelector("#year")

    let day = parseInt(dayInput.value)
    let month = parseInt(monthInput.value) - 1
    let year = parseInt(yearInput.value)

    validity = new Date(year, month, day)

    console.log(validity)
    console.log(new Date())

    if (validity > new Date()){
        data.append("day", day)
        data.append("month", month + 1)
        data.append("year", year)
        removeWarning(validityDiv)
    } else {
        addWarning(validityDiv)
        valid = false
    }

    if (valid){
        return data
    } else {
        return false
    }
}

function addWarning(obj){
    if (!obj.classList.contains("warning-background")){
        obj.classList.add("warning-background")
    }
    obj.addEventListener("change", function(){
        removeWarning(obj)
    })
}

function removeWarning(obj){
    if (obj.classList.contains("warning-background")){
        obj.classList.remove("warning-background")
    }
}

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
        showImage(reader.result)
    }
    reader.readAsDataURL(event.target.files[0]);
}

function showImage(source){
    var output = $('.image')
    output.attr("src", source)
    output.show()
    var imagePlaceholder = $('.image-placeholder')
    imagePlaceholder.hide()
}

function fetchLanguages(){
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
}

if (!editMode){
    fetchLanguages()
}

function fetchSpecializations(){
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
}
    
if (!editMode){
    fetchSpecializations()
}

function getLanguageOptionHtml(language){
    if (editMode){
        for(let curLang of defaultProperties.blogger_model.languages){
            if (curLang.language == language.prefix){
                return "<option class='language-option' selected value='" + language.prefix + "'>" + language.language + "</option>"
            }
        }
    }
    return "<option class='language-option' value='" + language.prefix + "'>" + language.language + "</option>"
}


function getSpecializationOptionHtml(specialization){
    if (editMode){
        for(let curSpec of defaultProperties.blogger_model.specializations){
            if (curSpec.specialization == specialization.prefix){
                return "<option class='specialization-option' selected value='" + specialization.prefix + "'>" + specialization.specialization + "</option>"
            }
        }
    }
    return "<option class='specialization-option' value='" + specialization.prefix + "'>" + specialization.specialization + "</option>"
}

function selectGroupOfSubscribers(){
    let subscribersSelect = document.querySelector("#subscribers_number_groups")
    for (let option of subscribersSelect){
        for (let receivedOption of defaultProperties.blogger_model.subscriber_groups){
            if (receivedOption.group == option.value){
                option.selected = true
            }
        }
    }
}

function selectSex(){
    sex = defaultProperties.blogger_model.sex
    if (sex == "M"){
        sexInput = document.querySelector("#sexM")
    } else if (sex == "W") {
        sexInput = document.querySelector("#sexW")
    } else {
        sexInput = document.querySelector("#sexAny")
    }
    sexInput.checked = true
}

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

if (editMode){
    var deleteBtn = document.querySelector(".btn-delete-offer")
    deleteBtn.addEventListener("click", function(){
        $.alert({
            title: "You want to delete an offer",
            content: "Are you sure?",
            buttons: {
                No: {},
                Yes: function(){
                    request = new XMLHttpRequest()
                    request.open("DELETE", "/api/offers/delete/" + defaultProperties.id + "/", true)
                    request.setRequestHeader('X-CSRFToken', csrftoken);
                    request.onload = function(oEvent) {
                        if (request.status == 200) {
                            console.log(request.response)
                            window.location.href = "/offers/?action=deleted"
                        } else {
                            console.log("Error " + request.status + " occurred when trying to delete your offer.")
                        }
                    };
                    request.send()
                }
            }
        })
    })
} else {
    var deleteBtn = $(".btn-delete-offer")
    deleteBtn.hide()
}
    