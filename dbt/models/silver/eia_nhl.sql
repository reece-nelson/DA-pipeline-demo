{{ config(
    materialized='table',
    schema='silver'
) }}

select 
    eia.*,
    coalesce(nhl.team_name, 'no_team_found') as team_name
from {{ source('bronze', 'raw_eia') }} as eia
left join {{ source('bronze', 'raw_nhl_us_teams') }} as nhl
    on eia.stateid = nhl.state_id
