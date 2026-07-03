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