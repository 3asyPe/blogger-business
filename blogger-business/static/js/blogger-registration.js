var availableTags = new Map();

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

$(".language-input" ).autocomplete({
    source: function(request, response) {
        var results = $.ui.autocomplete.filter(Array.from(availableTags.keys()), request.term);
        response(results.slice(0, 10));
    }
});

function addLanguageInput(id){
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

    languageInputs = $(".language-inputs")
    nextId = parseInt(id) + 1
    newLanguageInputHtml = '' +
        `<div class="language-input-div" id="language-div-` + id + `">
            <input type="text" class="language-input custom-form-control" name="languages" id="language-` + id + `" placeholder="Enter language"
                data-toggle="language-popover" data-trigger="none" data-content="Language syntax error" data-placement="bottom">
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

    checkOnRemoveAndAddButtons(3)
}

function removeLanguageInput(id){
    languageInputs = document.querySelector(".language-inputs")
    languageInput = languageInputs.querySelector("#language-div-" + id)
    languageInputs.removeChild(languageInput)
    checkOnRemoveAndAddButtons(3)
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

// Adding content in the birthday field
function enterDay(){
    var kcyear = document.getElementsByName("year")[0],
    kcmonth = document.getElementsByName("month")[0],
    kcday = document.getElementsByName("day")[0];
        
    var d = new Date();
    var n = d.getFullYear();
    for (var i = n; i >= 1950; i--) {
        var opt = new Option();
        opt.value = opt.text = i;
        kcyear.add(opt);
    }
    kcyear.addEventListener("change", validate_date);
    kcmonth.addEventListener("change", validate_date);

    function validate_date() {
        var y = kcyear.value, m = kcmonth.value, d = kcday.value;
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

// Form submiting

var form = document.querySelector("#registration-form")

form.addEventListener('submit', async function(ev) {
    ev.preventDefault()

    saveBtn = document.querySelector("#save-btn")
    defaultSaveBtnHtml = saveBtn.innerHTML
    saveBtn.innerHTML = 'Loading <i class="fas fa-spinner fa-spin"></i>'
    
    var oData = new FormData(form)
    
    if(oData.get('image').size === 0){
        imageDiv = document.querySelector(".label-image")
        if (!imageDiv.classList.contains("invalid-field")){
            imageDiv.classList.add("invalid-field")
        }
        imageDiv.scrollIntoView({
            behavior: "smooth",
            block: "center",
        })
        saveBtn.innerHTML = defaultSaveBtnHtml
        return
    }

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

    exists = await check_exists()
    if (exists){
        saveBtn.innerHTML = defaultSaveBtnHtml
        return false
    }

    if (!googleConnected){
        $('[data-toggle="youtube-popover"]').popover("show")
        youtubeBtn = document.querySelector("#google-sign-in-or-out-button")
        youtubeBtn.scrollIntoView({
            behavior: "smooth",
            block: "center",
        })
        return false
    }

    appendUserDataToFormData(googleUser, oData)
    oData.append("google_code", googleAuthCode)

    oData.append("accountType", "blogger");

    var oReq = new XMLHttpRequest()
    oReq.open("POST", "/api/registration/complete", true)

    oReq.onload = function(oEvent) {
        saveBtn.innerHTML = defaultSaveBtnHtml

        if (oReq.status == 201) {
            $.confirm({
                title: 'You have created your account',
                content: "We sent you new password. Please check your email.",
                type: 'blue',
                typeAnimated: true,
                buttons: {
                    ok: {
                        text: 'OK',
                        btnClass: 'btn-blue',
                        action: function () {
                            window.location.href = "/login/"
                        }
                    }
                }
            })
        } else {
            $.alert({
                title: 'An error occured',
                content: "Error " + oReq.status + " occurred when trying to register your account. Please try again.",
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
    oReq.send(oData)
}, false)

function getUsernameField(){
    return document.querySelector("#blog_name")
}

function appendUserDataToFormData(user, formData){
    basicProfile = user.getBasicProfile()
    formData.append("google_email", basicProfile.getEmail())
    formData.append("google_name", basicProfile.getName())
    formData.append("google_image_url", basicProfile.getImageUrl())
}

document.querySelector("#blog_name").onfocus = function(e){
    $('[data-toggle="username-popover"]').popover("hide")
    if (e.target.classList.contains("invalid-field")){
        e.target.classList.remove("invalid-field")
    }
}

document.querySelector(".image-placeholder").onclick = function(e){
    labelImage = document.querySelector(".label-image")
    if (labelImage.classList.contains("invalid-field")){
        labelImage.classList.remove("invalid-field")
    }
}

document.querySelector("#language-1").onfocus = function(e){
    $("#language-1").popover("hide")
    if (e.target.classList.contains("invalid-field")){
        e.target.classList.remove("invalid-field")
    }
}

document.querySelector("#google-sign-in-or-out-button").onfocus = function(e){
    $('[data-toggle="youtube-popover"]').popover("hide")
}

// // Set limit of choosing specializations to max 3

var limit = 3;
$('input.spec-checkbox').on('change', function(evt) {
   if($('input[name=specializations]:checked').length > limit) {
       this.checked = false;
   }
});

var elements = $("input[type=text]");
elements.each(function(index){
    $(this).on("invalid", function(e){
        e.preventDefault();
        if (!e.target.classList.contains("invalid-field")){
            e.target.classList.add("invalid-field")
        }
        $(this).get(0).scrollIntoView({
            behavior: "smooth",
            block: "center",
        })
    })
    $(this).on("focus", function(e) {
        if (e.target.classList.contains("invalid-field")){
            e.target.classList.remove("invalid-field")
        }
    });
})

function camelize(str) {
    return str.replace(/\W+(.)/g, function(match, chr){
        return chr.toUpperCase();
    });
}
