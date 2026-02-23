// NeuroLearn AI - Dashboard Interactivity

const API_BASE_URL = 'https://ai-neuro-backend.onrender.com';

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    initializeNavigation();
    initializeAnimations();
    loadUserData();
    loadRecommendations();
});

// Navigation handling
function initializeNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');
            const href = item.getAttribute('href');
            navigateToPage(href);
        });
    });
}

function navigateToPage(page) {
    window.scrollTo({ top: 0, behavior: 'smooth' });
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
    }, { threshold: 0.1 });

    document.querySelectorAll('.card, .stat-card').forEach(card => {
        observer.observe(card);
    });
}

// ============================================
// API INTEGRATION - Load User Data
// ============================================

async function loadUserData() {
    const userId = 'demo_user_123';

    try {
        showLoadingState();

        const response = await fetch(`${API_BASE_URL}/api/v1/users/${userId}`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });

        if (!response.ok) throw new Error(`HTTP error: ${response.status}`);

        const data = await response.json();
        updateDashboard(data);

    } catch (error) {
        console.error('Error loading user data:', error);
        showFallbackData(); // Show static data if API fails
    }
}

// ============================================
// API INTEGRATION - Load Recommendations
// ============================================

async function loadRecommendations() {
    const userId = 'demo_user_123';

    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/adaptation/recommend-content`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
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

        if (!response.ok) throw new Error(`HTTP error: ${response.status}`);

        const data = await response.json();
        updateRecommendations(data);

    } catch (error) {
        console.error('Error loading recommendations:', error);
        // Static recommendations already in HTML - no update needed
    }
}

// ============================================
// UPDATE DASHBOARD WITH API DATA
// ============================================

function updateDashboard(data) {
    // Update stat cards
    if (data.sessions_completed !== undefined) {
        const sessionEl = document.querySelector('.stat-card:nth-child(1) .stat-value');
        if (sessionEl) sessionEl.textContent = data.sessions_completed;
    }

    if (data.average_score !== undefined) {
        const scoreEl = document.querySelector('.stat-card:nth-child(2) .stat-value');
        if (scoreEl) scoreEl.innerHTML = `${(data.average_score * 100).toFixed(1)}<span class="stat-unit">%</span>`;
    }

    if (data.engagement_level !== undefined) {
        const engageEl = document.querySelector('.stat-card:nth-child(3) .stat-value');
        if (engageEl) engageEl.innerHTML = `${(data.engagement_level * 100).toFixed(0)}<span class="stat-unit">%</span>`;
    }

    if (data.streak_days !== undefined) {
        const streakEl = document.querySelector('.stat-card:nth-child(4) .stat-value');
        if (streakEl) streakEl.innerHTML = `🔥 <span>${data.streak_days}</span>`;
    }

    // Update cognitive profile
    if (data.learning_style) {
        const styleEl = document.querySelector('.profile-stat:nth-child(1) .profile-stat-value');
        if (styleEl) styleEl.textContent = capitalize(data.learning_style);
    }

    if (data.cognitive_load_capacity) {
        const loadEl = document.querySelector('.profile-stat:nth-child(2) .profile-stat-value');
        if (loadEl) loadEl.textContent = `${data.cognitive_load_capacity}/10`;
    }

    // Update user name
    if (data.name) {
        const titleEl = document.querySelector('.page-title');
        if (titleEl) titleEl.textContent = `Welcome back, ${data.name} 👋`;

        const avatarEl = document.querySelector('.user-avatar span');
        if (avatarEl) {
            const initials = data.name.split(' ').map(n => n[0]).join('');
            avatarEl.textContent = initials;
        }

        const nameEl = document.querySelector('.user-name');
        if (nameEl) nameEl.textContent = data.name;
    }
}

function updateRecommendations(data) {
    const list = document.querySelector('.recommendation-list');
    if (!list || !data.recommendations?.length) return;

    // Clear existing and render API recommendations
    list.innerHTML = '';

    const types = ['video', 'text', 'code'];

    data.recommendations.slice(0, 3).forEach((rec, index) => {
        const item = document.createElement('div');
        item.className = 'recommendation-item';
        item.innerHTML = `
            <div class="rec-thumbnail ${types[index % types.length]}"></div>
            <div class="rec-content">
                <h3 class="rec-title">${rec.title || rec.content_id}</h3>
                <div class="rec-meta">
                    <span class="rec-type">${rec.content_type || 'Interactive'} • ${rec.duration || '45'} min</span>
                    <span class="rec-match">${Math.round((rec.score || 0.9) * 100)}% match</span>
                </div>
            </div>
        `;
        item.addEventListener('click', () => {
            console.log('Opening:', rec.title || rec.content_id);
        });
        list.appendChild(item);
    });
}

// ============================================
// LOADING STATE & FALLBACK
// ============================================

function showLoadingState() {
    document.querySelectorAll('.stat-value').forEach(el => {
        el.style.opacity = '0.4';
    });
}

function showFallbackData() {
    // Restore opacity — static HTML values already shown
    document.querySelectorAll('.stat-value').forEach(el => {
        el.style.opacity = '1';
    });
    console.log('Using static fallback data');
}

// ============================================
// PROGRESS BAR ANIMATIONS
// ============================================

function animateProgressBars() {
    const progressFills = document.querySelectorAll('.progress-fill');
    progressFills.forEach(fill => {
        const width = fill.style.getPropertyValue('--width');
        fill.style.width = '0%';
        setTimeout(() => { fill.style.width = width; }, 100);
    });
}

setTimeout(animateProgressBars, 500);

// ============================================
// BUTTON HANDLERS
// ============================================

document.querySelector('.btn-secondary')?.addEventListener('click', async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/users/demo_user_123/export`);
        if (response.ok) {
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'learning-data.json';
            a.click();
        } else {
            alert('Export coming soon!');
        }
    } catch {
        alert('Export coming soon!');
    }
});

document.querySelector('.btn-primary')?.addEventListener('click', async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/adaptation/next-lesson`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: 'demo_user_123' })
        });
        if (response.ok) {
            const data = await response.json();
            alert(`Starting: ${data.lesson_title || 'Next Lesson'}`);
        } else {
            alert('Starting next lesson...');
        }
    } catch {
        alert('Starting next lesson...');
    }
});

// Recommendation click handlers
document.querySelectorAll('.recommendation-item').forEach(item => {
    item.addEventListener('click', () => {
        const title = item.querySelector('.rec-title')?.textContent;
        console.log('Clicked recommendation:', title);
    });
});

// Stat card hover effects
document.querySelectorAll('.stat-card').forEach(card => {
    card.addEventListener('mouseenter', () => { card.style.transform = 'translateY(-8px)'; });
    card.addEventListener('mouseleave', () => { card.style.transform = 'translateY(0)'; });
});

// Helpers
function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

console.log('%c🧠 NeuroLearn AI Dashboard', 'color: #667eea; font-size: 20px; font-weight: bold;');
console.log('%cDashboard loaded successfully!', 'color: #10b981; font-size: 14px;');