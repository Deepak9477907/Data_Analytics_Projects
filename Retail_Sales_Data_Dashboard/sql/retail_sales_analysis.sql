-- Load the cleaned Superstore CSV into a table named superstore.

SELECT COUNT(*) AS rows,
       COUNT(DISTINCT order_id) AS orders,
       COUNT(DISTINCT customer_id) AS customers,
       ROUND(SUM(sales),2) AS total_sales,
       ROUND(SUM(profit),2) AS total_profit,
       SUM(quantity) AS total_quantity,
       ROUND(SUM(profit)/NULLIF(SUM(sales),0)*100,2) AS profit_margin_pct
FROM superstore;

SELECT region, ROUND(SUM(sales),2) AS sales,
       ROUND(SUM(profit),2) AS profit
FROM superstore
GROUP BY region ORDER BY sales DESC;

SELECT category, sub_category,
       ROUND(SUM(sales),2) AS sales,
       ROUND(SUM(profit),2) AS profit
FROM superstore
GROUP BY category, sub_category
ORDER BY sales DESC;

SELECT product_name, ROUND(SUM(sales),2) AS sales,
       ROUND(SUM(profit),2) AS profit
FROM superstore
GROUP BY product_name
ORDER BY sales DESC LIMIT 10;

SELECT product_name, ROUND(SUM(profit),2) AS profit
FROM superstore
GROUP BY product_name
ORDER BY profit ASC LIMIT 10;

SELECT segment, ROUND(SUM(sales),2) AS sales,
       ROUND(SUM(profit),2) AS profit
FROM superstore
GROUP BY segment ORDER BY sales DESC;
