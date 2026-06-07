with inv as (
    select * from {{ ref('int_inventory_vs_sales') }}
)

select
    store_id,
    store_name,
    product_id,
    product_name,
    product_category,
    product_cost_usd,
    stock_on_hand,
    total_units_sold,
    avg_daily_units_sold,

   
    round(stock_on_hand / nullif(avg_daily_units_sold, 0), 0)       as days_of_stock_remaining,

    
    round(stock_on_hand * product_cost_usd, 2)                      as inventory_value_usd,

    -
    case 
        when stock_on_hand = 0 then true else false 
    end                                                             as is_out_of_stock,

    
    case
        when stock_on_hand > 50
        and avg_daily_units_sold < 0.5
        then true else false
    end                                                             as is_dead_stock,

    
    case
        when round(stock_on_hand / nullif(avg_daily_units_sold, 0), 0) < 7
        and stock_on_hand > 0
        then true else false
    end                                                             as is_low_stock

from inv