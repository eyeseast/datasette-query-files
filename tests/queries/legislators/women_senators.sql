select
  legislators.id,
  legislators.name,
  legislator_terms.party,
  count(*) as terms
from
  legislators
  inner join legislator_terms on legislators.id = legislator_terms.legislator_id
where
  legislator_terms.type = 'sen'
  and legislators.bio_gender = 'F'
group by
  legislators.id
order by
  terms desc