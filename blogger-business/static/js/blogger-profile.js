function pullFullDataIntoHtml(){
    var image = document.querySelector('#upload-image-icon')
    image.src = defaultProfileData.image

    pullPersonalDataIntoHtml()

    pullBlogDataIntoHtml()

    pullStatisticsIntoHtml()

    fetchLanguages()
    fetchSpecializations()
}

function pullPersonalDataIntoHtml(){
    var blog_name = document.querySelector("#blog_name")
    blog_name.innerHTML = defaultProfileData.blog_name

    var country = document.querySelector("#country")
    var city = document.querySelector("#city")
    country.innerHTML = defaultProfileData.location.country
    city.innerHTML = defaultProfileData.location.city

    var birthday = document.querySelector("#birthday")
    birthday.innerHTML = defaultProfileData.birthday

}

function pullBlogDataIntoHtml(){
    putLanguagesDivsIntoHtml("languages")

    putSpecializationsDivsIntoHtml("specializations")

    var phone = document.querySelector("#phone")
    phone.innerHTML = defaultProfileData.phone

    var email = document.querySelector("#email")
    email.innerHTML = defaultProfileData.email

    if (defaultProfileData.email_activation){
        addEmailActivationMark()
    } else {
        emailActivationDiv = document.querySelector(".email-activation")
        emailActivationDiv.innerHTML = ''
    }
}

function pullStatisticsIntoHtml(){
    if (!defaultProfileData.youtube){
        googleAccountIsNotConnected()
    } else if (!defaultProfileData.youtube.channel_id){
        youtubeChannelDoesNotExist()
    } else {
        youtubeIsConnected()
        pullYoutubeStatisticsIntoHtml()
    }
}

function googleAccountIsNotConnected(){
    let youtubeStats = document.querySelector("#youtube-statistics")
    if (!youtubeStats.classList.contains("disabled-block")){
        youtubeStats.classList.add("disabled-block")
    }

    let youtubeLinkDiv = document.querySelector("#youtube-link-div")
    youtubeLinkDiv.innerHTML = '<div class="statistics-title-link no-hover-link">' +
                                    '<svg class="statistics-title-icon youtube">' +
                                        '<use xlink:href="#youtube"></use>' +
                                    '</svg>' +
                                    '<div class="statistics-title-text">youtube</div>' +
                                '</div>'

    let googleIsNotConnected = document.querySelector("#google-is-not-connected")
    if (googleIsNotConnected.classList.contains("d-none")){
        googleIsNotConnected.classList.remove("d-none")
    }

    let youtubeDoesNotExist = document.querySelector("#youtube-does-not-exist")
    if (!youtubeDoesNotExist.classList.contains("d-none")){
        youtubeDoesNotExist.classList.add("d-none")
    }

    let youtubeTotalStatistics = document.querySelector("#youtube-total-statistics")
    if (!youtubeTotalStatistics.classList.contains("d-none")){
        youtubeTotalStatistics.classList.add("d-none")
    }

    let youtubeMonthStatistics = document.querySelector("#youtube-month-statistics")
    if (!youtubeMonthStatistics.classList.contains("d-none")){
        youtubeMonthStatistics.classList.add("d-none")
    }
}

function youtubeChannelDoesNotExist(){
    googleAccountIsNotConnected()
    
    let googleIsNotConnected = document.querySelector("#google-is-not-connected")
    if (!googleIsNotConnected.classList.contains("d-none")){
        googleIsNotConnected.classList.add("d-none")
    }

    let youtubeDoesNotExist = document.querySelector("#youtube-does-not-exist")
    if (youtubeDoesNotExist.classList.contains("d-none")){
        youtubeDoesNotExist.classList.remove("d-none")
    }
}

