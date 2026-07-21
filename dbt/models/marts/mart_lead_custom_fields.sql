select
    cp.customer_profile_id,
    cp.tenant_id,
    t.name as tenant_name,

    cf.custom_field_id as field_id,
    cf.field_name,
    cf.label as field_label,
    cf.field_type,

    json_extract_scalar(field_json, '$.value') as field_value
from {{ ref('stg_customerprofiles') }} cp
left join {{ ref('stg_tenants') }} t on cp.tenant_id = t.tenant_id
cross join unnest(json_extract_array(cp.custom_fields)) as field_json
left join {{ ref('stg_customfields') }} cf
    on json_extract_scalar(field_json, '$.fieldId') = cf.custom_field_id
    and cf.tenant_id = cp.tenant_id
