let defaultProfileData;

function fetchFullData(){
    fetch("/api/blogger-profile-data/")
    .then(response => {
        return response.json()
    })
    .then(data => {
        defaultProfileData = JSON.parse(data)
        console.log(defaultProfileData)
        var image = document.querySelector('#upload-image-icon');
        image.src = defaultProfileData.image

        var blog_name = document.querySelector("#blog_name")
        blog_name.innerHTML = defaultProfileData.blog_name

        var country = document.querySelector("#country")
        var city = document.querySelector("#city")
        country.innerHTML = defaultProfileData.location.country
        city.innerHTML = defaultProfileData.location.city

        var birthday = document.querySelector("#birthday")
        birthday.innerHTML = defaultProfileData.birthday

        putLanguagesDivsIntoHtml("languages")

        putSpecializationsDivsIntoHtml("specializations")

        var phone = document.querySelector("#phone")
        phone.innerHTML = defaultProfileData.phone

        var email = document.querySelector("#email")
        email.innerHTML = defaultProfileData.email
    })
}

fetchFullData()

function fetchImageData(){
    fetch("/api/blogger-profile-data/image")
    .then(response => {
        return response.json()
    })
    .then(data => {
        data = JSON.parse(data)
        console.log(data)
        defaultProfileData.image = data.image

        var image = document.querySelector('#upload-image-icon');
        image.src = defaultProfileData.image

        var imageNavbar = document.querySelector("#profile-image-navbar")
        imageNavbar.src = defaultProfileData.image
    })
}

function fetchPersonalData(){
    fetch("/api/blogger-profile-data/personal")
    .then(response => {
        return response.json()
    })
    .then(data => {
        data = JSON.parse(data)
        console.log(data)
        
        defaultProfileData.blog_name = data.blog_name
        var blog_name = document.querySelector("#blog_name")
        blog_name.innerHTML = defaultProfileData.blog_name

        defaultProfileData.location.country = data.location.country
        defaultProfileData.location.city = data.location.city
        var country = document.querySelector("#country")
        var city = document.querySelector("#city")
        country.innerHTML = defaultProfileData.location.country
        city.innerHTML = defaultProfileData.location.city

        defaultProfileData.birthday = data.birthday
        var birthday = document.querySelector("#birthday")
        birthday.innerHTML = defaultProfileData.birthday
    })
}

function fetchBlogData(){
    fetch("/api/blogger-profile-data/blog")
    .then(response => {
        return response.json()
    })
    .then(data => {
        data = JSON.parse(data)
        console.log(data)
        
        defaultProfileData.languages = data.languages
        putLanguagesDivsIntoHtml("languages")

        defaultProfileData.specializations = data.specializations
        putSpecializationsDivsIntoHtml("specializations")

        defaultProfileData.phone = data.phone
        var phone = document.querySelector("#phone")
        phone.innerHTML = defaultProfileData.phone

        defaultProfileData.email = data.email
        var email = document.querySelector("#email")
        email.innerHTML = defaultProfileData.email
    })
}

function previewImage(event){
    var reader = new FileReader();
    reader.onload = function() {
        var output = document.querySelector('#upload-image-icon');
        output.src = reader.result;
    }
    reader.readAsDataURL(event.target.files[0]);
    var saveBtn = document.querySelector(".btn-save-change-image")
    saveBtn.classList.remove("d-none")
}

var imageForm = document.querySelector("#image-form")

