select
    ln.lead_note_id,
    ln.tenant_id,
    t.name as tenant_name,
    ln.customer_profile_id,
    cp.first_name,
    cp.last_name,
    ln.content,
    ln.author_id,
    au.first_name as author_first_name,
    au.last_name as author_last_name,
    ln.is_archived,
    ln.created_at,
    ln.updated_at
from {{ ref('stg_leadnotes') }} ln
left join {{ ref('stg_tenants') }} t on ln.tenant_id = t.tenant_id
left join {{ ref('stg_customerprofiles') }} cp on ln.customer_profile_id = cp.customer_profile_id
left join {{ ref('stg_users') }} au on ln.author_id = au.user_id
