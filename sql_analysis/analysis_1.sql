SELECT
    promo_group,
    COUNT(*) AS customers,
    ROUND(AVG(purchase_amount_usd), 2) AS avg_spend,
    ROUND(AVG(previous_purchases), 1) AS avg_previous_purchases,
    ROUND(AVG(review_rating), 2) AS avg_rating
FROM customer_behavior
GROUP BY promo_group
ORDER BY avg_previous_purchases DESC;

SELECT
    loyalty_tier,
    promo_group,
    COUNT(*) AS customers,
    ROUND(AVG(purchase_amount_usd), 2) AS avg_spend
FROM customer_behavior
GROUP BY loyalty_tier, promo_group
ORDER BY loyalty_tier, avg_spend DESC;

SELECT * FROM customer_behavior;

--Operational diagnostics
SELECT
    shipping_type,
    ROUND(AVG(review_rating), 2) AS avg_rating,
    SUM(low_rating_flag) AS low_rating_count,
    COUNT(*) AS total_orders,
    ROUND(100.0 * SUM(low_rating_flag) / COUNT(*), 1) AS pct_low_rating
FROM customer_behavior
GROUP BY shipping_type
ORDER BY pct_low_rating DESC;

--category wise average spend
SELECT 
	category,
	ROUND(AVG(purchase_amount_usd),2) AS category_avg_spend
FROM customer_behavior
GROUP BY category
ORDER BY category_avg_spend DESC;

--Above-Average Spenders by Category
WITH category_avgs AS(SELECT 
	customer_id,
	purchase_amount_usd,
	category,
	ROUND(AVG(purchase_amount_usd) OVER (PARTITION BY category), 2) AS category_avg_spend
FROM customer_behavior)
SELECT * FROM category_avgs
WHERE purchase_amount_usd > category_avg_spend
ORDER BY category, purchase_amount_usd DESC;