function youtubeIsConnected(){
    let youtubeStats = document.querySelector("#youtube-statistics")
    if (youtubeStats.classList.contains("disabled-block")){
        youtubeStats.classList.remove("disabled-block")
    }

    let youtubeLinkDiv = document.querySelector("#youtube-link-div")
    youtubeLink = defaultProfileData.youtube.url
    youtubeLinkDiv.innerHTML = '<a href="' + youtubeLink + '" add target="_blank" class="statistics-title-link">' +
                                    '<svg class="statistics-title-icon youtube">' +
                                        '<use xlink:href="#youtube"></use>' +
                                    '</svg>' +
                                    '<div class="statistics-title-text">youtube</div>' +
                                '</a>' +
                                '<button class="statistics-update-btn" onclick="updateStatistics()">' +
                                    '<svg class="statistics-update-btn-icon">' +
                                        '<use xlink:href="#refresh"></use>' +
                                    '</svg>' +
                                '</button>'

    let googleIsNotConnected = document.querySelector("#google-is-not-connected")
    if (!googleIsNotConnected.classList.contains("d-none")){
        googleIsNotConnected.classList.add("d-none")
    }

    let youtubeDoesNotExist = document.querySelector("#youtube-does-not-exist")
    if (!youtubeDoesNotExist.classList.contains("d-none")){
        youtubeDoesNotExist.classList.add("d-none")
    }

    let youtubeTotalStatistics = document.querySelector("#youtube-total-statistics")
    if (youtubeTotalStatistics.classList.contains("d-none")){
        youtubeTotalStatistics.classList.remove("d-none")
    }

    let youtubeMonthStatistics = document.querySelector("#youtube-month-statistics")
    if (youtubeMonthStatistics.classList.contains("d-none")){
        youtubeMonthStatistics.classList.remove("d-none")
    }
}

function pullYoutubeStatisticsIntoHtml(){
    statistics = defaultProfileData.youtube.statistics
    
    let youtubeSubscribers = document.querySelector("#youtube-subscribers")
    youtubeSubscribers.innerHTML = toShortenNumber(statistics.subscribers)

    let youtubeVideos = document.querySelector("#youtube-videos")
    youtubeVideos.innerHTML = toShortenNumber(statistics.total_video_count)

    let youtubeViews = document.querySelector("#youtube-views")
    youtubeViews.innerHTML = toShortenNumber(statistics.total_views)

    let youtubeMonthSubscribers = document.querySelector("#youtube-month-subscribers")
    youtubeMonthSubscribers.innerHTML = toShortenNumber(statistics.month_subscribers_gained)

    let youtubeMonthViews = document.querySelector("#youtube-month-views")
    youtubeMonthViews.innerHTML = toShortenNumber(statistics.month_views)
    
    let youtubeMonthComments = document.querySelector("#youtube-month-comments")
    youtubeMonthComments.innerHTML = toShortenNumber(statistics.month_comments)

    let youtubeMonthlikes = document.querySelector("#youtube-month-likes")
    youtubeMonthlikes.innerHTML = toShortenNumber(statistics.month_likes)

    let youtubeMonthDislikes = document.querySelector("#youtube-month-dislikes")
    youtubeMonthDislikes.innerHTML = toShortenNumber(statistics.month_dislikes)
}

function refreshChannelInfo(){
    let refreshBtn = document.querySelector(".refresh-btn")
    defaultInnerHtml = refreshBtn.innerHTML
    refreshBtn.innerHTML = 'Loading <i class="fas fa-spinner fa-spin"></i>'

    fetch("/api/youtube/refresh/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
                "Content-Type": "application/json"
            },
    }).then(response => {
            refreshBtn.innerHTML = defaultInnerHtml
            if (!response.ok) { 
                throw response
            }
            return response.json()
    }).then(data => {     
        data = JSON.parse(data)
        console.log(data)
        defaultProfileData.youtube = data
        youtubeIsConnected()
        pullYoutubeStatisticsIntoHtml()
    }).catch(error => {
        
    })
}

function updateStatistics(){
    let updateBtn = document.querySelector(".statistics-update-btn")
    defaultInnerHtml = updateBtn.innerHTML
    updateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>'
    fetch("/api/youtube/statistics/update/", {
        method: "POST",
        headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": "application/json"
        },
    }).then(response => {
        updateBtn.innerHTML = defaultInnerHtml
        if (!response.ok) { 
            throw response
        }
        return response.json()
    }).then(data => {     
        data = JSON.parse(data)
        console.log(data)
        defaultProfileData.youtube.statistics = data
        youtubeIsConnected()
        pullYoutubeStatisticsIntoHtml()
    }).catch(error => {
        console.log(error)
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
        defaultProfileData.location.country = data.location.country
        defaultProfileData.location.city = data.location.city
        defaultProfileData.birthday = data.birthday

        pullPersonalDataIntoHtml()
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
        defaultProfileData.specializations = data.specializations
        defaultProfileData.phone = data.phone
        defaultProfileData.email = data.email
        defaultProfileData.email_activation = data.email_activation

        fetchLanguages()
        fetchSpecializations()

        pullBlogDataIntoHtml()
    })
}

var languagesHtml;
var specializationsHtml;

