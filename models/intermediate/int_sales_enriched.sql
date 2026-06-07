with sales as (
    select * from {{ ref('stg_maven_toys_sales') }}
),

products as (
    select * from {{ ref('stg_maven_toys_products') }}
),

stores as (
    select * from {{ ref('stg_maven_toys_stores') }}
),

enriched as (
    select
        s.sale_id,
        s.sale_date,
        s.units,

        -- store info
        s.store_id,
        st.store_name,
        st.store_city,
        st.store_location,

        -- product info
        s.product_id,
        p.product_name,
        p.product_category,
        p.product_cost_usd,
        p.product_price_usd,
        p.unit_margin_usd,

        -- calculated financials
        s.units * p.product_price_usd   as revenue,
        s.units * p.product_cost_usd    as cost,
        s.units * p.unit_margin_usd     as profit

    from sales s
    left join products p on s.product_id = p.product_id
    left join stores  st on s.store_id   = st.store_id
)

select * from enriched