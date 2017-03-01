// navbar autoscroll and coloring
+function ($) {
  $(document).ready(function(){
    $(window).scroll(function() { // check if scroll event happened
      if ($(document).scrollTop() > 300) { // check if user scrolled more than 50 from top of the browser window
        $("nav.navbar-wrapper.navbar-fixed-top").css("background-color", "black"); // if yes, then change the color of class "navbar-fixed-top" to white (#f8f8f8)
        $(".container-2 input#search").css("background-color", "#333");
      } else {
        $("nav.navbar-wrapper.navbar-fixed-top").css("background-color", "transparent"); // if not, change it back to transparent
        $(".container-2 input#search").css("background-color", "transparent");
      }
    });
  });
}(jQuery);
