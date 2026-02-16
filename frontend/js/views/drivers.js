import api from '../api.js';

let drivers = [];

export async function render() {
    const container = document.getElementById('app');

    container.innerHTML = `
        <div class="table-container">
            <div class="table-header">
                <h2>Drivers</h2>
                <button class="btn btn-primary" onclick="window.showCreateDriverModal()">
                    + Add Driver
                </button>
            </div>
            <div class="loading">Loading drivers...</div>
        </div>
        
        <div id="driverModal" class="modal">
            <div class="modal-content">
                <div class="modal-header">
                    <h2>Add Driver</h2>
                    <button class="modal-close" onclick="window.closeDriverModal()">×</button>
                </div>
                <form id="driverForm">
                    <div class="form-group">
                        <label>Nombre *</label>
                        <input type="text" name="nombre" required>
                    </div>
                    <div class="form-group">
                        <label>Licencia *</label>
                        <input type="text" name="licencia" required>
                    </div>
                    <div class="form-group">
                        <label>Estado *</label>
                        <select name="estado" required>
                            <option value="ACTIVE">Active</option>
                            <option value="INACTIVE">Inactive</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Fecha Contratación *</label>
                        <input type="date" name="fecha_contratacion" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Create Driver</button>
                </form>
            </div>
        </div>
    `;

    await loadDrivers();
    setupEventListeners();
}

async function loadDrivers() {
    try {
        drivers = await api.getDrivers(50, 0);
        displayDrivers();
    } catch (error) {
        document.querySelector('.table-container').innerHTML = `
            <div class="error" style="color: var(--danger); padding: 2rem;">
                Error loading drivers: ${error.message}
            </div>
        `;
    }
}

function displayDrivers() {
    const tableHtml = `
        <div class="table-header">
            <h2>Drivers</h2>
            <button class="btn btn-primary" onclick="window.showCreateDriverModal()">
                + Add Driver
            </button>
        </div>
        <table>
            <thead>
                <tr>
                    <th>Nombre</th>
                    <th>Licencia</th>
                    <th>Estado</th>
                    <th>Fecha Contratación</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                ${drivers.map(d => `
                    <tr>
                        <td>${d.nombre}</td>
                        <td>${d.licencia}</td>
                        <td>
                            <span class="badge badge-${d.estado === 'ACTIVE' ? 'success' : 'danger'}">
                                ${d.estado}
                            </span>
                        </td>
                        <td>${d.fecha_contratacion}</td>
                        <td>
                            <button class="btn btn-sm btn-danger" onclick="window.deleteDriver('${d._id}')">
                                Delete
                            </button>
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;

    document.querySelector('.table-container').innerHTML = tableHtml;
}

function setupEventListeners() {
    const form = document.getElementById('driverForm');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);

        try {
            await api.createDriver(data);
            window.closeDriverModal();
            await loadDrivers();
        } catch (error) {
            alert('Error creating driver: ' + error.message);
        }
    });
}

// Global functions
window.showCreateDriverModal = () => {
    document.getElementById('driverModal').classList.add('active');
};

window.closeDriverModal = () => {
    document.getElementById('driverModal').classList.remove('active');
    document.getElementById('driverForm').reset();
};

window.deleteDriver = async (id) => {
    if (!confirm('Are you sure you want to delete this driver?')) return;

    try {
        await api.deleteDriver(id);
        await loadDrivers();
    } catch (error) {
        alert('Error deleting driver: ' + error.message);
    }
};
