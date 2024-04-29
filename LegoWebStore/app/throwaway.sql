drop table if exists duplo;
create table duplo(
    id int not null auto_increment primary key,
    `size` int,
    colour varchar(6)
);