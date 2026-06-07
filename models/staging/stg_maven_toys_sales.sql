with source as (
    select * from {{ source('raw', 'sales') }}
),

cleaned as (
    select
        Sale_ID                  as sale_id,
        cast(Date as date)       as sale_date,
        Store_ID                 as store_id,
        Product_ID               as product_id,
        Units                    as units

    from source
)

select * from cleaned