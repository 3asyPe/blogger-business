function fetchData(){
    fetch("/api/blogger-profile-data/")
    .then(response => {
        return response.json()
    })
    .then(data => {
        data = JSON.parse(data)
        console.log(data)
        var image = document.querySelector('#upload-image-icon');
        image.src = data.image

        var blog_name = document.querySelector("#blog_name")
        blog_name.innerHTML = data.blog_name

        var location = document.querySelector("#location")
        location.innerHTML = "Location: " + data.location.country + ", " + data.location.city

        var birthday = document.querySelector("#birthday")
        birthday.innerHTML = "Birthday: " + data.birthday

        var languagesDiv = document.querySelector("#languages")
        var languages = ""
        for(const language of data.languages){
            languages += "<div class='block-item'>" + language.language + "</div>"
        }
        languagesDiv.innerHTML = languages

        var specializationsDiv = document.querySelector("#specializations")
        var specializations = ""
        for(const specialization of data.specializations){
            specializations += "<div class='block-item'>" + specialization.specialization + "</div>"
        }
        specializationsDiv.innerHTML = specializations

        var phone = document.querySelector("#phone")
        phone.innerHTML = data.phone

        var email = document.querySelector("#email")
        email.innerHTML = data.email
    })
}

fetchData()

function previewImage(event){
    var reader = new FileReader();
    reader.onload = function() {
        var output = document.querySelector('#upload-image-icon');
        output.src = reader.result;
    }
    reader.readAsDataURL(event.target.files[0]);
}

function editPersonalInfo(){
    $.confirm({
        title: 'Prompt!',
        content: '' +
        '<form action="" class="formName">' +
        '<div class="form-group">' +
        '<label>Enter something here</label>' +
        '<input type="text" placeholder="Your name" class="name form-control" required />' +
        '</div>' +
        '</form>',
        buttons: {
            formSubmit: {
                text: 'Submit',
                btnClass: 'btn-blue',
                action: function () {
                    var name = this.$content.find('.name').val();
                    if(!name){
                        $.alert('provide a valid name');
                        return false;
                    }
                    $.alert('Your name is ' + name);
                }
            },
            cancel: function () {
                //close
            },
        },
        onContentReady: function () {
            // bind to events
            var jc = this;
            this.$content.find('form').on('submit', function (e) {
                // if the user submits the form by pressing enter in the field.
                e.preventDefault();
                jc.$$formSubmit.trigger('click'); // reference the button and click it
            });
        }
    });
}