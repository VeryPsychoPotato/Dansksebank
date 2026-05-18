--3.1

SELECT
    c.customer_id,
    c.country,
    COUNT(a.agreement_id) AS agreement_count,
    SUM(a.monthly_payment) AS total_monthly_exposure
FROM customers c
JOIN agreements a
    ON c.customer_id = a.customer_id
WHERE a.status = 'ACTIVE'
  AND a.currency = 'EUR'
  AND c.segment = 'CORPORATE'
GROUP BY c.customer_id, c.country
HAVING COUNT(a.agreement_id) >= 2
ORDER BY total_monthly_exposure DESC;

--3.2

SELECT
    a.asset_type,
    ROUND(100.0 * SUM(CASE WHEN p.is_late THEN 1 ELSE 0 END)/ COUNT(*), 2) AS late_payment_rate
FROM payments p
JOIN agreements a
    ON p.agreement_id = a.agreement_id
GROUP BY a.asset_type
HAVING COUNT(*) > 100;

--3.3

-- finds last payment date for each customer_id

WITH last_payments AS (
    SELECT
        a.customer_id,
        MAX(p.payment_date) AS last_payment_date
    FROM agreements a
    LEFT JOIN payments p
        ON a.agreement_id = p.agreement_id
    GROUP BY a.customer_id
),
active_customers AS (
    SELECT DISTINCT customer_id
    FROM agreements
    WHERE status = 'ACTIVE'
)
SELECT
    c.customer_id,
    c.segment,
    lp.last_payment_date
FROM customers c
JOIN active_customers ac
    ON c.customer_id = ac.customer_id
LEFT JOIN last_payments lp
    ON c.customer_id = lp.customer_id
WHERE
    lp.last_payment_date IS NULL
    OR lp.last_payment_date < CURRENT_DATE - INTERVAL '90 days';

--3.4

SELECT *
FROM agreements a
--for every row in agreements, sql does subquery count(*) in payments, and if those tables are big, it has to do a lot of calculations, which makes it perform very slowly
-- correct way to join agreement and payment tables and use group by and having clause

WHERE (SELECT COUNT(*) FROM payments p 
       WHERE p.agreement_id = a.agreement_id) > 5

--UPPER function converts string to string upper-case and because of that data manipulation it prevents of using index of column status
-- just use a.status = 'ACTIVE' and if there is inconsistencies fix it on the database level
AND UPPER(a.status) = 'ACTIVE'

-- same problem as previous, function prevents using column index, just use
--a.start_date >= 2023-01-01
-- AND a.start_date < 2024-01-01
AND YEAR(a.start_date) = 2023;

--New better sql 

SELECT a.*
FROM agreements a
JOIN payments p ON p.agreement_id = a.agreement_id
WHERE a.status = 'ACTIVE'
  AND a.start_date >= '2023-01-01'
  AND a.start_date < '2024-01-01'
GROUP BY a.agreement_id, a.status, a.start_date 
HAVING COUNT(p.agreement_id) > 5
