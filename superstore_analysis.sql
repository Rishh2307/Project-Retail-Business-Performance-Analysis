SELECT * FROM superstore_db.superstore_sales;

SELECT COUNT(*) AS total_rows 
FROM superstore_sales;

SELECT * FROM superstore_sales 
LIMIT 10;

SELECT DISTINCT Category 
FROM superstore_sales;

SELECT DISTINCT Region 
FROM superstore_sales;

SELECT Order_ID, Customer_Name, Sales, Profit
FROM superstore_sales
ORDER BY Sales DESC
LIMIT 5;

SELECT Order_ID, Customer_Name, Sales, Profit
FROM superstore_sales
ORDER BY Profit ASC
LIMIT 5;

select count(*) AS row_count from superstore_sales;

-- 1)Profit by Category & Sub-Category
SELECT 
    Category, 
    Sub_Category,
    SUM(Sales) AS total_sales,
    SUM(Profit) AS total_profit,
    ROUND(SUM(Profit)/NULLIF(SUM(Sales),0)*100,2) AS profit_margin_pct
FROM superstore_sales
GROUP BY Category, Sub_Category
ORDER BY total_profit ASC;

-- 2)Region-wise Profitability
SELECT 
    Region,
    SUM(Sales) AS total_sales,
    SUM(Profit) AS total_profit,
    ROUND(SUM(Profit)/NULLIF(SUM(Sales),0)*100,2) AS profit_margin_pct
FROM superstore_sales
GROUP BY Region
ORDER BY total_profit DESC;

-- 3)Monthly Sales & Priofit Trend 
SELECT 
    YEAR(Order_Date)  AS year, 
    MONTH(Order_Date) AS month,
    SUM(Sales)  AS total_sales, 
    SUM(Profit) AS total_profit
FROM superstore_sales
GROUP BY YEAR(Order_Date), MONTH(Order_Date)
ORDER BY year, month;

-- 4)Discount Impact (Banned)
SELECT 
    CASE 
        WHEN Discount = 0 THEN '0%'
        WHEN Discount <= 0.10 THEN '0-10%'
        WHEN Discount <= 0.20 THEN '10-20%'
        WHEN Discount <= 0.30 THEN '20-30%'
        ELSE '>30%'
    END AS discount_band,
    SUM(Sales)  AS total_sales,
    SUM(Profit) AS total_profit,
    ROUND(SUM(Profit)/NULLIF(SUM(Sales),0)*100,2) AS profit_margin_pct
FROM superstore_sales
GROUP BY discount_band
ORDER BY discount_band;

-- 5) Top 10 Loss Making Products
SELECT 
    Product_Name,
    SUM(Sales)  AS total_sales,
    SUM(Profit) AS total_profit
FROM superstore_sales
GROUP BY Product_Name
HAVING SUM(Profit) < 0
ORDER BY total_profit ASC
LIMIT 10;