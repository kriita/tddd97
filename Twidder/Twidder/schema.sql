create table user_data(email varchar(100), password varchar(10), 
					name varchar(30), familyName varchar(30),
					gender varchar(30), city varchar(30),
					country varchar(30));

create table logged_in(email varchar(100), token varchar(100));

create table messages(sender varchar(100), message varchar(250), target varchar(100));