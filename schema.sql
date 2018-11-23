CREATE TABLE customers (
	cust_no int, 
	cust_name varchar(50), 
	cust_addr, varchar(200), 
	cust_phone, varchar(15), 
	CONSTRAINT customers_pk PRIMARY KEY (cust_no)
 );

 CREATE TABLE artist (
	art_id int, 
	art_name varchar(50), 
	art_code, varchar(200), 
	art_title, varchar(200), 
	CONSTRAINT artist_pk PRIMARY KEY (art_id)
 );

  CREATE TABLE purchases (
	cust_no int, 
	art_id INT, 
	pur_date, DATE, 
	price, int, 
	CONSTRAINT purchases_pk PRIMARY KEY (cust_no, art_id)
 );