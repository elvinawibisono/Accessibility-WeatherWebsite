$(document).ready(function(){
    $('#country').change(function(){
        var countryName =$('#country option:selected').text();
        $.ajax({
            url: '/load',
            data: {countryName: countryName},
            type: 'POST', 
            success: function(response){
                console.log(response); 

            }, 
            error: function(error){
                console.log(error); 
            }
        })
    });
});

