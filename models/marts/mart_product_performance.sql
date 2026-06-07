with base as (
    select * from {{ ref('int_sales_enriched') }}
)

select
    product_id,
    product_name,
    product_category,
    product_cost_usd,
    product_price_usd,
    unit_margin_usd,

    sum(units)                                          as total_units_sold,
    sum(revenue)                                        as total_revenue,
    sum(cost)                                           as total_cost,
    sum(profit)                                         as total_profit,
    round(sum(profit)/nullif(sum(revenue),0)*100, 2)    as profit_margin_pct,
    count(distinct sale_date)                           as active_selling_days

from base
group by
    product_id, product_name, product_category,
    product_cost_usd, product_price_usd, unit_margin_usd