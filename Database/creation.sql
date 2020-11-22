create table Station (
	station_id int not null auto_increment,
    station_name varchar(30) not null,
    primary key ( station_id )
);

/* train_type {Sleeper : S, Chair : C} */ 
create table Train (
	train_id int not null auto_increment,
    train_type char not null default 'C',
    check ( train_type in ( 'C', 'S' ) ),
    train_name varchar(20) not null unique,
    no_of_seats int not null default 100,
    check (no_of_seats > 0),
    start_station int not null,
    end_station int not null,
    start_time time not null,
    end_time time not null,
    seat_cost int not null,
    check (seat_cost > 0),
    primary key ( train_id ),
    foreign key ( start_station ) references Station( station_id ),
    foreign key ( end_station ) references Station( station_id )
);

create table Route (
	route_id int not null auto_increment,
	train_id int not null,
    station_id int not null,
    primary key ( route_id ),
    unique key ( train_id, station_id ),
    foreign key ( train_id ) references Train( train_id ),
    foreign key ( station_id ) references Station( station_id )
);

create table TrainStatus (
	seats_booked int not null default 0,
    train_id int not null,
    departure_date date not null,
    seat_cost int not null,
    total_seats int not null,
    waiting int not null default 0,
    primary key ( train_id, departure_date ),
    foreign key ( train_id ) references Train( train_id ),
    check (seats_booked >= 0),
    check (seat_cost > 0),
    check (total_seats >= 0),
    check (waiting >= 0)
);

/* W : Waiting, C : Confirmed */
create table Ticket (
	ticket_id int not null auto_increment,
    ticket_status char not null default 'W',
    check (ticket_status in ( 'W', 'C' )),
    seat_cost int not null,
    seat_no int not null,
    check (seat_cost > 0),
    user_id int not null,
    train_id int not null,
    departure_date date not null,
    primary key ( ticket_id ),
    foreign key ( train_id, departure_date ) references TrainStatus( train_id, departure_date ) on delete cascade,
    foreign key ( user_id ) references auth_user( id )
);