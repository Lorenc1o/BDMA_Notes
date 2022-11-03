SELECT CAST(SUM((Unitprice-Discount)*Quantity) AS int) as TotalSales, MONTH(OrderDate) Month, YEAR(OrderDate) Year, ShipCountry
FROM Orders O
JOIN [Order Details] OD ON OD.OrderID=O.OrderID
JOIN Employees E ON O.EmployeeID=E.EmployeeID
GROUP BY ShipCountry, MONTH(OrderDate), YEAR(OrderDate)
ORDER BY TotalSales