$(document).ready(function(){
    function addToCart(){
        $.ajax({
            url: url,
            type: 'GET',
            cache: true,
            success: function (data) {
                console.log("OK");
            },
            error: function(){
                console.log("error")
            }
        })
    }
});