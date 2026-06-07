{{ config(
    materialized='view'
)}}

with source as (
    select * from {{ source('raw', 'inventory') }}
),

cleaned as (
    select
        Store_ID                 as store_id,
        Product_ID               as product_id,
        Stock_On_Hand            as stock_on_hand

    from source
)

select * from cleaned