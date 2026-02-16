import * as Dashboard from './views/dashboard.js';
import * as Vehicles from './views/vehicles.js';
import * as Drivers from './views/drivers.js';
import * as Assignments from './views/assignments.js';

const routes = {
    'dashboard': Dashboard,
    'vehicles': Vehicles,
    'drivers': Drivers,
    'assignments': Assignments
};

let currentRoute = 'dashboard';

function navigate(route) {
    // Update active nav link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.dataset.route === route) {
            link.classList.add('active');
        }
    });

    // Render the view
    currentRoute = route;
    if (routes[route]) {
        routes[route].render();
    }
}

function init() {
    // Setup navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const route = link.dataset.route;
            window.location.hash = route === 'dashboard' ? '/' : `/${route}`;
        });
    });

    // Handle hash changes
    window.addEventListener('hashchange', () => {
        const hash = window.location.hash.slice(1) || '/';
        const route = hash === '/' ? 'dashboard' : hash.slice(1);
        navigate(route);
    });

    // Initial route
    const hash = window.location.hash.slice(1) || '/';
    const route = hash === '/' ? 'dashboard' : hash.slice(1);
    navigate(route);
}

// Start the app
init();
