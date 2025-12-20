USE waste_management_system;

SELECT VehicleID, Model, Make, Capacity, LicensePlate, Status
FROM Vehicle
WHERE Status = 'Active' AND Capacity > 5000;