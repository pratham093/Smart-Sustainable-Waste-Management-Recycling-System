-- QUERY 5: NESTED QUERY (Non-Correlated Subquery)
-- Description: Find households on routes that have more than one scheduled collection

SELECT HouseholdID, Name, Address, RouteID
FROM Household
WHERE RouteID IN (
    SELECT RouteID
    FROM CollectionSchedule
    GROUP BY RouteID
    HAVING COUNT(ScheduleID) > 1
);