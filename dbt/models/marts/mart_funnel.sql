select
    lh.lead_history_id,
    lh.tenant_id,
    t.name as tenant_name,
    lh.customer_profile_id,
    cp.first_name,
    cp.last_name,
    fs.name as from_stage_name,
    fs.sort_order as from_stage_order,
    ts.name as to_stage_name,
    ts.sort_order as to_stage_order,
    lh.actor,
    lh.actor_id,
    au.first_name as actor_first_name,
    au.last_name as actor_last_name,
    lh.entered_at,
    lh.exited_at,
    lh.duration_minutes,
    lh.created_at
from {{ ref('stg_leadhistories') }} lh
left join {{ ref('stg_tenants') }} t on lh.tenant_id = t.tenant_id
left join {{ ref('stg_customerprofiles') }} cp on lh.customer_profile_id = cp.customer_profile_id
left join {{ ref('stg_stages') }} fs on lh.from_stage_id = fs.stage_id
left join {{ ref('stg_stages') }} ts on lh.to_stage_id = ts.stage_id
left join {{ ref('stg_users') }} au on lh.actor_id = au.user_id
