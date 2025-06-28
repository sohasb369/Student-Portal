
  $(document).ready(function() {
    // Initialize video player
    const player = new Plyr('#plyr-video-player');
    
    // Initialize perfect scrollbar for menu
    const ps = new PerfectScrollbar('#layout-menu', {
      wheelSpeed: 2,
      wheelPropagation: true,
      minScrollbarLength: 20
    });
    
    // Toggle menu on mobile
    $('.layout-menu-toggle').on('click', function() {
      $('.layout-menu').toggleClass('layout-menu-expanded');
      $('.layout-overlay').toggleClass('show');
    });
    
    // Close menu when clicking overlay
    $('.layout-overlay').on('click', function() {
      $('.layout-menu').removeClass('layout-menu-expanded');
      $(this).removeClass('show');
    });
    
    // Initialize submenu toggles
    $('.menu-toggle').on('click', function(e) {
      e.preventDefault();
      const $parent = $(this).parent('.menu-item');
      $parent.siblings().removeClass('active').find('.menu-sub').slideUp();
      $parent.toggleClass('active');
      $parent.find('.menu-sub').slideToggle();
    });
    
    // Theme switcher functionality
    function setTheme(theme) {
      $('html').attr('data-theme', theme);
      localStorage.setItem('theme', theme);
      
      // Update UI
      if (theme === 'dark') {
        $('.light-icon').hide();
        $('.dark-icon').show();
        $('.theme-item[data-theme="dark"]').addClass('active');
        $('.theme-item[data-theme="light"]').removeClass('active');
      } else {
        $('.light-icon').show();
        $('.dark-icon').hide();
        $('.theme-item[data-theme="light"]').addClass('active');
        $('.theme-item[data-theme="dark"]').removeClass('active');
      }
    }
    
    // Handle theme selection
    $('.theme-item').on('click', function() {
      const theme = $(this).data('theme');
      setTheme(theme);
    });
    
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
  });

  