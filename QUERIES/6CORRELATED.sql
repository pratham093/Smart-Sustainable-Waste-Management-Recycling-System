-- QUERY 6: CORRELATED QUERY
-- Description: Find staff members who have participated in more collections than the average
SELECT s.StaffID, s.Name, s.Role, s.Department
FROM Staff s
WHERE (
    SELECT COUNT(*)
    FROM LogStaff ls
    WHERE ls.StaffID = s.StaffID
) > (
    SELECT AVG(collection_count)
    FROM (
        SELECT COUNT(*) AS collection_count
        FROM LogStaff
        GROUP BY StaffID
    ) AS avg_counts
);