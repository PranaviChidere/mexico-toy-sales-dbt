with source as (
    select * from {{ source('raw','products') }}
),
cleaned as  (
    select 
    Product_ID as product_id ,
    Product_Name as product_name,
    Product_Category as product_category,
    cast(replace(Product_Cost,'$','') as decimal(10,2)) as product_cost_usd,
    cast(replace(Product_Price,'$','') as decimal(10,2)) as product_price_usd,
    cast(replace(Product_Price,'$','') as decimal(10,2))-cast(replace(Product_Cost,'$','') as decimal(10,2)) as unit_margin_usd

    from source
)
select * from cleaned