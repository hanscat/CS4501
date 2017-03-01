$(document).ready(function(){
    $(window).scroll(function(){
        if($(window).scrollTop() > $(window).height()){
            $(".menu").css({"background-color":"transparent"});
        }
        else{
            $(".menu").css({"background-color":"black"});
        }

    })
})
