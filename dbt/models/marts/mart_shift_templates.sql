select
    st.shift_template_id,
    st.tenant_id,
    t.name as tenant_name,
    st.name,
    st.description,
    st.is_system_template,
    st.is_soft_deleted,
    st.created_at,
    st.updated_at
from {{ ref('stg_crmshifttemplates') }} st
left join {{ ref('stg_tenants') }} t on st.tenant_id = t.tenant_id
