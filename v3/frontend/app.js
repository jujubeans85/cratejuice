// Crate Juice v3 - Main Application Script

document.addEventListener('DOMContentLoaded', function() {
    console.log('🧃 Crate Juice v3 Loaded!');
    
    // Demo button functionality
    const demoBtn = document.getElementById('demoBtn');
    const messageEl = document.getElementById('message');
    
    const messages = [
        '🎉 Welcome to Crate Juice!',
        '✨ The framework is working perfectly!',
        '🚀 Ready to build something amazing?',
        '💡 Your ideas start here!',
        '🌟 Making web development fun again!'
    ];
    
    let messageIndex = 0;
    
    demoBtn.addEventListener('click', function() {
        messageEl.textContent = messages[messageIndex];
        messageIndex = (messageIndex + 1) % messages.length;
        
        // Add animation
        messageEl.style.animation = 'none';
        setTimeout(() => {
            messageEl.style.animation = 'fadeInUp 0.5s ease';
        }, 10);
    });
    
    // Add smooth scroll behavior
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Feature card hover effects
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.background = 'linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.background = '#f8f9fa';
        });
    });
});
