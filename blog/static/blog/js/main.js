// Main JavaScript file for The Byline website

document.addEventListener('DOMContentLoaded', function() {
    console.log('The Byline website loaded successfully!');
    
    // Initialize custom functionality
    initScrollAnimations();
    initMobileMenu();
    initSearchFunctionality();
    initNavbarBehavior();
});

// Scroll animations
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fadeIn');
            }
        });
    }, observerOptions);
    
    // Observe elements with animation classes
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });
}

// Mobile menu functionality
function initMobileMenu() {
    const mobileMenuToggle = document.querySelector('[data-mobile-menu-toggle]');
    const mobileMenu = document.querySelector('[data-mobile-menu]');
    
    if (mobileMenuToggle && mobileMenu) {
        mobileMenuToggle.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
            mobileMenuToggle.setAttribute('aria-expanded', 
                mobileMenu.classList.contains('hidden') ? 'false' : 'true'
            );
        });
    }
}

// Search functionality
function initSearchFunctionality() {
    const searchInput = document.querySelector('[data-search-input]');
    const searchResults = document.querySelector('[data-search-results]');
    
    if (searchInput && searchResults) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            if (query.length > 2) {
                searchTimeout = setTimeout(() => {
                    performSearch(query);
                }, 300);
            } else {
                searchResults.classList.add('hidden');
            }
        });
    }
}

// Perform search (placeholder function)
function performSearch(query) {
    // This would typically make an AJAX request to your search endpoint
    console.log('Searching for:', query);
    
    // For now, just show the search results container
    const searchResults = document.querySelector('[data-search-results]');
    if (searchResults) {
        searchResults.classList.remove('hidden');
        // Add your search logic here
    }
}

// Newsletter subscription
function initNewsletterSubscription() {
    const newsletterForm = document.querySelector('[data-newsletter-form]');
    
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = this.querySelector('[data-email-input]').value;
            if (email) {
                subscribeToNewsletter(email);
            }
        });
    }
}

// Newsletter subscription function (placeholder)
function subscribeToNewsletter(email) {
    console.log('Subscribing email:', email);
    // Add your newsletter subscription logic here
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function initNavbarBehavior() {
  const navbar = document.getElementById('cat-navbar'); 
  if (navbar) {
    let lastScrollTop = 0;
    const scrollThreshold = 192.864;
    
    navbar.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
    navbar.style.transform = 'translateY(0)';
    navbar.style.opacity = '1';

    window.addEventListener('scroll', function() {
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      
      if (scrollTop > scrollThreshold) {
        navbar.style.position = 'fixed';
        navbar.style.top = '0';
        navbar.style.left = '0';
        navbar.style.right = '0';
        navbar.style.width = '100%';
        navbar.style.transform = 'translateY(0)';
        navbar.style.opacity = '1';
        navbar.style.boxShadow = '0 4px 20px 0px rgb(0 0 0 / 0.25)';
      } else {
        navbar.style.position = 'sticky';
        navbar.style.top = '0';
        navbar.style.transform = 'translateY(0)';
        navbar.style.opacity = '1';
        navbar.style.boxShadow = '6px 4px 20px 0px rgb(0 0 0 / 0.20)';
      }
      
      lastScrollTop = scrollTop;
    });
  }
}

// Export functions for use in other scripts
window.TheByline = {
    initScrollAnimations,
    initMobileMenu,
    initSearchFunctionality,
    initNewsletterSubscription,
    initNavbarBehavior
};
