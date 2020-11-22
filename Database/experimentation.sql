select * from station natural join route where train_id = 1 order by id;
select station_name from station natural join route natural join train where train_name = "Gujarat Mail" order by id;

select *
from station natural join route
where train_id = (
	select train_id
    from train
    where train_name = "Gujarat Mail"
);

create view train_station_join as select * from train natural join route natural join station;

/* select s1.train_id, s1.train_name, s1.start_time, s1.end_time, s1.station_name, s1.seat_cost, s2.station_name */
select *
from (
	select *
	from train natural join route natural join station
	where train_type = 'S' and station_name = 'Surat'
) as s1 inner join (
	select *
	from train natural join route natural join station
	where train_type = 'S' and station_name = 'Mumbai'
) as s2 on s1.train_name = s2.train_name
where s1.id < s2.id;

drop procedure if exists general_search;
delimiter //
create procedure general_search(in train_t char(1), in station_a varchar(30), in station_b varchar(30))
begin
	select s1.train_id, s1.train_type, s1.train_name,
    s1.no_of_seats, s1.start_time, s1.end_time, s1.seat_cost,
    s1.end_station, s1.start_station
	from (
		select *
		from train natural join route natural join station
		where train_type = train_t and station_name = station_a
	) as s1 inner join (
		select *
		from train natural join route natural join station
		where train_type = train_t and station_name = station_b
	) as s2 on s1.train_id = s2.train_id
	where s1.id < s2.id;
end //
delimiter ;

call general_search("s","Surat","Mumbai");

SELECT *
FROM `train`
INNER JOIN `route` ON (`train`.`train_id` = `route`.`train_id`)
INNER JOIN `station` ON (`route`.`station_id` = `station`.`station_id`)
INNER JOIN `route` T4 ON (`train`.`train_id` = T4.`train_id`)
WHERE (`station`.`station_name` = "Mumbai" AND T4.`id` < (
		SELECT route.id
		from train natural join route natural join station
		WHERE station_name = "Surat"
    )
);

select *
from train natural join route natural join station
where train_type = 'S'
group by train_name
having station_name in ("Surat","Mumbai")
order by id;