drop table if exists worksOn;
drop table if exists controls;
drop table if exists project;
drop table if exists affiliation;
drop table if exists dptNEmp;
drop table if exists dptBudget;
drop table if exists dptLocations;
drop table if exists department;
drop table if exists supervision;
drop table if exists administrativeDependent;
drop table if exists administrativeLifecycle;
drop table if exists administrative;
drop table if exists engineerDiplomas;
drop table if exists engineerType;
drop table if exists engineer;
drop table if exists employeeAddress;
drop table if exists employeeSalary;
drop table if exists employeeLifecycle;
drop table if exists employee;

create table employee (
    SSN integer primary key,
    Fname varchar(20),
    MInit varchar(10),
    LName varchar(20),
    BirthDate date,
    Sex varchar(20)
);

create table employeeLifecycle (
    SSN integer,
    fromDate date,
    toDate date,
    FOREIGN key (SSN) REFERENCES employee(SSN),
    PRIMARY key (SSN, fromDate)
);

create table employeeSalary (
    SSN integer,
    salary integer,
    fromDate date,
    toDate date,
    FOREIGN key (SSN) REFERENCES employee(SSN),
    PRIMARY key (SSN, fromDate)
);

create table employeeAddress (
    SSN integer,
    street varchar(20),
    city varchar(20),
    zip integer,
    state varchar(20),
    fromDate date,
    toDate date,
    FOREIGN key (SSN) REFERENCES employee(SSN),
    PRIMARY key (SSN, fromDate)
);

create table engineer (
    SSN integer primary key
    FOREIGN key (SSN) REFERENCES employee(SSN)
);

create table engineerType (
    SSN integer,
    engineerType varchar(20),
    fromDate date,
    toDate date,
    FOREIGN key (SSN) REFERENCES engineer(SSN),
    PRIMARY key (SSN, fromDate)
);

create table engineerDiplomas (
    SSN integer, 
    diploma varchar(20),
    FOREIGN key (SSN) REFERENCES engineer(SSN),
    PRIMARY key (SSN, diploma)
);

create table administrative (
    SSN integer primary key,
    FOREIGN key (SSN) REFERENCES employee(SSN)
);

create table administrativeLifecycle (
    SSN integer,
    fromDate date,
    toDate date,
    FOREIGN key (SSN) REFERENCES administrative(SSN)
);

create table administrativeDependent (
    SSN integer,
    name varchar(20), 
    relationship varchar(20), 
    sex varchar(20),
    birthDate date,
    fromDate date,
    toDate date,
    FOREIGN key (SSN) REFERENCES administrative(SSN),
    PRIMARY key (SSN, name, relationship, fromDate)
);

create table supervision (
    supervisor integer,
    subordinate integer,
    fromDate date,
    toDate date,
    FOREIGN key (supervisor) REFERENCES employee(SSN),
    FOREIGN key (subordinate) REFERENCES employee(SSN),
    PRIMARY key (subordinate, fromDate)
);

create table department (
    DNumber integer primary key,
    DName varchar(20),
    MgrSSN integer,
    MgrStartDate date,
    fromDate date,
    toDate date,
    FOREIGN key (MgrSSN) REFERENCES employee(SSN)
);

create table dptLocations (
    DNumber integer,
    Location varchar(20),
    fromDate date,
    toDate date,
    FOREIGN key (DNumber) REFERENCES department(DNumber),
    PRIMARY key (DNumber, fromDate)
);

create table dptBudget (
    DNumber integer,
    DBudget integer,
    fromDate date,
    toDate date,
    FOREIGN key (DNumber) REFERENCES department(DNumber),
    PRIMARY key (DNumber, fromDate)
);

create table dptNEmp (
    DNumber integer,
    NEmp integer,
    fromDate date,
    toDate date,
    FOREIGN key (DNumber) REFERENCES department(DNumber),
    PRIMARY key (DNumber, fromDate)
);

create table affiliation (
    SSN integer, 
    DNumber integer,
    fromDate date,
    toDate date,
    FOREIGN key (SSN) REFERENCES employee(SSN),
    FOREIGN key (DNumber) REFERENCES department(DNumber),
    PRIMARY key (SSN, DNumber, fromDate)
);

create table project (
    PNumber integer primary key,
    Pname varchar(20),
    PLocation varchar(20),
    PBudget integer,
    fromDate date,
    toDate date
);

create table controls (
    DNumber integer,
    PNumber integer,
    fromDate date,
    toDate date,
    FOREIGN key (DNumber) REFERENCES department(DNumber),
    FOREIGN key (PNumber) REFERENCES project(PNumber),
    PRIMARY key (DNumber, PNumber, fromDate)
);

create table worksOn (
    SSN integer,
    PNumber integer,
    hours integer,
    fromDate date,
    toDate date,
    FOREIGN key (SSN) REFERENCES employee(SSN),
    FOREIGN key (PNumber) REFERENCES project(PNumber),
    PRIMARY key (SSN, PNumber, fromDate)
)
