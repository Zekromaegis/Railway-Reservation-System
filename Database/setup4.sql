-- This creates an event that triggers daily automatically.

call t_status_creator(CURRENT_DATE);

drop event if exists trainstatus_creation_event;
create event trainstatus_creation_event
on schedule 
	every 1 day
comment "Create new Train Status for the next day!"
do
	call t_status_creator(CURRENT_DATE + INTERVAL 1 DAY);