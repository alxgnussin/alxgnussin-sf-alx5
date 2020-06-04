-- DROP TABLE public.p5_categories;

CREATE TABLE public.p5_categories (
	id serial NOT NULL,
	title varchar(24) NOT NULL,
	CONSTRAINT p5_categories_pk PRIMARY KEY (id)
);



-- DROP TABLE public.p5_users;

CREATE TABLE public.p5_users (
	id serial NOT NULL,
	mail varchar(30) NOT NULL,
	"password" varchar(128) NOT NULL,
	"name" varchar(20) NOT NULL,
	address text NULL,
	phone varchar(16) NOT NULL,
	CONSTRAINT p5_users_pk PRIMARY KEY (id)
);



-- DROP TABLE public.p5_meals;

CREATE TABLE public.p5_meals (
	id serial NOT NULL,
	title varchar(64) NOT NULL,
	price numeric(10,2) NOT NULL,
	description text NOT NULL,
	picture varchar(32) NOT NULL,
	category_id int4 NOT NULL,
	CONSTRAINT p5_meals_pk PRIMARY KEY (id)
);


-- public.p5_meals foreign keys

ALTER TABLE public.p5_meals ADD CONSTRAINT p5_meals_fk FOREIGN KEY (category_id) REFERENCES p5_categories(id);



-- DROP TABLE public.p5_orders;

CREATE TABLE public.p5_orders (
	id serial NOT NULL,
	order_date varchar(10) NOT NULL,
	order_sum numeric(10,2) NOT NULL,
	phone varchar(16) NOT NULL,
	address text NOT NULL,
	mail varchar(30) NOT NULL,
	user_id int4 NOT NULL,
	CONSTRAINT p5_orders_pk PRIMARY KEY (id)
);


-- public.p5_orders foreign keys

ALTER TABLE public.p5_orders ADD CONSTRAINT p5_orders_fk FOREIGN KEY (user_id) REFERENCES p5_users(id);



-- DROP TABLE public.p5_orders_meals;

CREATE TABLE public.p5_orders_meals (
	meals_id int4 NOT NULL,
	orders_id int4 NOT NULL
);


-- public.p5_orders_meals foreign keys

ALTER TABLE public.p5_orders_meals ADD CONSTRAINT p5_orders_meals_fk FOREIGN KEY (orders_id) REFERENCES p5_orders(id);
ALTER TABLE public.p5_orders_meals ADD CONSTRAINT p5_orders_meals_fk_1 FOREIGN KEY (meals_id) REFERENCES p5_meals(id);