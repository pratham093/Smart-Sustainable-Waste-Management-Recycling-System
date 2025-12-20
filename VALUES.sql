INSERT INTO Zone (Name, GeographicBoundary) VALUES
('North Zone', 'Latitude: 42.3601, Longitude: -71.0942'),
('South Zone', 'Latitude: 42.3401, Longitude: -71.0742'),
('East Zone', 'Latitude: 42.3501, Longitude: -71.0642'),
('West Zone', 'Latitude: 42.3701, Longitude: -71.1042'),
('Central Zone', 'Latitude: 42.3551, Longitude: -71.0842');

-- Insert Routes
INSERT INTO Route (Name, RouteDetails, ZoneID) VALUES
('Route N1', 'Main Street to Oak Avenue', 1),
('Route N2', 'Pine Road to Elm Street', 1),
('Route S1', 'River Road to Lake Street', 2),
('Route S2', 'Hill Avenue to Valley Drive', 2),
('Route E1', 'Eastern Parkway to Sunrise Blvd', 3),
('Route W1', 'Western Avenue to Sunset Drive', 4),
('Route C1', 'Central Square to City Hall', 5);

-- Insert Waste Types
INSERT INTO WasteType (Name, DisposalMethod, ProcessingCost) VALUES
('Organic', 'Composting', 25.50),
('Recyclable', 'Recycling', 15.75),
('Hazardous', 'Special Treatment', 85.00),
('General', 'Landfill', 35.00),
('Electronic', 'E-waste Processing', 65.00),
('Glass', 'Glass Recycling', 20.00),
('Paper', 'Paper Recycling', 12.50);

-- Insert Households
INSERT INTO Household (Name, Address, ContactEmail, RouteID) VALUES
('Smith Family', '123 Main St', 'smith@email.com', 1),
('Johnson Family', '456 Oak Ave', 'johnson@email.com', 1),
('Williams Family', '789 Pine Rd', 'williams@email.com', 2),
('Brown Family', '321 Elm St', 'brown@email.com', 2),
('Davis Family', '654 River Rd', 'davis@email.com', 3),
('Miller Family', '987 Lake St', 'miller@email.com', 3),
('Wilson Family', '147 Hill Ave', 'wilson@email.com', 4),
('Moore Family', '258 Valley Dr', 'moore@email.com', 4),
('Taylor Family', '369 Eastern Pkwy', 'taylor@email.com', 5),
('Anderson Family', '741 Sunrise Blvd', 'anderson@email.com', 5),
('Thomas Family', '852 Western Ave', 'thomas@email.com', 6),
('Jackson Family', '963 Sunset Dr', 'jackson@email.com', 6),
('White Family', '159 Central Sq', 'white@email.com', 7),
('Harris Family', '753 City Hall Rd', 'harris@email.com', 7),
('Martin Family', '486 North St', 'martin@email.com', 1);

-- Insert Staff
INSERT INTO Staff (Name, HireDate, Role, Department, ContactPhone) VALUES
('John Driver', '2020-01-15', 'Driver', 'Operations', '555-0101'),
('Jane Collector', '2020-03-20', 'Collector', 'Operations', '555-0102'),
('Bob Supervisor', '2019-05-10', 'Supervisor', 'Management', '555-0103'),
('Alice Driver', '2021-02-01', 'Driver', 'Operations', '555-0104'),
('Tom Collector', '2021-06-15', 'Collector', 'Operations', '555-0105'),
('Sarah Admin', '2019-08-20', 'Administrator', 'Admin', '555-0106'),
('Mike Mechanic', '2020-11-30', 'Mechanic', 'Maintenance', '555-0107'),
('Lisa Collector', '2022-01-10', 'Collector', 'Operations', '555-0108'),
('David Driver', '2022-03-25', 'Driver', 'Operations', '555-0109'),
('Emma Supervisor', '2018-12-01', 'Supervisor', 'Management', '555-0110');

