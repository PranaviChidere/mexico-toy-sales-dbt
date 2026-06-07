with inventory as (
    select * from {{ ref('stg_maven_toys_inventory') }}
),

sales as (
    select * from {{ ref('stg_maven_toys_sales') }}
),

products as (
    select * from {{ ref('stg_maven_toys_products') }}
),

stores as (
    select * from {{ ref('stg_maven_toys_stores') }}
),

joined as (
    select
        i.store_id,
        st.store_name,
        i.product_id,
        p.product_name,
        p.product_category,
        p.product_cost_usd,
        i.stock_on_hand,
        coalesce(sum(s.units), 0)                                       as total_units_sold,

        -- avg daily units sold based on total sales days
        round(coalesce(sum(s.units), 0) / nullif(count(distinct s.sale_date), 0), 2) as avg_daily_units_sold

    from inventory i
    left join sales s
        on i.store_id = s.store_id
        and i.product_id = s.product_id
    left join products p
        on i.product_id = p.product_id
    left join stores st
        on i.store_id = st.store_id
    group by
        i.store_id,
        st.store_name,
        i.product_id,
        p.product_name,
        p.product_category,
        p.product_cost_usd,
        i.stock_on_hand
)

select * from joined