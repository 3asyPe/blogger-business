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
    fetch("/api/offers/get/" + offer_id + "/")
    .then(response => {
        return response.json()
    })
    .then(data => {
        data = JSON.parse(data)
        if (data !== {}){
            console.log(data)

            defaultProperties = data

            setMinSubscribers(defaultProperties.blogger_model.min_subscribers)
            setMaxSubscribers(defaultProperties.blogger_model.max_subscribers)

            fetchLanguages()
            insertLanguages()
            selectSpecializations()
            selectAgeGroups()
            selectSex()

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
    oData = getDataFromExampleCard(oData)

    if (oData == false){
        $.alert({
            title: "Warning!",
            content: "Please fill in the correct information"
        })
        return false
    }

    oData.delete("min_subscribers")
    oData.delete("max_subscribers")
    oData.append("min_subscribers", min_subscribers)
    oData.append("max_subscribers", max_subscribers)

    let languageInputs = document.querySelector(".language-inputs")
    let languages = []
    for(let languageInputDiv of languageInputs.children){
        languageInput = languageInputDiv.querySelector(".language-input")
        languagePrefix = availableTags.get(camelize(languageInput.value))
        if (!languagePrefix){
            $(languageInput).popover("show")
            if (!languageInput.classList.contains("invalid-field")){
                languageInput.classList.add("invalid-field")
            }
            saveBtn.innerHTML = defaultSaveBtnHtml
            return 
        }
        languages.push(languagePrefix)
    }
    oData.delete("languages")
    for (let language of languages){
        oData.append("languages" ,language)
    }

    if ($('input[name=specializations]:checked').length == 0){
        specInput = document.querySelector("#spec-kids")
        specInput.setCustomValidity("Please select at least one specialization")
        specInput.reportValidity()
        specInput.scrollIntoView({
            behavior: "smooth",
            block: "center",
        })
        saveBtn.innerHTML = defaultSaveBtnHtml
        return
    }

    var oReq = new XMLHttpRequest()

    if (editMode){
        url = "/api/offers/edit/" + defaultProperties.offer_id + "/"
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

    console.log(data.delivery)
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

var availableTags = new Map();

function fetchLanguages(){
    fetch("/api/blog-languages")
    .then(response => {
        return response.json()
    })
    .then(data => {
        const languages = data.languages
        for(let language of languages){
            availableTags.set(camelize(language.language), language.prefix)
        }
    })
}

if (!editMode){
    fetchLanguages()
}

$(".language-input" ).autocomplete({
    source: function(request, response) {
        var results = $.ui.autocomplete.filter(Array.from(availableTags.keys()), request.term);
        response(results.slice(0, 10));
    }
});

function selectAgeGroups(){
    let ageGroupSelects = document.querySelector("#age_groups")
    for (let option of ageGroupSelects.options){
        for (let defSpec of defaultProperties.blogger_model.age_groups){
            if (defSpec.age_group == option.value){
                option.selected = true;
            }
        }
    }
}

function selectSpecializations(){
    let specSelects = document.getElementsByName("specializations")
    for (let option of specSelects){
        for (let defSpec of defaultProperties.blogger_model.specializations){
            if (defSpec.specialization == option.value){
                option.checked = true;
            }
        }
    }
}

function insertLanguages(){
    let languages = defaultProperties.blogger_model.languages
    let firstLanguageInput = document.querySelector("#language-1")
    firstLanguageInput.value = languages[0].language
    if (languages.length > 1){
        let id = 2
        for (let language of languages.slice(1)){
            addLanguageInput(id, language.language, false)
            id += 1
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

var specLimit = 5;
$('input.spec-checkbox').on('change', function(evt) {
   if($('input[name=specializations]:checked').length > specLimit) {
       this.checked = false;
   }
});

function addLanguageInput(id, value, check=true){
    if (!value){
        value = ""
    }
    if (check){
        previousId = parseInt(id) - 1
        languageInput = document.querySelector("#language-" + previousId)
        languagePrefix = availableTags.get(camelize(languageInput.value))
        if (!languagePrefix){
            $("#language-" + previousId).popover("show")
            if (!languageInput.classList.contains("invalid-field")){
                languageInput.classList.add("invalid-field")
            }
            return 
        }
    }

    languageInputs = $(".language-inputs")
    nextId = parseInt(id) + 1
    newLanguageInputHtml = '' +
        `<div class="language-input-div" id="language-div-` + id + `">
            <input type="text" class="language-input custom-form-control" name="languages" id="language-` + id + `" placeholder="Enter language"
                value="` + value + `" data-toggle="language-popover" data-trigger="none" data-content="Language syntax error" data-placement="bottom">
            <button type="button" class="add-language-btn action-language-btn" id="add-language-` + id + `" onclick="addLanguageInput(` + nextId + `)">
                <svg class="add-language-btn-icon action-language-btn-icon">
                    <use xlink:href="#plus"></use>
                </svg>
            </button>
            <button type="button" class="remove-language-btn action-language-btn" id="remove-language-` + id + `" onclick="removeLanguageInput(` + id + `)">
                <svg class="remove-language-btn-icon action-language-btn-icon">
                    <use xlink:href="#remove"></use>
                </svg>
            </button>
        </div>`
        
    languageInputs.append(newLanguageInputHtml)
    $("#language-" + id).autocomplete({
        source: function(request, response) {
            var results = $.ui.autocomplete.filter(Array.from(availableTags.keys()), request.term);
            response(results.slice(0, 10));
        }
    })
    
    document.querySelector("#language-" + id).onfocus = function(e){
        $("#language-" + id).popover("hide")
        if (e.target.classList.contains("invalid-field")){
            e.target.classList.remove("invalid-field")
        }
    }

    checkOnRemoveAndAddButtons(specLimit)
}

function removeLanguageInput(id){
    languageInputs = document.querySelector(".language-inputs")
    languageInput = languageInputs.querySelector("#language-div-" + id)
    languageInputs.removeChild(languageInput)
    checkOnRemoveAndAddButtons(specLimit)
}

function checkOnRemoveAndAddButtons(limit){
    let languageInputs = document.querySelector(".language-inputs")
    i = 0
    for (let languageInputDiv of languageInputs.children){
        i += 1
        let addBtn = languageInputDiv.querySelector(".add-language-btn")
        let removeBtn = languageInputDiv.querySelector(".remove-language-btn")
        if (languageInputDiv == languageInputs.lastChild && i != limit){
            if (addBtn.classList.contains("d-none")){
                addBtn.classList.remove("d-none")
            }
            if (!removeBtn.classList.contains("d-none")){
                removeBtn.classList.add("d-none")
            }
        } else {
            if (!addBtn.classList.contains("d-none")){
                addBtn.classList.add("d-none")
            }
            if (removeBtn.classList.contains("d-none")){
                removeBtn.classList.remove("d-none")
            }
        }
    }
}

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
                    request.open("DELETE", "/api/offers/delete/" + defaultProperties.offer_id + "/", true)
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
    
document.querySelector("#language-1").onfocus = function(e){
    $("#language-1").popover("hide")
    if (e.target.classList.contains("invalid-field")){
        e.target.classList.remove("invalid-field")
    }
}

var min_subscribers = 500000
var max_subscribers = 1000000
$("#slider-range").slider({
    range: true,
    min: 0,
    max: 50000000,
    step: 1000,
    values: [min_subscribers, max_subscribers],
    change: function( event, ui ){
        if (ui.values[0] > ui.values[1]){
            ui.values[0] = ui.values[1]
        }
        if (ui.values[1] < ui.values[0]){
            ui.values[1] = ui.values[0]
        }
        if (ui.values[0] > ui.max){
            ui.values[0] = ui.max
        }
        if (ui.values[0] < ui.min){
            ui.values[0] = ui.min
        }
        if (ui.values[1] > ui.max){
            ui.values[1] = ui.max
        }
        if (ui.values[1] < ui.min){
            ui.values[1] = ui.min
        }
        
        min_subscribers = ui.values[0]
        max_subscribers = ui.values[1]
        $("#min_subscribers").val(toShortenNumber(min_subscribers))
        $("#max_subscribers").val(toShortenNumber(max_subscribers))
    },
    slide: function( event, ui ) {
        
    }
});
$("#min_subscribers").val(toShortenNumber($("#slider-range").slider("values", 0)))
$("#max_subscribers").val(toShortenNumber($("#slider-range").slider("values", 1)))

function setMinSubscribers(val){
    $("#slider-range").slider("values", 0, parseShortenNumber(val))
}

function setMaxSubscribers(val){
    $("#slider-range").slider("values", 1, parseShortenNumber(val))
}

$("#min_subscribers").on("change", function(){
    setMinSubscribers($(this).val())
})
$("#max_subscribers").on("change", function () {
    setMaxSubscribers($(this).val())
})

function camelize(str) {
    return str.replace(/\W+(.)/g, function(match, chr){
        return chr.toUpperCase();
    });
}
