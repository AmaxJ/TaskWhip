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
            var icon_div = $whyUs.offset().top - 400;
            //fade navbar if not at top of page
            if ($window.scrollTop() !== 0) {
                $header.fadeOut(1000);
            } else {
                $header.fadeIn(500);
            }
            if($window.scrollTop() > icon_div && !iconsJumped) {
                transformIcons(true);
                iconsJumped = true;
            } else if ($window.scrollTop() < icon_div && iconsJumped) {
                transformIcons();
                iconsJumped = false;
            }
        }

        function transformIcons(flag) {
            if (flag) {
                $icons.each(function(index){
                    $(this).addClass('grow');
                });
            } else {
                $icons.each(function() {
                    $(this).removeClass('grow');
                });
            }
        }

    });
}(window.jQuery, window, document);