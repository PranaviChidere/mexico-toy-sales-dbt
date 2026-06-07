with base as (
    select * from {{ ref('int_sales_enriched') }}
)

select
    sale_date,
    year(sale_date)                     as year,
    month(sale_date)                    as month_number,
    store_id,
    store_name,
    store_city,
    store_location,
    product_id,
    product_name,
    product_category,

    sum(units)                          as total_units_sold,
    sum(revenue)                        as total_revenue,
    sum(cost)                           as total_cost,
    sum(profit)                         as total_profit,
    round(sum(profit)/nullif(sum(revenue),0)*100, 2) as profit_margin_pct

from base
group by
    sale_date, year(sale_date), month(sale_date),
    store_id, store_name, store_city, store_location,
    product_id, product_name, product_category