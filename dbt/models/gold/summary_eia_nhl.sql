{{ config(
    materialized='table',
    schema='gold'
) }}


SELECT
    period,
    stateid,
    statedescription,
    MAX(team_name) AS team_name,
    AVG(price)     AS avg_price,
    SUM(price)     AS total_price,
    MIN(price)     AS min_price,
    MAX(price)     AS max_price,
    AVG(revenue)   AS avg_revenue,
    SUM(revenue)   AS total_revenue,
    AVG(sales)     AS avg_sales,
    SUM(sales)     AS total_sales
FROM {{ source('silver', 'eia_nhl') }}
GROUP BY period, stateid, stateDescription
ORDER BY period, stateid