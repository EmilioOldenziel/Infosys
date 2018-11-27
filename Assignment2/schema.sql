/* create tables customer, artist, article and purchase */

CREATE TABLE customer (
	cust_no int,
	cust_name varchar(50),
	cust_addr varchar(200),
	cust_phone varchar(15),
	CONSTRAINT customers_pk PRIMARY KEY (cust_no)
 );

CREATE TABLE artist (
	artist_id int,
	artist_name varchar(50),
	CONSTRAINT artist_pk PRIMARY KEY (artist_id)
 );

CREATE TABLE article (
	art_code varchar(200),
	art_title varchar(200),
	CONSTRAINT article_pk PRIMARY KEY (art_code)
);

CREATE TABLE purchase (
	cust_no int,
	artist_id int,
	art_code varchar(200), 
	pur_date DATE,
	price int,
	CONSTRAINT purchases_pk PRIMARY KEY (cust_no, artist_id, art_code, pur_date)
 );

/* function that changes a name of customer to its uppercase */
CREATE OR REPLACE FUNCTION cust_uppercase()
RETURNS TRIGGER AS 
$BODY$
BEGIN
	UPDATE customer SET cust_name = UPPER(cust_name);
	RETURN NEW;
END;
$BODY$
language plpgsql;

/* function that changes a name of artist to its uppercase */
CREATE OR REPLACE FUNCTION art_uppercase()
RETURNS TRIGGER AS 
$BODY$
BEGIN
	UPDATE artist SET artist_name = UPPER(artist_name);
	RETURN NEW;
END;
$BODY$
language plpgsql;

/* function that raises an error when price is not positive */
CREATE OR REPLACE FUNCTION price_pos() 
RETURNS TRIGGER AS 
$BODY$
BEGIN 
  IF NEW.price <= 0 THEN 
    RAISE EXCEPTION 'price is not positive'; 
  END IF; 
  return new; 
END;
$BODY$
language plpgsql;

/* trigger that is triggered after each insert or update on customer */
CREATE TRIGGER cust_upper
AFTER INSERT OR UPDATE 
ON customer 
FOR EACH ROW 
WHEN (pg_trigger_depth() = 0)
EXECUTE PROCEDURE cust_uppercase();

/* trigger that is triggered after each insert or update on artist */
CREATE TRIGGER art_upper
AFTER INSERT OR UPDATE 
ON artist 
FOR EACH ROW 
WHEN (pg_trigger_depth() = 0)
EXECUTE PROCEDURE art_uppercase();

/* trigger that is raises error when price is not greater than 0 */
CREATE TRIGGER price_check
AFTER INSERT OR UPDATE 
ON purchase 
FOR EACH ROW 
WHEN (pg_trigger_depth() = 0)
EXECUTE PROCEDURE price_pos();