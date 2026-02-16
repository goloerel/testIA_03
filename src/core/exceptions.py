class FleetManagementException(Exception):
    """Base exception for the application"""
    pass

class VehicleAlreadyExistsError(FleetManagementException):
    def __init__(self, message: str = "Vehicle already exists"):
        self.message = message
        super().__init__(self.message)


class VehicleNotFoundError(FleetManagementException):
    def __init__(self, message: str = "Vehicle not found"):
        self.message = message
        super().__init__(self.message)

class DriverAlreadyExistsError(FleetManagementException):
    def __init__(self, message: str = "Driver already exists"):
        self.message = message
        super().__init__(self.message)


class DriverNotFoundError(FleetManagementException):
    def __init__(self, message: str = "Driver not found"):
        self.message = message
        super().__init__(self.message)

class AssignmentError(FleetManagementException):
    """Base exception for assignment errors"""
    pass

class VehicleAlreadyAssignedError(AssignmentError):
    def __init__(self, message: str = "Vehicle is already assigned"):
        self.message = message
        super().__init__(self.message)

class DriverAlreadyAssignedError(AssignmentError):
    def __init__(self, message: str = "Driver is already assigned"):
        self.message = message
        super().__init__(self.message)

class AssignmentNotFoundError(AssignmentError):
    def __init__(self, message: str = "Assignment not found"):
        self.message = message
        super().__init__(self.message)
