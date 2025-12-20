-- QUERY 10: SUBQUERIES IN SELECT AND FROM
-- Description: Comprehensive analysis with subqueries in both SELECT and FROM clauses
SELECT 
    h.HouseholdID,
    h.Name AS HouseholdName,
    h.Address,
    -- Subquery in SELECT: Count of bins per household
    (SELECT COUNT(*) 
     FROM WasteBin wb 
     WHERE wb.HouseholdID = h.HouseholdID) AS TotalBins,
    -- Subquery in SELECT: Total violations per household
    (SELECT COALESCE(SUM(v.FineAmount), 0) 
     FROM Violation v 
     WHERE v.HouseholdID = h.HouseholdID) AS TotalFines,
    -- Subquery in SELECT: Total payments made
    (SELECT COALESCE(SUM(p.Amount), 0) 
     FROM Payment p 
     WHERE p.HouseholdID = h.HouseholdID) AS TotalPayments,
    route_stats.RouteName,
    route_stats.TotalHouseholdsOnRoute
FROM Household h
-- Subquery in FROM: Route statistics
JOIN (
    SELECT 
        r.RouteID,
        r.Name AS RouteName,
        COUNT(hh.HouseholdID) AS TotalHouseholdsOnRoute
    FROM Route r
    LEFT JOIN Household hh ON r.RouteID = hh.RouteID
    GROUP BY r.RouteID, r.Name
) AS route_stats ON h.RouteID = route_stats.RouteID
ORDER BY h.HouseholdID;
