select
    cp.customer_profile_id,
    cp.tenant_id,
    t.name as tenant_name,
    cp.first_name,
    cp.last_name,
    cp.email,
    cp.phone,
    cp.is_soft_deleted,
    cp.deal_status,
    cp.priority,
    cp.follow_up_count,
    s.name as stage_name,
    s.sort_order as stage_order,
    ps.name as previous_stage_name,
    u.first_name as assigned_agent_first_name,
    u.last_name as assigned_agent_last_name,
    ub.first_name as assigned_by_first_name,
    ub.last_name as assigned_by_last_name,
    cp.entered_pipeline_at,
    cp.stage_entered_at,
    cp.first_contact_at,
    cp.last_contact_at,
    cp.last_activity_at,
    cp.deal_won_at,
    cp.deal_lost_at,
    cp.booking_date,
    cp.snoozed_at,
    cp.snooze_date,
    cp.crm_module_active,
    cp.cms_module_active,
    cp.custom_fields,
    cp.created_at,
    cp.updated_at
from {{ ref('stg_customerprofiles') }} cp
left join {{ ref('stg_tenants') }} t on cp.tenant_id = t.tenant_id
left join {{ ref('stg_stages') }} s on cp.stage_id = s.stage_id
left join {{ ref('stg_stages') }} ps on cp.previous_stage_id = ps.stage_id
left join {{ ref('stg_users') }} u on cp.assigned_to = u.user_id
left join {{ ref('stg_users') }} ub on cp.assigned_by = ub.user_id
