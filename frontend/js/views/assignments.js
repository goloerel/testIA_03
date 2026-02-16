import api from '../api.js';

let assignments = [];
let drivers = [];
let vehicles = [];

export async function render() {
    const container = document.getElementById('app');

    container.innerHTML = `
        <div class="table-container">
            <div class="table-header">
                <h2>Assignments</h2>
                <button class="btn btn-primary" onclick="window.showCreateAssignmentModal()">
                    + Create Assignment
                </button>
            </div>
            <div class="loading">Loading assignments...</div>
        </div>
        
        <div id="assignmentModal" class="modal">
            <div class="modal-content">
                <div class="modal-header">
                    <h2>Create Assignment</h2>
                    <button class="modal-close" onclick="window.closeAssignmentModal()">×</button>
                </div>
                <form id="assignmentForm">
                    <div class="form-group">
                        <label>Driver *</label>
                        <select name="driver_id" id="driverSelect" required>
                            <option value="">Select a driver...</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Vehicle *</label>
                        <select name="vehicle_id" id="vehicleSelect" required>
                            <option value="">Select a vehicle...</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Fecha Inicio *</label>
                        <input type="date" name="fecha_inicio" required>
                    </div>
                    <div class="form-group">
                        <label>Observaciones</label>
                        <input type="text" name="observaciones">
                    </div>
                    <button type="submit" class="btn btn-primary">Create Assignment</button>
                </form>
            </div>
        </div>
        
        <div id="endAssignmentModal" class="modal">
            <div class="modal-content">
                <div class="modal-header">
                    <h2>End Assignment</h2>
                    <button class="modal-close" onclick="window.closeEndAssignmentModal()">×</button>
                </div>
                <form id="endAssignmentForm">
                    <input type="hidden" id="endAssignmentId">
                    <div class="form-group">
                        <label>Fecha Fin *</label>
                        <input type="date" name="fecha_fin" required>
                    </div>
                    <div class="form-group">
                        <label>Estado *</label>
                        <select name="estado" required>
                            <option value="COMPLETED">Completed</option>
                            <option value="CANCELLED">Cancelled</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Nota de Cierre</label>
                        <input type="text" name="nota_cierre">
                    </div>
                    <button type="submit" class="btn btn-primary">End Assignment</button>
                </form>
            </div>
        </div>
    `;

    await loadData();
    setupEventListeners();
}

async function loadData() {
    try {
        [assignments, drivers, vehicles] = await Promise.all([
            api.getAssignments(50, 0),
            api.getDrivers(50, 0),
            api.getVehicles(50, 0)
        ]);
        displayAssignments();
        populateDropdowns();
    } catch (error) {
        document.querySelector('.table-container').innerHTML = `
            <div class="error" style="color: var(--danger); padding: 2rem;">
                Error loading data: ${error.message}
            </div>
        `;
    }
}

function displayAssignments() {
    const tableHtml = `
        <div class="table-header">
            <h2>Assignments</h2>
            <button class="btn btn-primary" onclick="window.showCreateAssignmentModal()">
                + Create Assignment
            </button>
        </div>
        <table>
            <thead>
                <tr>
                    <th>Driver</th>
                    <th>Vehicle</th>
                    <th>Fecha Inicio</th>
                    <th>Estado</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                ${assignments.map(a => {
        const driver = drivers.find(d => d._id === a.driver_id);
        const vehicle = vehicles.find(v => v._id === a.vehicle_id);
        return `
                        <tr>
                            <td>${driver ? driver.nombre : a.driver_id}</td>
                            <td>${vehicle ? vehicle.placa : a.vehicle_id}</td>
                            <td>${a.fecha_inicio}</td>
                            <td>
                                <span class="badge badge-${getStatusClass(a.estado)}">
                                    ${a.estado}
                                </span>
                            </td>
                            <td>
                                ${a.estado === 'ACTIVE' ? `
                                    <button class="btn btn-sm btn-success" onclick="window.showEndAssignmentModal('${a._id}')">
                                        End
                                    </button>
                                ` : ''}
                            </td>
                        </tr>
                    `;
    }).join('')}
            </tbody>
        </table>
    `;

    document.querySelector('.table-container').innerHTML = tableHtml;
}

function populateDropdowns() {
    const driverSelect = document.getElementById('driverSelect');
    const vehicleSelect = document.getElementById('vehicleSelect');

    drivers.forEach(d => {
        const option = document.createElement('option');
        option.value = d._id;
        option.textContent = `${d.nombre} (${d.licencia})`;
        driverSelect.appendChild(option);
    });

    vehicles.forEach(v => {
        const option = document.createElement('option');
        option.value = v._id;
        option.textContent = `${v.placa} - ${v.marca} ${v.modelo}`;
        vehicleSelect.appendChild(option);
    });
}

function getStatusClass(status) {
    if (status === 'ACTIVE') return 'success';
    if (status === 'COMPLETED') return 'warning';
    return 'danger';
}

function setupEventListeners() {
    document.getElementById('assignmentForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const data = Object.fromEntries(formData);

        try {
            await api.createAssignment(data);
            window.closeAssignmentModal();
            await loadData();
        } catch (error) {
            alert('Error creating assignment: ' + error.message);
        }
    });

    document.getElementById('endAssignmentForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const id = document.getElementById('endAssignmentId').value;
        const formData = new FormData(e.target);
        const data = Object.fromEntries(formData);

        try {
            await api.updateAssignment(id, data);
            window.closeEndAssignmentModal();
            await loadData();
        } catch (error) {
            alert('Error ending assignment: ' + error.message);
        }
    });
}

// Global functions
window.showCreateAssignmentModal = () => {
    document.getElementById('assignmentModal').classList.add('active');
};

window.closeAssignmentModal = () => {
    document.getElementById('assignmentModal').classList.remove('active');
    document.getElementById('assignmentForm').reset();
};

window.showEndAssignmentModal = (id) => {
    document.getElementById('endAssignmentId').value = id;
    document.getElementById('endAssignmentModal').classList.add('active');
};

window.closeEndAssignmentModal = () => {
    document.getElementById('endAssignmentModal').classList.remove('active');
    document.getElementById('endAssignmentForm').reset();
};
