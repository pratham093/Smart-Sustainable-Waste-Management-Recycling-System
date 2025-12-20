-- QUERY 4: LEFT OUTER JOIN
-- Description: List all households with their violations (including those without violations)
SELECT 
    h.HouseholdID,
    h.Name AS HouseholdName,
    h.Address,
    v.ViolationID,
    v.Reason,
    v.FineAmount,
    v.Status AS ViolationStatus
FROM Household h
LEFT OUTER JOIN Violation v ON h.HouseholdID = v.HouseholdID
ORDER BY h.HouseholdID;