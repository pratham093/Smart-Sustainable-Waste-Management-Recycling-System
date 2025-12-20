-- QUERY 2: AGGREGATE QUERY
-- Description: Calculate total fines collected and average fine amount by violation type
use waste_management_system;
SELECT 
    ViolationType,
    COUNT(*) AS TotalViolations,
    SUM(FineAmount) AS TotalFines,
    AVG(FineAmount) AS AverageFine,
    MAX(FineAmount) AS MaxFine,
    MIN(FineAmount) AS MinFine
FROM Violation
GROUP BY ViolationType
HAVING COUNT(*) >= 1;