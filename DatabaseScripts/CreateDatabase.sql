  create table doctor (
	DoctorID int,
    DoctorName varchar(50),
	email varchar(50),
    password_ varchar(15),
    primary key(DoctorID, email)
   );
    
# Segmented control = 1
# TextField = 2
create table questions (
	QuestionID int auto_increment primary key,
	QuestionType tinyint, 
    PossibleAnswers varchar(250),
    Question varchar(250));
    
create table json_files (
	name varchar(50) primary key,
    data blob);
    
create table testframe (
	TestID int auto_increment,
    PatientID varchar(50),
    DateTaken date,
    DoctorID int,
    TestName varchar(50),
    TestLength time,
    constraint fk_doctorid foreign key (DoctorID) references Doctor(DoctorID),
    constraint fk_testname foreign key (TestName) references json_files(name),
    primary key (TestID, PatientID, DoctorID));
    
create table circles (
	TestID int,
    CircleID int,
    symbol varchar(1),
    begin_circle double,
    end_circle double,
    total_time double,
    constraint fk_testid foreign key (TestID) references testframe(TestID),
    primary key (CircleID, TestID));
    
create table pressure (
	TestID int,
    CircleID int,
    PressureID int,
    Xcoord double,
    Ycoord double,
    Pressure double,
    PenAltitude double,
    Azimuth double,
    constraint fk_circleid foreign key (CircleID) references circles(CircleID),
    constraint fk_testid3 foreign key (TestID) references testframe(TestID),
    primary key (TestID, CircleID, PressureID));
    
create table answers (
	TestID int,
    QuestionID int,
    Answer varchar(250),
    constraint fk_testid2 foreign key (TestID) references testframe(TestID),
    constraint fk_questionid foreign key (QuestionID) references questions(QuestionID),
    primary key (TestID, QuestionID));
