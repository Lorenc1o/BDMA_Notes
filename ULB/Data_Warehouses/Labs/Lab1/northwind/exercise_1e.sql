SELECT CAST(SUM((Unitprice-Discount)*Quantity) AS int) as TotalSales, E.FirstName as Name, E.LastName as SecondName, MONTH(OrderDate) as Month
FROM Employees E, Orders O
JOIN [Order Details] OD ON OD.OrderID=O.OrderID
WHERE YEAR(O.OrderDate) = '1997' AND E.EmployeeID=9
GROUP BY E.FirstName, E.LastName, MONTH(OrderDate)
ORDER BY TotalSales