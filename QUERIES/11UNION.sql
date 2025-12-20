-- QUERY 9: SET OPERATIONS (UNION)
-- Description: Get combined list of all people involved in waste management
--              (staff from Operations department UNION staff from Management)

SELECT StaffID, Name, Role, Department, 'Operations Staff' AS Category
FROM Staff
WHERE Department = 'Operations'

UNION

SELECT StaffID, Name, Role, Department, 'Management Staff' AS Category
FROM Staff
WHERE Department = 'Management'

UNION

SELECT StaffID, Name, Role, Department, 'Other Staff' AS Category
FROM Staff
WHERE Department NOT IN ('Operations', 'Management')

ORDER BY Category, Name;