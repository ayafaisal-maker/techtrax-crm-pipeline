select
    s.stage_id,
    s.tenant_id,
    t.name as tenant_name,
    s.name,
    s.slug,
    s.sort_order,
    s.stage_type,
    s.sla_hours,
    s.status,
    s.is_soft_deleted,
    s.created_at,
    s.updated_at
from {{ ref('stg_stages') }} s
left join {{ ref('stg_tenants') }} t on s.tenant_id = t.tenant_id
order by s.tenant_id, s.sort_order
