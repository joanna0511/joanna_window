CREATE TABLE IF NOT EXISTS student (
	student_id Serial Primary Key,
   name VARCHAR(20) not null,
   major VARCHAR(20)
 );

drop table student;
drop table youbike;

select * from youbike;