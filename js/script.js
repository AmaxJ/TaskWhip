//protect global scope
!function($, window, document){
    //when document is ready
    $(function(){
        "use strict"
        //cache selections
        var $window = $(window),
            $introTag = $("#tag-one"),
            $introMention = $("#tag-two"),
            $whyUs = $("#why-us"),
            $header = $("#main-header"),
            $icons = $(".icon"),
            $firstTwo = $("#first-two");

        //flags
        var iconsJumped = false;

        //Main banner text animations
        $introTag.fadeIn(1500);
        $introMention.delay(1000).fadeIn(1400);

        $window.scroll(scrollAnimations);

        function scrollAnimations() {
            var icon_div = $whyUs.offset().top - 400,
                reset_div = $firstTwo.offset.top - 400;
            //fade navbar if not at top of page
            if ($window.scrollTop() !== 0) {
                $header.fadeOut(1000);
            } else {
                $header.fadeIn(500);
            }
            if($window.scrollTop() > icon_div && !iconsJumped) {
                bounceIcons();
                iconsJumped = true;
            }
        }

        function bounceIcons() {
            $icons.each(function(index){
                $(this).delay(1000).addClass('grow');
            });
        }

    });
}(window.jQuery, window, document);