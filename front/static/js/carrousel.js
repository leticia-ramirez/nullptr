$(document).ready(function() {
    $('.owl-carousel').owlCarousel({
        // loop:false,
        autoplay:false,
        autoplayhoverpause:true,
        autoplaytimeout:30,
        items:4,
        margin:5,
        padding:5,
        stagePadding:5,
        responsiveClass:true,
        center:true,
        nav:true,
        navigation: true,
        navigationText: ['«', '»'],
        responsive:{
            0: {
                items:1,
                dots:false
            },
            485: {
                items:2,
                dots:false
            },
            728: {
                items:3,
                dots:false
            },
            960: {
                items:3,
                dots:false
            },
            1200: {
                items:3,
                dots:false
            }

        }
        
    });
  })
alert(hola)