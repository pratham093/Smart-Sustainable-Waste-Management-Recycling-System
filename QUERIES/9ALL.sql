-- QUERY 8: >= ALL / > ANY
-- Description: Find vehicles with capacity >= all other vehicles (largest)

SELECT VehicleID, Model, Make, Capacity, LicensePlate
FROM Vehicle
WHERE Capacity >= ALL (
    SELECT Capacity
    FROM Vehicle
);