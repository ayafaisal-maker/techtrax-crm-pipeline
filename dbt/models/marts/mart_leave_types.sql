select
    lt.leave_type_id,
    lt.tenant_id,
    t.name as tenant_name,
    lt.slug,
    lt.name,
    lt.description,
    lt.is_paid,
    lt.is_active,
    lt.is_system_reserved,
    lt.balance,
    lt.is_soft_deleted,
    lt.created_at,
    lt.updated_at
from {{ ref('stg_crmleavetypes') }} lt
left join {{ ref('stg_tenants') }} t on lt.tenant_id = t.tenant_id