-- Insert Vehicles
INSERT INTO Vehicle (Model, Make, Capacity, LicensePlate, Status) VALUES
('F-550', 'Ford', 5000.00, 'WM-001', 'Active'),
('T880', 'Kenworth', 8000.00, 'WM-002', 'Active'),
('ACX', 'Mack', 7000.00, 'WM-003', 'Active'),
('F-450', 'Ford', 4500.00, 'WM-004', 'Maintenance'),
('T370', 'Kenworth', 6000.00, 'WM-005', 'Active'),
('LR', 'Mack', 7500.00, 'WM-006', 'Active');

-- Insert Collection Schedules
INSERT INTO CollectionSchedule (RouteID, StartTime, EndTime, IsRecurring, ScheduledDate, CollectionDay) VALUES
(1, '06:00:00', '14:00:00', TRUE, '2025-11-01', 'Monday'),
(1, '06:00:00', '14:00:00', TRUE, '2025-11-04', 'Thursday'),
(2, '07:00:00', '15:00:00', TRUE, '2025-11-02', 'Tuesday'),
(2, '07:00:00', '15:00:00', TRUE, '2025-11-05', 'Friday'),
(3, '06:30:00', '14:30:00', TRUE, '2025-11-01', 'Monday'),
(4, '08:00:00', '16:00:00', TRUE, '2025-11-03', 'Wednesday'),
(5, '06:00:00', '14:00:00', TRUE, '2025-11-02', 'Tuesday'),
(6, '07:30:00', '15:30:00', TRUE, '2025-11-04', 'Thursday'),
(7, '08:00:00', '16:00:00', TRUE, '2025-11-05', 'Friday');

-- Insert Waste Bins
INSERT INTO WasteBin (HouseholdID, WasteTypeID, BinLocation, Capacity) VALUES
(1, 1, 'Curbside', 120.00),
(1, 2, 'Curbside', 240.00),
(2, 1, 'Driveway', 120.00),
(2, 4, 'Curbside', 240.00),
(3, 2, 'Curbside', 240.00),
(3, 1, 'Backyard', 120.00),
(4, 4, 'Curbside', 360.00),
(5, 2, 'Driveway', 240.00),
(5, 1, 'Curbside', 120.00),
(6, 4, 'Curbside', 240.00),
(7, 2, 'Curbside', 240.00),
(8, 1, 'Backyard', 120.00),
(9, 2, 'Driveway', 240.00),
(10, 4, 'Curbside', 360.00),
(11, 1, 'Curbside', 120.00),
(12, 2, 'Driveway', 240.00),
(13, 4, 'Curbside', 240.00),
(14, 1, 'Backyard', 120.00),
(15, 2, 'Curbside', 240.00);

-- Insert Recycling Centers
INSERT INTO RecyclingCenter (Name, Address, ProcessingCapacity) VALUES
('Green Earth Recycling', '100 Recycling Way', 10000.00),
('EcoCenter Boston', '200 Environmental Dr', 15000.00),
('Clean Future Facility', '300 Sustainability Rd', 12000.00),
('Resource Recovery Center', '400 Recovery Ave', 8000.00);

-- Insert Collection Logs
INSERT INTO CollectionLog (RouteID, VehicleID, CollectionDate, TotalRouteWeight, Status) VALUES
(1, 1, '2025-11-01', 1250.50, 'Completed'),
(2, 2, '2025-11-02', 1800.75, 'Completed'),
(3, 3, '2025-11-01', 1500.25, 'Completed'),
(4, 1, '2025-11-03', 2100.00, 'Completed'),
(5, 5, '2025-11-02', 1750.50, 'Completed'),
(1, 1, '2025-11-04', 1300.00, 'Completed'),
(2, 2, '2025-11-05', 1850.25, 'Completed'),
(6, 6, '2025-11-04', 1600.75, 'Completed'),
(7, 3, '2025-11-05', 1950.50, 'Completed'),
(1, 1, '2025-10-28', 1200.00, 'Completed');

