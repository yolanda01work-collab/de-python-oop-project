/* Revenue by Day */
SELECT
    order_date,
    SUM(net_sales) AS total_revenue
FROM fact_sales
GROUP BY order_date
ORDER BY order_date;


/* Products with Highest Revenue */
SELECT
    p.product_name,
    SUM(f.net_sales) AS total_revenue
FROM fact_sales f
JOIN dim_products p
    ON f.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_revenue DESC;


/* Region with Highest Sales */
SELECT
    c.region,
    SUM(f.net_sales) AS total_revenue
FROM fact_sales f
JOIN dim_customers c
    ON f.customer_id = c.customer_id
GROUP BY c.region
ORDER BY total_revenue DESC;


/* Customer Lifetime Value */
SELECT
    c.customer_id,
    c.customer_name,
    SUM(f.net_sales) AS lifetime_value
FROM fact_sales f
JOIN dim_customers c
    ON f.customer_id = c.customer_id
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY lifetime_value DESC;


/* Rejected Records */
SELECT *
FROM etl_rejected_sales;