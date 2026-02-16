import api from '../api.js';

let vehicles = [];

export async function render() {
    const container = document.getElementById('app');

    container.innerHTML = `
        <div class="table-container">
            <div class="table-header">
                <h2>Vehicles</h2>
                <button class="btn btn-primary" onclick="window.showCreateVehicleModal()">
                    + Add Vehicle
                </button>
            </div>
            <div class="loading">Loading vehicles...</div>
        </div>
        
        <div id="vehicleModal" class="modal">
            <div class="modal-content">
                <div class="modal-header">
                    <h2>Add Vehicle</h2>
                    <button class="modal-close" onclick="window.closeVehicleModal()">×</button>
                </div>
                <form id="vehicleForm">
                    <div class="form-group">
                        <label>Placa *</label>
                        <input type="text" name="placa" required pattern="[A-Z0-9]{2,3}-[A-Z0-9]{3,5}">
                    </div>
                    <div class="form-group">
                        <label>Número Económico *</label>
                        <input type="text" name="numero_economico" required>
                    </div>
                    <div class="form-group">
                        <label>Marca *</label>
                        <input type="text" name="marca" required>
                    </div>
                    <div class="form-group">
                        <label>Modelo *</label>
                        <input type="text" name="modelo" required>
                    </div>
                    <div class="form-group">
                        <label>Año *</label>
                        <input type="number" name="anno" required min="1990" max="2026">
                    </div>
                    <div class="form-group">
                        <label>Tipo *</label>
                        <select name="tipo_vehiculo" required>
                            <option value="TRACTOR_TRUCK">Tractor Truck</option>
                            <option value="RIGID_TRUCK">Rigid Truck</option>
                            <option value="TRAILER">Trailer</option>
                            <option value="DOLLY">Dolly</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Capacidad Carga (kg) *</label>
                        <input type="number" name="capacidad_carga_kg" required min="0">
                    </div>
                    <div class="form-group">
                        <label>Número de Serie (VIN) *</label>
                        <input type="text" name="numero_serie" required minlength="17" maxlength="17">
                    </div>
                    <div class="form-group">
                        <label>Estado *</label>
                        <select name="estado_vehiculo" required>
                            <option value="ACTIVE">Active</option>
                            <option value="IN_MAINTENANCE">In Maintenance</option>
                            <option value="OUT_OF_SERVICE">Out of Service</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Póliza Seguro *</label>
                        <input type="text" name="poliza_seguro" required>
                    </div>
                    <div class="form-group">
                        <label>Vigencia Seguro *</label>
                        <input type="date" name="vigencia_seguro" required>
                    </div>
                    <div class="form-group">
                        <label>Kilometraje Actual *</label>
                        <input type="number" name="kilometraje_actual" required min="0">
                    </div>
                    <div class="form-group">
                        <label>Tipo Combustible *</label>
                        <select name="tipo_combustible" required>
                            <option value="DIESEL">Diesel</option>
                            <option value="NATURAL_GAS">Natural Gas</option>
                            <option value="ELECTRIC">Electric</option>
                        </select>
                    </div>
                    <button type="submit" class="btn btn-primary">Create Vehicle</button>
                </form>
            </div>
        </div>
    `;

    await loadVehicles();
    setupEventListeners();
}

async function loadVehicles() {
    try {
        vehicles = await api.getVehicles(50, 0);
        displayVehicles();
    } catch (error) {
        document.querySelector('.table-container').innerHTML = `
            <div class="error" style="color: var(--danger); padding: 2rem;">
                Error loading vehicles: ${error.message}
            </div>
        `;
    }
}

function displayVehicles() {
    const tableHtml = `
        <div class="table-header">
            <h2>Vehicles</h2>
            <button class="btn btn-primary" onclick="window.showCreateVehicleModal()">
                + Add Vehicle
            </button>
        </div>
        <table>
            <thead>
                <tr>
                    <th>Placa</th>
                    <th>Marca</th>
                    <th>Modelo</th>
                    <th>Año</th>
                    <th>Estado</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                ${vehicles.map(v => `
                    <tr>
                        <td>${v.placa}</td>
                        <td>${v.marca}</td>
                        <td>${v.modelo}</td>
                        <td>${v.anno}</td>
                        <td>
                            <span class="badge badge-${getStatusClass(v.estado_vehiculo)}">
                                ${v.estado_vehiculo}
                            </span>
                        </td>
                        <td>
                            <button class="btn btn-sm btn-danger" onclick="window.deleteVehicle('${v._id}')">
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

function getStatusClass(status) {
    if (status === 'ACTIVE') return 'success';
    if (status === 'IN_MAINTENANCE') return 'warning';
    return 'danger';
}

function setupEventListeners() {
    const form = document.getElementById('vehicleForm');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);

        // Convert numeric fields
        data.anno = parseInt(data.anno);
        data.capacidad_carga_kg = parseFloat(data.capacidad_carga_kg);
        data.kilometraje_actual = parseInt(data.kilometraje_actual);

        try {
            await api.createVehicle(data);
            window.closeVehicleModal();
            await loadVehicles();
        } catch (error) {
            alert('Error creating vehicle: ' + error.message);
        }
    });
}

// Global functions for onclick handlers
window.showCreateVehicleModal = () => {
    document.getElementById('vehicleModal').classList.add('active');
};

window.closeVehicleModal = () => {
    document.getElementById('vehicleModal').classList.remove('active');
    document.getElementById('vehicleForm').reset();
};

window.deleteVehicle = async (id) => {
    if (!confirm('Are you sure you want to delete this vehicle?')) return;

    try {
        await api.deleteVehicle(id);
        await loadVehicles();
    } catch (error) {
        alert('Error deleting vehicle: ' + error.message);
    }
};
