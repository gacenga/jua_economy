document.addEventListener('DOMContentLoaded', function() {
    var navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    var navbarCollapse = document.getElementById('navbarNav');
  
    navLinks.forEach(function(link) {
      link.addEventListener('click', function() {
        if (navbarCollapse.classList.contains('show')) {
          var bootstrapCollapse = new bootstrap.Collapse(navbarCollapse, {
            toggle: false
          });
          bootstrapCollapse.hide();
        }
      });
    });
  });
