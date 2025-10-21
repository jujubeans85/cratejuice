// Crate Juice v3 - Main Application Script

// Backend API configuration
const API_CONFIG = {
    baseUrl: window.location.hostname === 'localhost' 
        ? 'http://localhost:5000' 
        : 'https://cratejuice-backend.onrender.com',
    endpoints: {
        health: '/api/health',
        features: '/api/features',
        info: '/api/info'
    }
};

// API utility functions
async function fetchAPI(endpoint) {
    try {
        const response = await fetch(`${API_CONFIG.baseUrl}${endpoint}`);
        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`Failed to fetch ${endpoint}:`, error);
        return null;
    }
}

// Load features from backend
async function loadFeaturesFromBackend() {
    const data = await fetchAPI(API_CONFIG.endpoints.features);
    if (data && data.features) {
        const featureGrid = document.querySelector('.feature-grid');
        if (featureGrid) {
            featureGrid.innerHTML = data.features.map(feature => `
                <div class="feature-card">
                    <h4>${feature.icon} ${feature.name}</h4>
                    <p>${feature.description}</p>
                </div>
            `).join('');
            
            // Re-attach hover effects
            attachFeatureCardEffects();
        }
    }
}

// Load app info from backend
async function loadAppInfo() {
    const data = await fetchAPI(API_CONFIG.endpoints.info);
    if (data) {
        console.log('App Info:', data);
        // Update page title if needed
        if (data.name) {
            document.querySelector('header h1').textContent = `🧃 ${data.name} v${data.version}`;
        }
    }
}

// Check backend health
async function checkBackendHealth() {
    const health = await fetchAPI(API_CONFIG.endpoints.health);
    if (health && health.status === 'healthy') {
        console.log('✅ Backend is healthy');
        return true;
    } else {
        console.warn('⚠️ Backend is not available, using static content');
        return false;
    }
}

document.addEventListener('DOMContentLoaded', async function() {
    console.log('🧃 Crate Juice v3 Loaded!');
    
    // Check backend and load dynamic content
    const backendAvailable = await checkBackendHealth();
    if (backendAvailable) {
        await loadAppInfo();
        await loadFeaturesFromBackend();
    }
    
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
    attachFeatureCardEffects();
});

// Function to attach hover effects to feature cards
function attachFeatureCardEffects() {
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.background = 'linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.background = '#f8f9fa';
        });
    });
}
