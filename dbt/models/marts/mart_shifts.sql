select
    s.shift_id,
    s.tenant_id,
    t.name as tenant_name,
    s.user_id,
    u.first_name,
    u.last_name,
    s.shift_template_id,
    st.name as shift_template_name,
    s.is_soft_deleted,
    s.created_at,
    s.updated_at
from {{ ref('stg_crmshifts') }} s
left join {{ ref('stg_tenants') }} t on s.tenant_id = t.tenant_id
left join {{ ref('stg_users') }} u on s.user_id = u.user_id
left join {{ ref('stg_crmshifttemplates') }} st on s.shift_template_id = st.shift_template_id
