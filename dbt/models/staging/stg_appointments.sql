select
    _id as appointment_id,
    tenantId as tenant_id,
    patientId as patient_id,
    doctorId as doctor_id,

    appointmentDateTime as appointment_datetime,
    appointmentEndTime as appointment_end_time,
    duration,

    status,
    sessionType as session_type,
    visitType as visit_type,
    protocol,
    protocolId as protocol_id,
    protocolIds as protocol_ids,

    isFirstVisit as is_first_visit,
    isFollowUp as is_follow_up,
    isWalkIn as is_walk_in,
    isBillAble as is_bill_able,

    cancelReason as cancel_reason,
    canceledAt as canceled_at,
    canceledBy as canceled_by,

    recommendedProtocols as recommended_protocols,
    to_json_string(formSubmissions) as form_submissions_json,

    isSoftDeleted as is_soft_deleted,
    createdAt as created_at,
    updatedAt as updated_at
from {{ source('techtrax_raw', 'appointments') }}
qualify row_number() over (partition by _id order by updatedAt desc) = 1
