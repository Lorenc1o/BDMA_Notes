SELECT CAST(SUM((Unitprice-Discount)*Quantity) AS int) as TotalSales, E.FirstName as Name, E.LastName as SecondName, YEAR(OrderDate) Year
FROM Orders O
JOIN [Order Details] OD ON OD.OrderID=O.OrderID
JOIN Employees E ON O.EmployeeID=E.EmployeeID
GROUP BY E.FirstName, E.LastName, YEAR(OrderDate)
ORDER BY TotalSales