select group_type, count(group_type)
from projects_group
group by group_type;
