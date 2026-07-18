select
    c.clock_record_id,
    c.tenant_id,
    t.name as tenant_name,
    c.user_id,
    u.first_name,
    u.last_name,
    c.day,
    c.clock_in,
    c.clock_out,
    c.status,
    c.shift_minutes,
    c.worked_minutes,
    c.is_soft_deleted,
    c.created_at,
    c.updated_at
from {{ ref('stg_crmclockrecords') }} c
left join {{ ref('stg_tenants') }} t on c.tenant_id = t.tenant_id
left join {{ ref('stg_users') }} u on c.user_id = u.user_id
