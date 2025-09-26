// Navigation Test Script for Semantic Self-Aware Kit
// Validates all navigation links are functional

document.addEventListener('DOMContentLoaded', function() {
    console.log('🧠 Semantic Self-Aware Kit - Navigation Test');
    
    // Test all navigation links
    const navLinks = [
        'components.html',
        'protocols.html', 
        'sovereign-ai.html',
        'documentation.html'
    ];
    
    navLinks.forEach(link => {
        fetch(link)
            .then(response => {
                if (response.ok) {
                    console.log(`✅ ${link} - OK`);
                } else {
                    console.log(`❌ ${link} - Error: ${response.status}`);
                }
            })
            .catch(error => {
                console.log(`❌ ${link} - Network Error: ${error}`);
            });
    });
    
    // Highlight active navigation
    const currentPage = window.location.pathname.split('/').pop();
    const navItems = document.querySelectorAll('nav a');
    
    navItems.forEach(item => {
        if (item.getAttribute('href') === currentPage) {
            item.classList.add('nav-active');
        }
    });
    
    console.log('Navigation test complete.');
});