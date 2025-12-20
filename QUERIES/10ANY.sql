-- Using > ANY: Collection logs with weight greater than any collection in Route 3

SELECT cl.CollectionLogID, r.Name AS RouteName, cl.CollectionDate, cl.TotalRouteWeight
FROM CollectionLog cl
JOIN Route r ON cl.RouteID = r.RouteID
WHERE cl.TotalRouteWeight > ANY (
    SELECT TotalRouteWeight
    FROM CollectionLog
    WHERE RouteID = 3
);