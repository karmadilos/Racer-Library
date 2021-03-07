$(".right-arrow").click(function() {

    var curSlide = $("#photo .slide.active");
    var nextSlide = curSlide.next();

    var curText = $("#recommend_info .slide.active");
    var nextText = curText.next();

    curSlide.fadeOut().removeClass("active");
    nextSlide.fadeIn().addClass("active");

    curText.removeClass("active");
    nextText.addClass("active");

    if( nextSlide.length === 0 ) {
        $("#photo .slide").first().fadeIn().addClass("active");
    }

    if( nextText.length === 0 ) {
        $("#recommend_info .slide").first().addClass("active");
    }
});


$(".left-arrow").click(function() {

    var curSlide = $("#photo .slide.active");
    var prevSlide = curSlide.prev();

    var curText = $("#recommend_info .slide.active");
    var prevText = curText.prev();

    curSlide.fadeOut().removeClass("active");
    prevSlide.fadeIn().addClass("active");

    curText.removeClass("active");
    prevText.addClass("active");

    if( prevSlide.length === 0 ) {
        $("#photo .slide").last().fadeIn().addClass("active");
    }

    if( prevText.length === 0 ) {
        $("#recommend_info .slide").first().addClass("active");
    }
});
