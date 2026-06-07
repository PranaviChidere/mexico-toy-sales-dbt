with base as (
    select * from {{ ref('int_sales_enriched') }}
)

select
    store_id,
    store_name,
    store_city,
    store_location,

    sum(units)                                          as total_units_sold,
    sum(revenue)                                        as total_revenue,
    sum(cost)                                           as total_cost,
    sum(profit)                                         as total_profit,
    round(sum(profit)/nullif(sum(revenue),0)*100, 2)    as profit_margin_pct,
    count(distinct sale_date)                           as active_selling_days,
    round(sum(revenue)/nullif(count(distinct sale_date),0), 2) as avg_daily_revenue

from base
group by
    store_id, store_name, store_city, store_location