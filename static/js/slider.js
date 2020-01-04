
    var swiper = new Swiper('.swiper-container', {
      slideToClickedSlide: 'true',
      slidesPerView: 'auto', //auto
      spaceBetween: 10,
  // Responsive breakpoints
  breakpoints: {
    // when window width is >= 320px
    320: {
      slidesPerView: 2,
      spaceBetween: 10
    },
    // when window width is >= 480px
    480: {
      slidesPerView: 3,
      spaceBetween: 10
    },
    // when window width is >= 640px
    640: {
      slidesPerView: 4,
      spaceBetween: 10
    },
    // when window width is >= 860px
    860: {
      slidesPerView: 6,
      spaceBetween: 10
    }
  },
      
      pagination: {
        el: '.swiper-pagination',
        
      },
      navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
      },
      autoplay: {
          delay: 1500,
      },
    
    });