imageForm.addEventListener('submit', function(ev) {
    ev.preventDefault()

    var oData = new FormData(imageForm)

    var oReq = new XMLHttpRequest()
    oReq.open("POST", "/api/blogger-profile-data/image/edit/", true)

    var saveBtn = document.querySelector(".btn-save-change-image")
    
    oReq.onload = function(oEvent) {
        fetchImageData()
        saveBtn.innerHTML = defaultSaveBtnHtml
        saveBtn.classList.add("d-none")
        if (oReq.status == 200) {
        } else {
            $.alert({
                title: 'An error occured',
                content: "Error " + oReq.status + " occurred when trying to edit your profile image. Please try again.",
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

    defaultSaveBtnHtml = saveBtn.innerHTML
    saveBtn.innerHTML = 'Loading <i class="fas fa-spinner fa-spin"></i>'

    oReq.send(oData)
}, false)

function editPersonalInfo(){
    var blog_name = defaultProfileData.blog_name
    var country = defaultProfileData.location.country
    var city = defaultProfileData.location.city
    
    $.confirm({
        title: 'Edit personal info',
        columnClass: "medium",
        content: '' +
        '<form action="" method="POST" class="formName" id="editPersonalForm">' +
            '<div class="form-group">' +
                '<label for="edit-blog-name">Your name:</label>' +
                '<input type="text" id="edit-blog-name" name="blog_name" value="' + blog_name + '" class="blog_name form-control" required />' +
            '</div>' +
            '<div class="form-group">' +
                '<label for="edit-country">Your country:</label>' +
                '<input type="text" id="edit-country" name="country" value="' + country + '" class="country form-control" required />' +
            '</div>' +
            '<div class="form-group">' +
                '<label for="edit-city">Your city:</label>' +
                '<input type="text" id="edit-city" name="city" value="' + city + '" class="city form-control" required />' +
            '</div>' +
            '<div class="form-group birthday-div">' +
                '<div class="col-3 col-form-label form-label">Birthday:</div>' +
                '<select name="month" onchange="enterDay()" required class="month custom-select col-2 birthday-" id="month-selector">' +
                    '<option value="1" selected>Jan</option>' +
                    '<option value="2">Feb</option>' +
                    '<option value="3">Mar</option>' +
                    '<option value="4">Apr</option>' +
                    '<option value="5">May</option>' +
                    '<option value="6">Jun</option>' +
                    '<option value="7">Jul</option>' +
                    '<option value="8">Aug</option>' +
                    '<option value="9">Sep</option>' +
                    '<option value="10">Oct</option>' +
                    '<option value="11">Nov</option>' +
                    '<option value="12">Dec</option>' +
                '</select>' +
                '<select name="day" required class="day custom-select col-2" id="day-selector">' +
                    '<option value="1" selected>1</option>' +
                '</select>' +
                '<select name="year" required onchange="enterDay()" class="year custom-select col-2" id="year-selector">' +
                '<option value="2020" selected>2020</option>' +
                '</select>' +
            '</div>' +
        '</form>',
        buttons: {
            formSubmit: {
                text: 'Submit',
                btnClass: 'btn-blue',
                action: function () {
                    var editPersonalForm = document.querySelector("#editPersonalForm")
                    console.log(editPersonalForm)

                    var oData = new FormData(editPersonalForm)
                    
                    console.log(oData)
                    
                    var oReq = new XMLHttpRequest()
                    oReq.open("POST", "/api/blogger-profile-data/personal/edit/", true)
                    oReq.setRequestHeader('X-CSRFToken', csrftoken)
                    
                    oReq.onload = function(oEvent) {
                        fetchPersonalData()
                        if (oReq.status == 200) {
                        } else {
                            $.alert({
                                title: 'An error occured',
                                content: "Error " + oReq.status + " occurred when trying to edit your personal info. Please try again.",
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
                }
            },
            cancel: function () {
                //close
            },
        },
        onContentReady: function () {
            // bind to events
            enterDay()
            selectCurrentDate()
            var jc = this;

            form = this.$content.find('form')
            console.log(form)
            console.log(form.serializeArray())

            this.$content.find('form').on('submit', function (e) {
                // if the user submits the form by pressing enter in the field.
                e.preventDefault();

                jc.$$formSubmit.trigger('click'); // reference the button and click it
            });
        }
    })
}

function editBlogInfo(){
    var languages = defaultProfileData.languages
    var specializations = defaultProfileData.specializations
    var phone = defaultProfileData.phone
    var email = defaultProfileData.email
    
    $.confirm({
        title: 'Edit blog info',
        columnClass: "medium",
        content: '' +
        '<form action="" id="editBlogForm" class="formName">' +
            '<div class="form-group">' +
                '<label for="edit-languages">Languages of blog:</label>' +
                '<select id="edit-languages" required name="languages" multiple class="custom-select col-4">' +
                '</select>' +
            '</div>' +
            '<div class="form-group">' +
                '<label for="edit-specializations">Specializations of blog (max 3):</label>' +
                '<select id="edit-specializations" required name="specializations" multiple class="specializations custom-select col-4">' +
                '</select>' +
            '</div>' +
            '<div class="form-group">' +
                '<label for="edit-phone">Your phone:</label>' +
                '<input type="text" id="edit-phone" name="phone" value="' + phone + '" class="form-control" required />' +
            '</div>' +
            '<div class="form-group">' +
                '<label for="edit-email">Your email:</label>' +
                '<input type="text" id="edit-email" name="email" value="' + email + '" class="form-control" required />' +
            '</div>' +
        '</form>',
        buttons: {
            formSubmit: {
                text: 'Submit',
                btnClass: 'btn-blue',
                action: function () {
                    var editBlogForm = document.querySelector("#editBlogForm")
                    console.log(editBlogForm)

                    var oData = new FormData(editBlogForm)
                    
                    console.log(oData)
                    
                    var oReq = new XMLHttpRequest()
                    oReq.open("POST", "/api/blogger-profile-data/blog/edit/", true)
                    oReq.setRequestHeader('X-CSRFToken', csrftoken)
                    
                    oReq.onload = function(oEvent) {
                        fetchBlogData()
                        if (oReq.status == 200) {
                        } else {
                            $.alert({
                                title: 'An error occured',
                                content: "Error " + oReq.status + " occurred when trying to edit your blog info. Please try again.",
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
                }
            },
            cancel: function () {
                //close
            },
        },
        onContentReady: function () {
            // bind to events
            fetchLanguages()
            fetchSpecializations()
            var jc = this;

            $(".specializations").on('change', function(e) {
                if (Object.keys($(this).val()).length > 3) {
                    $('option[value="' +$(this).val().toString().split(',')[3] + '"]').prop('selected', false);
            
                }
            });

            this.$content.find('form').on('submit', function (e) {
                // if the user submits the form by pressing enter in the field.
                e.preventDefault();
                jc.$$formSubmit.trigger('click'); // reference the button and click it
            });
        }
    })
}


function enterDay(){
    var kcyear = document.getElementsByName("year")[0],
    kcmonth = document.getElementsByName("month")[0],
    kcday = document.getElementsByName("day")[0];
        
    var d = new Date();
    var n = d.getFullYear() - 1;
    for (var i = n; i >= 1950; i--) {
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

function selectCurrentDate(){
    var birthday = defaultProfileData.birthday.split("-")
    var year = birthday[0]
    var month = birthday[1]
    var day = birthday[2]

    var yearSelector = document.querySelector("#year-selector")
    var monthSelector = document.querySelector("#month-selector")
    var daySelector = document.querySelector("#day-selector")

    for(let yearSelect of yearSelector.options){
        if (yearSelect.value == year){
            yearSelect.selected = true
        }
    }

    for(let monthSelect of monthSelector.options){
        if (monthSelect.index + 1 == month){
            monthSelect.selected = true
        }
    }

    for(let daySelect of daySelector.options){
        if (daySelect.value == day){
            daySelect.selected = true
        }
    }
}

function putLanguagesDivsIntoHtml(id){
    var languagesDiv = document.querySelector("#" + id)
    var languages = ""
    for(const language of defaultProfileData.languages){
        languages += "<div class='block-item'>" + language.language + "</div>"
    }
    languagesDiv.innerHTML = languages
}

function putSpecializationsDivsIntoHtml(id){
    var specializationsDiv = document.querySelector("#" + id)
    var specializations = ""
    for(const specialization of defaultProfileData.specializations){
        specializations += "<div class='block-item'>" + specialization.specialization + "</div>"
    }
    specializationsDiv.innerHTML = specializations
}

function fetchLanguages(currentLanguages){
    fetch("/api/blog-languages")
        .then(response => {
            return response.json()
        })
        .then(data => {
            const languages = data.languages
            let selectEl = document.querySelector("#edit-languages")
            let selectElHTML = selectEl.innerHTML
            for(let language of languages){
                selectElHTML += getLanguageOptionHtml(language)
            }
            selectEl.innerHTML = selectElHTML
        })
}

function fetchSpecializations(){
    fetch("/api/blog-specializations")
    .then(response => {
        return response.json()
    })
    .then(data => {
        const specializations = data.specializations
        let selectEl = document.querySelector("#edit-specializations")
        let selectElHTML = selectEl.innerHTML
        for(let specialization of specializations){
            selectElHTML += getSpecializationOptionHtml(specialization)
        }
        selectEl.innerHTML = selectElHTML
    })
}

function getLanguageOptionHtml(language){
    for(let curLang of defaultProfileData.languages){
        if (curLang.language == language.language){
            return "<option class='language-option' selected value='" + language.prefix + "'>" + language.language + "</option>"
        }
    }
    return "<option class='language-option' value='" + language.prefix + "'>" + language.language + "</option>"
}

function getSpecializationOptionHtml(specialization){
    for(let curSpec of defaultProfileData.specializations){
        if (curSpec.specialization == specialization.specialization){
            return "<option class='specialization-option' selected value='" + specialization.prefix + "'>" + specialization.specialization + "</option>"
        }
    }
    return "<option class='specialization-option' value='" + specialization.prefix + "'>" + specialization.specialization + "</option>"
}


