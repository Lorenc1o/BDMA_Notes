SELECT COUNT(*) AS NSales, MONTH(OrderDate) as Month, YEAR(OrderDate) as Year, ShipCountry, MAX(Cat.CategoryName) AS Category
FROM Products P
JOIN Categories Cat ON P.CategoryID=Cat.CategoryID
JOIN [Order Details] OD ON P.ProductID=OD.ProductID
JOIN Orders O ON OD.OrderID=O.OrderID 
GROUP BY MONTH(OrderDate), YEAR(OrderDate), ShipCountry
ORDER BY Year, Month