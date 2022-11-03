SELECT COUNT(*) AS NSales, MAX(Cat.CategoryName) AS Category, O.ShipCountry AS Country
FROM Products P
JOIN Categories Cat ON P.CategoryID=Cat.CategoryID
JOIN [Order Details] OD ON P.ProductID=OD.ProductID
JOIN Orders O ON OD.OrderID=O.OrderID
GROUP BY P.CategoryID, O.ShipCountry
ORDER BY NSales DESC