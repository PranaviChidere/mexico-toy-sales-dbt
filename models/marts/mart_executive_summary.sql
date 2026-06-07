with base as (
    select * from {{ ref('int_sales_enriched') }}
)

select
    date_trunc('month', sale_date)                              as month,
    year(sale_date)                                             as year,
    monthname(sale_date)                                        as month_name,

    sum(units)                                                  as total_units_sold,
    sum(revenue)                                                as total_revenue,
    sum(cost)                                                   as total_cost,
    sum(profit)                                                 as total_profit,
    round(sum(profit)/nullif(sum(revenue),0)*100, 2)            as profit_margin_pct,
    count(distinct sale_id)                                     as total_transactions,
    count(distinct store_id)                                    as active_stores,
    count(distinct product_id)                                  as active_products

from base
group by
    date_trunc('month', sale_date), year(sale_date), monthname(sale_date)
order by month