function editPersonalInfo(){
    var blog_name = defaultProfileData.blog_name
    var country = defaultProfileData.location.country
    var city = defaultProfileData.location.city
    var birthday = defaultProfileData.birthday.split("-")
    var year = birthday[0]
    var month = birthday[1]
    var day = birthday[2]

    firstSelected = ""
    secondSelected = ""
    thirdSelected = ""
    fourthSelected = ""
    fifthSelected = ""
    sixthSelected = ""
    seventhSelected = ""
    eighthSelected = ""
    ninthSelected = ""
    tenthSelected = ""
    eleventhSelected = ""
    twelfthSelected = ""

    if (month == "01") {firstSelected = "selected"}
    else if (month == "02") {secondSelected = "selected"}
    else if (month == "03") {thirdSelected = "selected"}
    else if (month == "04") {fourthSelected = "selected"}
    else if (month == "05") {fifthSelected = "selected"}
    else if (month == "06") {sixthSelected = "selected"}
    else if (month == "07") {seventhSelected = "selected"}
    else if (month == "08") {eighthSelected = "selected"}
    else if (month == "09") {ninthSelected = "selected"}
    else if (month == "10") {tenthSelected = "selected"}
    else if (month == "11") {eleventhSelected = "selected"}
    else if (month == "12") {twelfthSelected = "selected"}
    
    $.confirm({
        title: 'Edit personal info',
        columnClass: "medium",
        content: '' +
        '<form action="" method="POST" class="formName" id="editPersonalForm">' +
            '<div class="form-group">' +
                '<label for="edit-blog-name">' +
                    '<i class="fas fa-exclamation-circle" data-toggle="tooltip" data-placement="top" title="This is a username field"></i>' +
                    'Your blog name:</label>' +
                '<input type="text" id="edit-blog-name" name="blog_name" value="' + blog_name + '" class="blog_name form-control" required data-toggle="username-popover" data-trigger="focus" data-placement="top"  data-content="Username is already taken" />' +
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
                    '<option value="1" ' + firstSelected+ '>Jan</option>' +
                    '<option value="2" ' + secondSelected+ '>Feb</option>' +
                    '<option value="3" ' + thirdSelected+ '>Mar</option>' +
                    '<option value="4" ' + fourthSelected+ '>Apr</option>' +
                    '<option value="5" ' + fifthSelected+ '>May</option>' +
                    '<option value="6" ' + sixthSelected+ '>Jun</option>' +
                    '<option value="7" ' + seventhSelected+ '>Jul</option>' +
                    '<option value="8" ' + eighthSelected+ '>Aug</option>' +
                    '<option value="9" ' + ninthSelected+ '>Sep</option>' +
                    '<option value="10" ' + tenthSelected+ '>Oct</option>' +
                    '<option value="11" ' + eleventhSelected+ '>Nov</option>' +
                    '<option value="12" ' + twelfthSelected+ '>Dec</option>' +
                '</select>' +
                '<select name="day" required class="day custom-select col-2" id="day-selector">' +
                    '<option value="' + day + '" selected>' + day + '</option>' +
                '</select>' +
                '<select name="year" required onchange="enterDay()" class="year custom-select col-2" id="year-selector">' +
                '<option value="' + year + '" selected>' + year + '</option>' +
                '</select>' +
            '</div>' +
        '</form>',
        buttons: {
            submit: {
                text: 'Submit',
                btnClass: 'btn-blue',
                action: function () {
                    send(this)
                    async function send(that){

                        var editPersonalForm = document.querySelector("#editPersonalForm")
                        var oReq = new XMLHttpRequest()
                        
                        var oData = new FormData(editPersonalForm)
                        
                        oReq.open("POST", "/api/blogger-profile-data/personal/edit/", true)
                        oReq.setRequestHeader('X-CSRFToken', csrftoken)
                        
                        username = editPersonalForm.elements.namedItem("blog_name").value
                        if (defaultProfileData.blog_name != username){
                            usernameExists = await username_check(username)
                            if (usernameExists){
                                $('[data-toggle="username-popover"]').popover("show")
                                return false
                            }
                        }
                        
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
                        that.close()
                        firstEntering = true
                    }
                    return false
                }
            },
            cancel: function () {
                firstEntering = true
                $('[data-toggle="username-popover"]').popover("hide")
            },
        },
        onContentReady: function () {
            // bind to events
            enterDay()
            var jc = this;

            form = this.$content.find('form')

            this.$content.find('form').on('submit', function (e) {
                // if the user submits the form by pressing enter in the field.
                e.preventDefault();

                jc.$$formSubmit.trigger('click'); // reference the button and click it
            });

            $('[data-toggle="tooltip"]').tooltip()

            document.querySelector("#edit-blog-name").onfocus = function(e){
                $('[data-toggle="username-popover"]').popover("hide")
            }
        }
    })
}

