$(document).ready(function(){
    var form = $('#user-info');
    console.log(form);


    const handleAlerts = (type, text) =>{
        alertBox.innerHTML = `<div class="alert alert-${type}" role="alert">
                            ${text}
                        </div>`
    }
    const alertBox = document.getElementById('alert-box')

    function updateProfile(){
        var data = {};

        data["username"] = document.getElementById("id_username").value;
        data["email"] = document.getElementById("id_email").value;
        data["phone"] = document.getElementById("id_phone").value;
        data["gender"] = document.getElementById("id_gender").value;
        data["image"] = document.getElementById("id_image").files[0];
        data["birth_date_month"] = document.getElementById("id_birth_date_month").value;
        data["birth_date_day"] = document.getElementById("id_birth_date_day").value;
        data["birth_date_year"] = document.getElementById("id_birth_date_year").value;

        var csrf_token = $('#user-info [name="csrfmiddlewaretoken"]').val();

        data["csrfmiddlewaretoken"] = csrf_token;

        var url = form.attr("action");

        console.log(data);

        $.ajax({
            url: url,
            type: 'POST',
            enctype: 'multipart/form-data',
            data: data,
            success: function (response) {
                document.getElementById("profile-username").textContent = data["username"];
                document.getElementById("title-username").textContent = data["username"];
                document.getElementById("title-email").textContent = data["email"];

                handleAlerts("success", "Your account has been updated successfully!")
                console.log(response);
            },
            error: function(error){
                console.log(error)
                handleAlerts("danger", "Try again")
            },
            cache: false
        });
    }

    form.on('submit', function(e){
        e.preventDefault();
        updateProfile();
    });

});