SELECT wt.WasteTypeID, wt.Name, wt.DisposalMethod
FROM WasteType wt
WHERE NOT EXISTS (
    SELECT 1
    FROM CenterProcessing cp
    WHERE cp.WasteTypeID = wt.WasteTypeID
);