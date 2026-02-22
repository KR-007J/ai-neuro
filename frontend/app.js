// NeuroLearn AI - Dashboard Interactivity

// API Base URL
const API_BASE_URL = 'https://ai-neuro-1.onrender.com';

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    initializeNavigation();
    initializeAnimations();
    loadUserData();
});

// Navigation handling
function initializeNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Remove active from all items
            navItems.forEach(nav => nav.classList.remove('active'));
            
            // Add active to clicked item
            item.classList.add('active');
            
            // Get the target page
            const href = item.getAttribute('href');
            navigateToPage(href);
        });
    });
}

// Page navigation
function navigateToPage(page) {
    // Smooth scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
    
    // You can add page transitions here
    console.log('Navigating to:', page);
}

// Initialize scroll animations
function initializeAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1
    });

    // Observe all cards
    document.querySelectorAll('.card, .stat-card').forEach(card => {
        observer.observe(card);
    });
}

// Load user data from API
async function loadUserData() {
    try {
        // Example: Load user stats
        // const response = await fetch(`${API_BASE_URL}/users/demo_user_123`);
        // const data = await response.json();
        // updateDashboard(data);
        
        console.log('User data loaded');
    } catch (error) {
        console.error('Error loading user data:', error);
    }
}

// Update dashboard with user data
function updateDashboard(data) {
    // Update stats cards
    // Update progress bars
    // Update recommendations
}

// Simulate API call for recommendations
async function getRecommendations(userId) {
    try {
        const response = await fetch(`${API_BASE_URL}/adaptation/recommend-content`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: userId,
                user_profile: {
                    user_id: userId,
                    learning_style: 'visual',
                    cognitive_load_capacity: 7.5
                },
                performance_history: [0.75, 0.78, 0.82],
                completed_content: []
            })
        });
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching recommendations:', error);
        return null;
    }
}

// Smooth progress bar animations
function animateProgressBars() {
    const progressFills = document.querySelectorAll('.progress-fill');
    
    progressFills.forEach(fill => {
        const width = fill.style.getPropertyValue('--width');
        fill.style.width = '0%';
        
        setTimeout(() => {
            fill.style.width = width;
        }, 100);
    });
}

// Call on page load
setTimeout(animateProgressBars, 500);

// Export data functionality
document.querySelector('.btn-secondary')?.addEventListener('click', async () => {
    alert('Export functionality - Coming soon!');
    // Implement actual export logic here
});

// Start learning button
document.querySelector('.btn-primary')?.addEventListener('click', () => {
    alert('Starting next lesson...');
    // Navigate to learning module
});

// Add click handlers to recommendation items
document.querySelectorAll('.recommendation-item').forEach(item => {
    item.addEventListener('click', () => {
        const title = item.querySelector('.rec-title').textContent;
        console.log('Clicked recommendation:', title);
        // Open learning module
    });
});

// Add hover effects to stat cards
document.querySelectorAll('.stat-card').forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.transform = 'translateY(-8px)';
    });
    
    card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateY(0)';
    });
});

// Console message
console.log('%c🧠 NeuroLearn AI Dashboard', 'color: #667eea; font-size: 20px; font-weight: bold;');
console.log('%cDashboard loaded successfully!', 'color: #10b981; font-size: 14px;');
