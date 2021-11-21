DROP TABLE phone_numbers;
DROP TABLE addresses;
DROP TABLE emails;
DROP TABLE persons;

CREATE TABLE persons (
  id SERIAL PRIMARY KEY,
  name VARCHAR UNIQUE
);

CREATE TABLE addresses (
  id SERIAL PRIMARY KEY,
  person_id INTEGER NOT NULL,
  street VARCHAR NOT NULL,
  apt_number VARCHAR,
  zip_code VARCHAR NOT NULL,
  city VARCHAR NOT NULL,
  state_abbr VARCHAR NOT NULL,
  UNIQUE(person_id, street),
  FOREIGN KEY(person_id) REFERENCES persons(id)
);

CREATE TABLE emails (
  id SERIAL PRIMARY KEY,
  person_id INTEGER NOT NULL,
  email VARCHAR NOT NULL,
  UNIQUE(person_id, email),
  FOREIGN KEY(person_id) REFERENCES persons(id)
);

CREATE TABLE phone_numbers (
  id SERIAL PRIMARY KEY,
  person_id INTEGER NOT NULL,
  phone_number VARCHAR NOT NULL,
  UNIQUE(person_id, phone_number),
  FOREIGN KEY(person_id) REFERENCES persons(id)
);
