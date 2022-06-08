select
  *
from
  executives
where
  id in (
    select
      executive_id
    from
      executive_terms
    where
      type = 'prez'
  )