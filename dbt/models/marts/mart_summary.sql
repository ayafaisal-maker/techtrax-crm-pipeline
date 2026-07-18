select
    t.tenant_id,
    t.name as tenant_name,
    count(distinct cp.customer_profile_id) as total_leads,
    countif(cp.deal_status = 'open') as open_leads,
    countif(cp.deal_status = 'won') as won_leads,
    countif(cp.deal_status = 'lost') as lost_leads,
    countif(cp.assigned_to is null) as unassigned_leads,
    count(distinct u.user_id) as total_agents,
    count(distinct s.stage_id) as total_stages,
    count(distinct ln.lead_note_id) as total_notes,
    count(distinct n.notification_id) as total_notifications,
    countif(not n.is_read) as unread_notifications
from {{ ref('stg_tenants') }} t
left join {{ ref('stg_customerprofiles') }} cp on cp.tenant_id = t.tenant_id
left join {{ ref('stg_users') }} u on u.tenant_id = t.tenant_id
left join {{ ref('stg_stages') }} s on s.tenant_id = t.tenant_id
left join {{ ref('stg_leadnotes') }} ln on ln.tenant_id = t.tenant_id
left join {{ ref('stg_notifications') }} n on n.tenant_id = t.tenant_id
group by t.tenant_id, t.name
