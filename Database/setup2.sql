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

drop procedure if exists t_status_creator;
delimiter $$
create procedure t_status_creator(in d date)
begin
	insert into trainstatus2(seats_booked, train_id, departure_date, seat_cost, total_seats, waiting)
	select 0, train_id, d, seat_cost, no_of_seats, 0 from train;
end $$
delimiter ;

-- call t_status_creator("2020-11-09");
-- call t_status_creator("2020-11-10");
-- call t_status_creator("2020-11-11");
-- call t_status_creator("2020-11-12");
-- call t_status_creator("2020-11-13");
-- call t_status_creator("2020-11-14");
-- call t_status_creator("2020-11-15");
-- call t_status_creator("2020-11-16");
-- call t_status_creator("2020-11-17");
-- call t_status_creator("2020-11-18");
-- call t_status_creator("2020-11-19");
-- call t_status_creator("2020-11-20");