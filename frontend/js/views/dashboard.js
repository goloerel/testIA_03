import api from '../api.js';

export async function render() {
    const container = document.getElementById('app');

    container.innerHTML = `
        <div class="loading">Loading dashboard...</div>
    `;

    try {
        const stats = await api.getStats();

        container.innerHTML = `
            <h1 style="margin-bottom: 2rem;">Dashboard</h1>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <h3>Total Vehicles</h3>
                    <div class="value">${stats.vehicles_total}</div>
                    <div class="subtext">
                        ${stats.vehicles_active} active, 
                        ${stats.vehicles_maintenance} in maintenance
                    </div>
                </div>
                
                <div class="stat-card">
                    <h3>Total Drivers</h3>
                    <div class="value">${stats.drivers_total}</div>
                    <div class="subtext">${stats.drivers_active} active</div>
                </div>
                
                <div class="stat-card">
                    <h3>Active Assignments</h3>
                    <div class="value">${stats.assignments_active}</div>
                    <div class="subtext">Currently assigned</div>
                </div>
            </div>
        `;
    } catch (error) {
        container.innerHTML = `
            <div class="error" style="color: var(--danger); padding: 2rem;">
                Error loading dashboard: ${error.message}
            </div>
        `;
    }
}
