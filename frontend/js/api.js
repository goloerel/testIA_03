const API_BASE = '/api/v1';

class API {
    async request(endpoint, options = {}) {
        const url = `${API_BASE}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Request failed');
            }

            if (response.status === 204) {
                return null;
            }

            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Stats
    async getStats() {
        return this.request('/stats/');
    }

    // Vehicles
    async getVehicles(limit = 10, offset = 0) {
        return this.request(`/vehicles?limit=${limit}&offset=${offset}`);
    }

    async getVehicle(id) {
        return this.request(`/vehicles/${id}`);
    }

    async createVehicle(data) {
        return this.request('/vehicles/', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async updateVehicle(id, data) {
        return this.request(`/vehicles/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    async deleteVehicle(id) {
        return this.request(`/vehicles/${id}`, {
            method: 'DELETE'
        });
    }

    // Drivers
    async getDrivers(limit = 10, offset = 0) {
        return this.request(`/drivers?limit=${limit}&offset=${offset}`);
    }

    async getDriver(id) {
        return this.request(`/drivers/${id}`);
    }

    async createDriver(data) {
        return this.request('/drivers/', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async updateDriver(id, data) {
        return this.request(`/drivers/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    async deleteDriver(id) {
        return this.request(`/drivers/${id}`, {
            method: 'DELETE'
        });
    }

    // Assignments
    async getAssignments(limit = 10, offset = 0) {
        return this.request(`/assignments?limit=${limit}&offset=${offset}`);
    }

    async getAssignment(id) {
        return this.request(`/assignments/${id}`);
    }

    async createAssignment(data) {
        return this.request('/assignments/', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async updateAssignment(id, data) {
        return this.request(`/assignments/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }
}

export default new API();
