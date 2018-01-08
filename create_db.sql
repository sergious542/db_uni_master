create sequence users_id start 1;
CREATE SEQUENCE trademark_id START 1;
CREATE SEQUENCE category_id START 1;
CREATE SEQUENCE product_id START 1;
CREATE SEQUENCE city_id START 1;
CREATE SEQUENCE region_id START 1;
CREATE SEQUENCE group_product_id START 1;
CREATE SEQUENCE order_id START 1;
CREATE SEQUENCE orders_state_id START 1;


CREATE TABLE region(
  id_region INT PRIMARY KEY DEFAULT nextval('region_id'),
  title_region VARCHAR(100)
);

CREATE TABLE city(
  id_city INT PRIMARY KEY DEFAULT nextval('city_id'),
  name_city VARCHAR(100),
  is_root BOOL,
  ref_id_region INT REFERENCES region(id_region)
);

CREATE TABLE admin(
  id_admin INT PRIMARY KEY ,
  mail VARCHAR(100),
  hash_password VARCHAR(100),
  session_key VARCHAR(100)
);

create table users (
    id_users INT PRIMARY KEY DEFAULT nextval('users_id'),
    full_name VARCHAR(100),
    mail VARCHAR(100),
    password_hash VARCHAR(100),
    phone VARCHAR(20),
    ref_id_city INT REFERENCES city(id_city)
);

CREATE TABLE trademark(
  id_trademark INT PRIMARY KEY DEFAULT nextval('trademark_id'),
  path_img VARCHAR(200),
   title_trademark VARCHAR(100) UNIQUE
);

CREATE TABLE category(
  id_category INT PRIMARY KEY DEFAULT nextval('category_id'),
  name_category VARCHAR(100),
  other_information_category json
);

CREATE TABLE group_product(
  id_group_product INT PRIMARY KEY DEFAULT nextval('group_product_id'),
  name_group_product VARCHAR(100)
);


CREATE TABLE product(
  id_product INT PRIMARY KEY DEFAULT nextval('product_id'),
  name varchar(100),
  article VARCHAR(20),
  price DECIMAL,
  other json,
  is_ref bool,
  description VARCHAR(1000),
  ref_id_category INT REFERENCES category(id_category),
  ref_id_trademark INT REFERENCES trademark(id_trademark)
);

CREATE TABLE product_to_group_product(
  ref_id_product INT REFERENCES product(id_product),
  ref_id_group_product INT REFERENCES  group_product(id_group_product),
  PRIMARY KEY (ref_id_product, ref_id_group_product)
);

CREATE TABLE orders_state(
  id_orders_state INT PRIMARY KEY DEFAULT nextval('orders_state_id'),
  name_orders_state VARCHAR(100)
);

CREATE TABLE orders (
  id_order INT PRIMARY KEY DEFAULT nextval('order_id'),
  created_on DATE DEFAULT now(),
  date_appruve DATE,
  ref_id_user INT REFERENCES users(id_users),
  ref_id_product INT REFERENCES product(id_product),
  ref_id_orders_state INT REFERENCES orders_state(id_orders_state),
  title_product VARCHAR(100),
  price DECIMAL,
  quantity DECIMAL,
  other_information json
);