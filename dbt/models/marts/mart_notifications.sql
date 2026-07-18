select
    n.notification_id,
    n.tenant_id,
    t.name as tenant_name,
    n.type,
    n.title,
    n.module,
    n.urgency,
    n.is_read,
    n.receiver_id,
    r.first_name as receiver_first_name,
    r.last_name as receiver_last_name,
    n.sender_id,
    sd.first_name as sender_first_name,
    sd.last_name as sender_last_name,
    n.created_at,
    n.updated_at
from {{ ref('stg_notifications') }} n
left join {{ ref('stg_tenants') }} t on n.tenant_id = t.tenant_id
left join {{ ref('stg_users') }} r on n.receiver_id = r.user_id
left join {{ ref('stg_users') }} sd on n.sender_id = sd.user_id
where n.is_soft_deleted = false
