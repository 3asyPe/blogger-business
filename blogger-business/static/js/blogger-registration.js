$.confirm({
    title: 'Blogger registration',
    content: 'You can fill out the form or sign in via Facebook',
    theme: 'material',
    buttons: {
        form: function () {
            showForm()
        },
        facebook: function() {

        }
    },
    animation: 'zoom',
    closeAnimation: 'scale'
});

function showForm(){
    let div_form = document.querySelector(".registration")
    div_form.classList.remove("d-none")    
}

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

form.addEventListener('submit', function(ev) {
    ev.preventDefault()

    var oData = new FormData(form)
    
    if(oData.get('image').size === 0){
        $.alert({
            title: 'Image is also required',
            content: "Please fill the image field",
            theme: 'material',
        })
        return
    }

    oData.append("accountType", "blogger");

    var oReq = new XMLHttpRequest()
    oReq.open("POST", "/api/registration/complete", true)
    oReq.onload = function(oEvent) {
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

    saveBtn = document.querySelector("#save-btn")
    defaultSaveBtnHtml = saveBtn.innerHTML
    saveBtn.innerHTML = 'Loading <i class="fas fa-spinner fa-spin"></i>'

    oReq.send(oData)
}, false)

// // Set limit of choosing specializations to max 3

$("#specializations").on('change', function(e) {
    if (Object.keys($(this).val()).length > 3) {
        $('option[value="' +$(this).val().toString().split(',')[3] + '"]').prop('selected', false);

    }
});
