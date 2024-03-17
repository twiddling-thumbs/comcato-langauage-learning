/**
  * Parallax
  * pageLoad
  * flatOwlCarowsel
  * flatIsotopeCase
  * searchIcon
  * popupVideo
  * FlMenu
*/

;(function($) {

    "use strict";

    var isMobile = {
        Android: function() {
            return navigator.userAgent.match(/Android/i);
        },
        BlackBerry: function() {
            return navigator.userAgent.match(/BlackBerry/i);
        },
        iOS: function() {
            return navigator.userAgent.match(/iPhone|iPad|iPod/i);
        },
        Opera: function() {
            return navigator.userAgent.match(/Opera Mini/i);
        },
        Windows: function() {
            return navigator.userAgent.match(/IEMobile/i);
        },
        any: function() {
            return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
        }
    };

    var Parallax = function() {
        if ( $().parallax && isMobile.any() == null ) {
            $('.parallax-1').parallax("50%", 0.1);
            $('.parallax-3').parallax("50%", 0.1);
            $('.parallax-4').parallax("50%", 0.1);          
        }
    };

    var pageLoad = function () {
        $( window ).on('load',function() {
            $('#preload').delay(1000).fadeOut('fast', function () {
                $('body').removeClass('preloading');
            });
        });
    }

    var flatOwlCarowsel = function() {
        if ( $().owlCarousel ) {
            $('.themesflat-carousel').each(function(){
                var
                $this = $(this),
                auto = $this.data("auto"),
                item = $this.data("item"),
                item2 = $this.data("item2"),
                item3 = $this.data("item3"),
                item4 = $this.data("item4"),
                margin = Number($this.data("margin"));

                $this.find('.owl-carousel').owlCarousel({
                    margin: margin,
                    navigation : false,
                    pagination: false,
                    autoplay: auto,
                    items: 2,   
                    loop:true,
                    nav: false,
                    dots: true,
                    dotsData: true,
                    animateOut:'fadeOut',
                    autoplayTimeout: 10000,
                    responsive: {
                        0:{
                            items:item4
                        },
                        600:{
                            items:item3
                        },
                        1000:{
                            items:item2
                        },
                        1752:{
                            items:item
                        }
                    }
                });
            });
        }
    };
    
    var flatIsotopeCase = function() {
        $(".fl-isotope").each(function () {
            if ( $().isotope ) {           
                var $container = $('.isotope-gl');
                $('.flat-filter-isotope li').on('click',function() {                           
                    var selector = $(this).find("a").attr('data-filter');
                    $('.flat-filter-isotope li').removeClass('active');
                    $(this).addClass('active');
                    $container.isotope({ filter: selector });
                    return false;
                });
            };
        });         
    };

    var popupVideo = function () {
        if ($().magnificPopup) {
            $('.popup-video').magnificPopup({
                type: 'iframe',
                mainClass: 'mfp-fade',
                removalDelay: 160,
                preloader: false,
                fixedContentPos: false
            });
        }
    }

    var searchIcon = function () {
        $(document).on('click', function(e) {   
            var clickID = e.target.id;   
            if ( ( clickID !== 'input-search' ) ) {
                $('.header-search-form').removeClass('show');                
            } 
        });

        $('.header-search-icon').on('click', function(event){
            event.stopPropagation();
        });

        $('.header-search-form').on('click', function(event){
            event.stopPropagation();
        });        

        $('.header-search-icon').on('click', function (event) {
            if(!$('.header-search-form').hasClass( "show" )) {
                $('.header-search-form').addClass('show');  
                event.preventDefault();                
            }
                
            else
                $('.header-search-form').removeClass('show');
                event.preventDefault();

        });        
  
    };

    var FlMenu = function () {
        $(".navigation-side-menu").add('.header-nav-toggle-btn').on("click", function () {
            $(".side-menu__block").addClass("active");
        });

        $(".side-menu__block-overlay,.side-menu__toggler, .scrollToLink").on(
            "click",
            function (e) {
                $(".side-menu__block").removeClass("active");
                e.preventDefault();
            }
        );
    }

    // Dom Ready
    $(function() {
        flatIsotopeCase();
        popupVideo();
        searchIcon();
        FlMenu();
        $( window ).on('load',function() {
            Parallax();
            flatOwlCarowsel();
        });

        pageLoad();
    });

})(jQuery);
