SELECT TOP 3 Category
FROM
(
	SELECT COUNT(*) AS NSales, MAX(Cat.CategoryName) AS Category
	FROM Products P
	JOIN Categories Cat ON P.CategoryID=Cat.CategoryID
	JOIN [Order Details] OD ON OD.ProductID=P.ProductID 
	GROUP BY P.CategoryID
) AS Temp
ORDER BY NSales DESC

SELECT TOP 3 MAX(Cat.CategoryName) AS Category
FROM Products P
	JOIN Categories Cat ON P.CategoryID=Cat.CategoryID
	JOIN [Order Details] OD ON OD.ProductID=P.ProductID 
GROUP BY P.CategoryID
ORDER BY COUNT(*) DESC
