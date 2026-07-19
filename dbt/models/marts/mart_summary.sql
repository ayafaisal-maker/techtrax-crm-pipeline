select
    t.tenant_id,
    t.name as tenant_name,

    (select count(distinct customer_profile_id) from {{ ref('stg_customerprofiles') }} cp where cp.tenant_id = t.tenant_id) as total_leads,
    (select count(distinct customer_profile_id) from {{ ref('stg_customerprofiles') }} cp where cp.tenant_id = t.tenant_id and cp.deal_status = 'open') as open_leads,
    (select count(distinct customer_profile_id) from {{ ref('stg_customerprofiles') }} cp where cp.tenant_id = t.tenant_id and cp.deal_status = 'won') as won_leads,
    (select count(distinct customer_profile_id) from {{ ref('stg_customerprofiles') }} cp where cp.tenant_id = t.tenant_id and cp.deal_status = 'lost') as lost_leads,
    (select count(distinct customer_profile_id) from {{ ref('stg_customerprofiles') }} cp where cp.tenant_id = t.tenant_id and cp.assigned_to is null) as unassigned_leads,

    safe_divide(
        (select count(distinct customer_profile_id) from {{ ref('stg_customerprofiles') }} cp where cp.tenant_id = t.tenant_id and cp.deal_status = 'won'),
        (select count(distinct customer_profile_id) from {{ ref('stg_customerprofiles') }} cp where cp.tenant_id = t.tenant_id)
    ) * 100 as win_rate_pct,

    (select count(distinct user_id) from {{ ref('stg_users') }} u where u.tenant_id = t.tenant_id) as total_agents,
    (select count(distinct stage_id) from {{ ref('stg_stages') }} s where s.tenant_id = t.tenant_id) as total_stages,
    (select count(distinct lead_note_id) from {{ ref('stg_leadnotes') }} ln where ln.tenant_id = t.tenant_id) as total_notes,
    (select count(distinct notification_id) from {{ ref('stg_notifications') }} n where n.tenant_id = t.tenant_id) as total_notifications,
    (select count(distinct notification_id) from {{ ref('stg_notifications') }} n where n.tenant_id = t.tenant_id and not n.is_read) as unread_notifications
from {{ ref('stg_tenants') }} t
