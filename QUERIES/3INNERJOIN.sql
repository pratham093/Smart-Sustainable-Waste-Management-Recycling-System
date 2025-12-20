-- QUERY 3: INNER JOIN
-- Description: Get household details with their assigned route and zone information
SELECT 
    h.HouseholdID,
    h.Name AS HouseholdName,
    h.Address,
    r.Name AS RouteName,
    r.RouteDetails,
    z.Name AS ZoneName
FROM Household h
INNER JOIN Route r ON h.RouteID = r.RouteID
INNER JOIN Zone z ON r.ZoneID = z.ZoneID
ORDER BY z.Name, r.Name;