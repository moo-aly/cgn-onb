DROP TABLE IF EXISTS patient;
DROP TABLE IF EXISTS claim;

create table patient(
	id INTEGER primary key autoincrement,
	name text,
	email text,
	username char(255),
	mobile text
);

create table claim(
	id INTEGER primary key autoincrement,
	reason text,
	submission_date date,
	total_value float,
	file_name text,
	patient_id integer,
	CONSTRAINT patient_id_fk FOREIGN KEY(patient_id) REFERENCES patient(id)
);
