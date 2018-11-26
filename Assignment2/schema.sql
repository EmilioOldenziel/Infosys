/*DROP TABLE customer; 
DROP TABLE artist; 
DROP TABLE purchase;
*/
CREATE TABLE customer2 (
	cust_no int,
	cust_name varchar(50),
	cust_addr varchar(200),
	cust_phone varchar(15),
	CONSTRAINT customers_pk PRIMARY KEY (cust_no)
 );

/*CREATE TABLE artist (
	art_id int,
	art_name varchar(50),
	art_code varchar(200),
	art_title varchar(200),
	CONSTRAINT artist_pk PRIMARY KEY (art_id)
 );

CREATE TABLE purchase (
	cust_no int,
	art_id INT,
	pur_date DATE,
	price int,
	CONSTRAINT purchases_pk PRIMARY KEY (cust_no, art_id)
 );
*/

/*CREATE OR REPLACE FUNCTION customer_to_uppercase() RETURNS TRIGGER AS $$
    BEGIN
        UPDATE customer SET cust_name = UPPER(cust_name);
	    RETURN NEW;
    END;
$$ LANGUAGE plpgsql;

*/


create function cust2upper() returns trigger as $$
begin
    new.cust_name := old.cust_name;
    return new;
end
$$ language plpgsql;

create trigger mytrigger before insert on customer2 for each row execute procedure cust2upper();