function editBlogInfo(){
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
                    languagesHtml+
                '</select>' +
            '</div>' +
            '<div class="form-group">' +
                '<label for="edit-specializations">Specializations of blog (max 3):</label>' +
                '<select id="edit-specializations" required name="specializations" multiple class="specializations custom-select col-4">' +
                    specializationsHtml +
                '</select>' +
            '</div>' +
            '<div class="form-group">' +
                '<label for="edit-phone">Your phone:</label>' +
                '<input type="text" id="edit-phone" name="phone" value="' + phone + '" class="form-control" required />' +
            '</div>' +
            '<div class="form-group">' +
                '<label for="edit-email">' +
                    '<i class="fas fa-exclamation-circle" data-toggle="tooltip" data-placement="top" title="You will need to confirm the new email address"></i>' +    
                    'Your email:' +
                '</label>' +
                '<input type="text" id="edit-email" name="email" value="' + email + '" class="form-control" required data-toggle="email-popover" data-trigger="focus" data-placement="top"  data-content="Email is already taken" />' +
            '</div>' +
        '</form>',
        buttons: {
            formSubmit: {
                text: 'Submit',
                btnClass: 'btn-blue',
                action: function () {
                    send(this)
                    async function send(that){

                        var editBlogForm = document.querySelector("#editBlogForm")
                        
                        var oData = new FormData(editBlogForm)
                    
                        var oReq = new XMLHttpRequest()
                        oReq.open("POST", "/api/blogger-profile-data/blog/edit/", true)
                        oReq.setRequestHeader('X-CSRFToken', csrftoken)
                        
                        email = editBlogForm.elements.namedItem("email").value
                        if (defaultProfileData.email != email){
                            emailExists = await email_check(email)
                            if (emailExists){
                                $('[data-toggle="email-popover"]').popover("show")
                                return false
                            }
                        }

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
                                        action: function(){}
                                        },
                                    }
                                })
                            }
                        };
                        oReq.send(oData)
                        that.close()
                    }
                    return false
                }
            },
            cancel: function () {
                $('[data-toggle="email-popover"]').popover("hide")
            },
        },
        onContentReady: function () {
            // bind to events
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

            $('[data-toggle="tooltip"]').tooltip()

            document.querySelector("#edit-email").onfocus = function(e){
                $('[data-toggle="email-popover"]').popover("hide")
            }
        }
    })
}

firstEntering = true

function enterDay(){
    kcyear = document.getElementsByName("year")[0],
    kcmonth = document.getElementsByName("month")[0],
    kcday = document.getElementsByName("day")[0];
        
    var birthday = defaultProfileData.birthday.split("-")
    var year = birthday[0]
    var month = birthday[1]
    var day = birthday[2]

    var d = new Date();
    var n = d.getFullYear();
    if (firstEntering){
        kcyear.innerHTML = ""
    }
    for (var i = n; i >= 1950; i--) {
        var opt = new Option();
        opt.value = opt.text = i;
        if (firstEntering && opt.value == year){
            opt.selected = true
        }
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
            if ((firstEntering && i == day) || i == d){
                opt.selected = true
            }
            kcday.add(opt);
        }
    }
    validate_date();
    firstEntering = false
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
        languages += "<div class='block-item language'>" + language.language + "</div>"
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
            languages = data.languages
            selectHtml = ""
            for(let language of languages){
                selectHtml += getLanguageOptionHtml(language)
            }
            languagesHtml = selectHtml
        })
}

function fetchSpecializations(){
    fetch("/api/blog-specializations")
    .then(response => {
        return response.json()
    })
    .then(data => {
        specializations = data.specializations
        selectHtml = ""
        for(let specialization of specializations){
            selectHtml += getSpecializationOptionHtml(specialization)
        }
        specializationsHtml = selectHtml
    })
}

function putLanguagesDivsIntoEditHtml(){
    select = document.querySelector("#edit-languages")
    select.innerHTML = languagesHtml
}

function putSpecializationsDivsIntoEditHtml(){
    select = document.querySelector("#edit-specializations")
    select.innerHTML = languagesHtml
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

