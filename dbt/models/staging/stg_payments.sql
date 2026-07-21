select
    _id as payment_id,
    tenantId as tenant_id,
    patientId as patient_id,
    doctorId as doctor_id,
    appointmentId as appointment_id,

    requiredAmount as required_amount,
    paidAmount as paid_amount,
    discount,
    totalPending as total_pending,

    status,
    method,
    isDelivered as is_delivered,
    noPackage as no_package,
    note,

    products,

    isSoftDeleted as is_soft_deleted,
    createdBy as created_by,
    updatedBy as updated_by,
    createdAt as created_at,
    updatedAt as updated_at
from {{ source('techtrax_raw', 'payments') }}
qualify row_number() over (partition by _id order by updatedAt desc) = 1
