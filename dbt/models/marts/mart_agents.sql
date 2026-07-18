select
    u.user_id,
    u.tenant_id,
    t.name as tenant_name,
    u.first_name,
    u.last_name,
    u.email,
    u.phone,
    u.role,
    u.status,
    tm.name as team_name,
    count(cp.customer_profile_id) as assigned_leads_count,
    countif(cp.deal_status = 'open') as open_leads_count,
    countif(cp.deal_status = 'won') as won_leads_count,
    countif(cp.deal_status = 'lost') as lost_leads_count,
    sum(cp.follow_up_count) as total_follow_ups
from {{ ref('stg_users') }} u
left join {{ ref('stg_tenants') }} t on u.tenant_id = t.tenant_id
left join {{ ref('stg_teams') }} tm on u.team_id = tm.team_id
left join {{ ref('stg_customerprofiles') }} cp
    on cp.assigned_to = u.user_id
    and cp.tenant_id = u.tenant_id
group by
    u.user_id, u.tenant_id, t.name, u.first_name, u.last_name, u.email, u.phone, u.role, u.status, tm.name