-- Insert Log Staff (Junction table)
INSERT INTO LogStaff (CollectionLogID, StaffID, Role) VALUES
(1, 1, 'Driver'),
(1, 2, 'Collector'),
(2, 4, 'Driver'),
(2, 5, 'Collector'),
(3, 9, 'Driver'),
(3, 8, 'Collector'),
(4, 1, 'Driver'),
(4, 2, 'Collector'),
(5, 4, 'Driver'),
(5, 5, 'Collector');

-- Insert Log Vehicle (Junction table)
INSERT INTO LogVehicle (CollectionLogID, VehicleID, DriverStaffID) VALUES
(1, 1, 1),
(2, 2, 4),
(3, 3, 9),
(4, 1, 1),
(5, 5, 4),
(6, 1, 1),
(7, 2, 4),
(8, 6, 9),
(9, 3, 1);

-- Insert Collection Details (Junction table)
INSERT INTO CollectionDetails (CollectionLogID, WasteBinID, WasteTypeID, CollectedWeight, CollectionTime) VALUES
(1, 1, 1, 45.50, '06:30:00'),
(1, 2, 2, 85.25, '06:45:00'),
(1, 3, 1, 38.75, '07:00:00'),
(2, 5, 2, 92.00, '07:30:00'),
(2, 6, 1, 41.25, '07:45:00'),
(3, 8, 2, 78.50, '06:45:00'),
(3, 9, 1, 52.00, '07:00:00'),
(4, 10, 4, 125.75, '08:30:00'),
(5, 11, 2, 88.00, '06:30:00'),
(6, 1, 1, 48.25, '06:30:00'),
(6, 2, 2, 91.50, '06:45:00'),
(7, 5, 2, 95.75, '07:30:00'),
(8, 12, 2, 87.25, '07:45:00'),
(9, 14, 4, 142.00, '08:15:00');

-- Insert Center Processing (Junction table)
INSERT INTO CenterProcessing (CenterID, WasteTypeID, ProcessingCost, ProcessingCapacity) VALUES
(1, 1, 20.00, 2000.00),
(1, 2, 15.00, 3000.00),
(2, 2, 14.50, 4000.00),
(2, 4, 32.00, 2500.00),
(3, 1, 22.00, 1800.00),
(3, 5, 60.00, 1000.00),
(4, 6, 18.00, 1500.00),
(4, 7, 11.00, 2000.00);

-- Insert Violations
INSERT INTO Violation (HouseholdID, DateIssued, Reason, FineAmount, Status, ViolationType) VALUES
(1, '2025-10-15', 'Improper waste sorting', 50.00, 'Paid', 'Minor'),
(3, '2025-10-20', 'Bin overflow', 75.00, 'Pending', 'Minor'),
(5, '2025-10-25', 'Hazardous waste in regular bin', 150.00, 'Pending', 'Major'),
(7, '2025-10-28', 'Missed collection schedule', 25.00, 'Paid', 'Minor'),
(2, '2025-11-01', 'Contaminated recycling', 50.00, 'Pending', 'Minor');

-- Insert Payments
INSERT INTO Payment (HouseholdID, Amount, PaymentDate, PaymentType, ServicePeriod, ViolationID) VALUES
(1, 50.00, '2025-10-20', 'Fine', NULL, 1),
(1, 45.00, '2025-11-01', 'Service', 'November 2025', NULL),
(2, 45.00, '2025-11-01', 'Service', 'November 2025', NULL),
(3, 45.00, '2025-11-01', 'Service', 'November 2025', NULL),
(4, 45.00, '2025-11-01', 'Service', 'November 2025', NULL),
(5, 45.00, '2025-11-01', 'Service', 'November 2025', NULL),
(7, 25.00, '2025-10-30', 'Fine', NULL, 4),
(7, 45.00, '2025-11-01', 'Service', 'November 2025', NULL),
(8, 45.00, '2025-11-01', 'Service', 'November 2025', NULL),
(9, 45.00, '2025-11-01', 'Service', 'November 2025', NULL),
(10, 45.00, '2025-11-01', 'Service', 'November 2025', NULL);