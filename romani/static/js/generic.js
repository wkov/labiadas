var didScroll;
var lastScrollTop = 0;
var delta = 5;
var navbarHeight = $('header').outerHeight();

$(window).scroll(function(event){
    didScroll = true;
});

setInterval(function() {
    if (didScroll) {
        hasScrolled();
        didScroll = false;
    }
}, 250);

function hasScrolled() {
    var st = $(this).scrollTop();

    // Make sure they scroll more than delta
    if(Math.abs(lastScrollTop - st) <= delta)
        return;

    // If they scrolled down and are past the navbar, add class .nav-up.
    // This is necessary so you never see what is "behind" the navbar.
    if (st > lastScrollTop && st > navbarHeight){
        // Scroll Down
        $('header').removeClass('nav-down').addClass('nav-up');
    } else {
        // Scroll Up
        if(st + $(window).height() < $(document).height()) {
            $('header').removeClass('nav-up').addClass('nav-down');
        }
    }

    lastScrollTop = st;
}

$( document ).ready(function() {

    <!-- Script per oucultar el menu -->
    $("#menu-toggle").click(function(e) {
        e.preventDefault();
        /*USO CON STATIC/CSS/simple-sidebar.css*/
        $("#wrapper").toggleClass("toggled");
        var $this = $(this).toggleClass('toggled');
        if($(this).hasClass('toggled')){
            $(this).text('>');
        } else {
            $(this).text('<');
        }
    });

    $("#busk-toggle").click(function(e) {
        e.preventDefault();
        $("#div_bsk_extend").toggle();
    });


    $("#convidar").submit(function(){

         $.post("/convidar/", $(this).serializeArray(),function(data){
        });



    })
 });

///*Script per Notificacións */
//function CallNotification(msg,type, position,width,height, multiline, time){
//    position = position || "center";
//    type = type || "info";
//    multiline = multiline || "true";
//    time = time || 9000000;
//    //width = width || "all";
//    height = height || 80;
//
//    notif({
//        msg: msg,
//        type: type,
//        position: position,
//        multiline : multiline,
//        time: time,
//        //width: width
//
//    });
//}


