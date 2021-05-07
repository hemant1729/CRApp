create table Program (
	program_id	serial primary key,
	prog_name	varchar(255) unique
);

create table Department (
	dept_id	serial primary key,
	dept_name	varchar(255) unique
);

create table Student (
	student_id 	serial primary key,    	
	roll_num	varchar(255) unique,
	name		varchar(255),
	year 		int,
	program_id	int,
	cpi		float(2),
	tot_credits	int,
	dept_id	int,
	foreign key (program_id) references Program(program_id),
	foreign key (dept_id) references Department(dept_id)
);

create table Instructor (
	instructor_id	serial primary key,
	roll_num	varchar(255) unique,
	instr_name	varchar(255),
	dept_id	int,
	foreign key (dept_id) references Department(dept_id)
);

create table Grade (
	grade_id	serial primary key,
	grade_name	varchar(255),
	value		int
);


create table Timeslot (
	time_slot_id	varchar(255) not null,
	day		varchar(255) not null,
	start_time	time not null,
	end_time	time not null
);


create table Course(
	course_id 	serial primary key,
	course_name	varchar(255) unique,
	dept_id	int,
	type		text,
	credits		int,
	foreign key (dept_id) references Department(dept_id)
);

create table Semester(
	sem_id		serial primary key,
	year		int,
	season		int
);

create table Tags (
	tag_id 		serial primary key,
	tag_name 	text
);

create table Interests (
	student_id 	int,
	tag_id		int,
	primary key (student_id, tag_id),
	foreign key (student_id) references Student(student_id),
	foreign key (tag_id) references Tags(tag_id)
);
create index Interests_student on Interests(student_id);

create table Course_tags (
	course_id	int,
	tag_id		int,
	primary key (course_id, tag_id),
	foreign key (course_id) references Course(course_id),
	foreign key (tag_id) references Tags(tag_id)
);
create index Course_tags_course on Course_tags(course_id);

create table Pre_req (
	course_id	int,
	prereq_id	int,
	foreign key (course_id) references Course(course_id),
	foreign key (prereq_id) references Course(course_id)
);

create table Course_semester (
	course_id	int,
	sem_id		int,
	instructor_id	int,
	time_slot_id	varchar(255),
	total		int,
	num_quiz	int,
	num_assgn	int,
	exam_toughness	int,
	assgn_toughness	int,
	overall_feel		int,
	project		int,
	help_availability 	int,
	working_hours		int,
	team_size 	int,
	primary key (course_id, sem_id, instructor_id),
	foreign key (course_id) references Course(course_id),
	foreign key (instructor_id) references Instructor(instructor_id),
	foreign key (sem_id) references Semester(sem_id)
);

create table Takes (
	take_id		serial primary key,
	student_id	int,
	sem_id		int,
	course_id	int,
	instructor_id	int,
	unique (course_id, sem_id,student_id,instructor_id),
	foreign key (student_id) references Student(student_id),
	foreign key (sem_id) references Semester(sem_id),
	foreign key (instructor_id) references Instructor(instructor_id),
	foreign key (course_id) references Course(course_id)
);

create table Core_courses (
	sem_id		int,
	dept_id	int,
	course_id	int,
	foreign key (sem_id) references Semester(sem_id),
	foreign key (dept_id) references Department(dept_id),
	foreign key (course_id) references Course(course_id)
);

create table Review(
	take_id		int,
	grade_id	int,
	num_quiz		text,
	num_assgn		text,
	exam_toughness	text,
	assgn_toughness	text,
	overall_feel		text,
	project			text,
	project_desc	text,
	teacher_review	text,
	help_availability	text,
	working_hours		text,
	team_size		text,
	followup_course_id	int,
	primary key (take_id),
	foreign key (take_id) references Takes(take_id),
	foreign key (grade_id) references Grade(grade_id),
	foreign key (followup_course_id) references Course(course_id)
);

create table DGSEC(
	student_id	int,
	sem_id		int,
	dept_id	int,
	foreign key (student_id) references Student(student_id),
	foreign key (sem_id) references Semester(sem_id),
	foreign key (dept_id) references Department(dept_id)
);


create table Student_tag_weights (
	student_id	int,
	tag_id		int,
	weight		float(2),
	count		int,
	in_interests int,
	foreign key (student_id) references Student(student_id),
	foreign key (tag_id) references Tags(tag_id)
);
create index Student_tag_weights_student on Student_tag_weights(student_id);

create table Student_sem (
	student_id  int primary key,
	sem_id		int,
	foreign key (student_id) references Student(student_id),
	foreign key (sem_id) references Semester(sem_id)
);

create table Messages (
	sender_id 	int,
	receiver_id	int,
	message	text,
	foreign key (sender_id) references Student(student_id),
	foreign key (receiver_id) references Student(student_id)
);
create index Messages_sender on Messages(sender_id);

create table Issues(
	issue_id	serial primary key,
	student_id	int,
	date		timestamp,
	issue		text,
	status 		int,
	reply		text,
	foreign key (student_id) references Student(student_id)
);
create index Issues_student on Issues(student_id);
