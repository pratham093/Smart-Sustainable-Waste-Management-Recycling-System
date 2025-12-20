-- QUERY 7: EXISTS / NOT EXISTS
-- Description: Find recycling centers that process recyclable waste type (EXISTS)
--              and waste types not processed by any center (NOT EXISTS)
SELECT rc.CenterID, rc.Name, rc.Address, rc.ProcessingCapacity
FROM RecyclingCenter rc
WHERE EXISTS (
    SELECT 1
    FROM CenterProcessing cp
    JOIN WasteType wt ON cp.WasteTypeID = wt.WasteTypeID
    WHERE cp.CenterID = rc.CenterID
    AND wt.Name = 'Recyclable'
);
