BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "auth_group" (
	"id"	integer NOT NULL,
	"name"	varchar(150) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "auth_user" (
	"id"	integer NOT NULL,
	"password"	varchar(128) NOT NULL,
	"last_login"	datetime,
	"is_superuser"	bool NOT NULL,
	"username"	varchar(150) NOT NULL UNIQUE,
	"last_name"	varchar(150) NOT NULL,
	"email"	varchar(254) NOT NULL,
	"is_staff"	bool NOT NULL,
	"is_active"	bool NOT NULL,
	"date_joined"	datetime NOT NULL,
	"first_name"	varchar(150) NOT NULL,
	"dni"	varchar(10) NULL,
	"phone"	varchar(15) NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_user_groups" (
	"id"	integer NOT NULL,
	"user_id"	integer NOT NULL,
	"group_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "authtoken_token" (
	"key"	varchar(40) NOT NULL,
	"created"	datetime NOT NULL,
	"user_id"	integer NOT NULL UNIQUE,
	PRIMARY KEY("key"),
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "parking_parkingassignment" (
	"id"	integer NOT NULL,
	"status"	varchar(20) NOT NULL,
	"entry_time"	datetime NOT NULL,
	"exit_time"	datetime,
	"planned_exit_time"	datetime,
	"total_cost"	decimal,
	"notes"	text NOT NULL,
	"created_at"	datetime NOT NULL,
	"updated_at"	datetime NOT NULL,
	"assigned_by_id"	integer,
	"completed_by_id"	integer,
	"parking_space_id"	bigint NOT NULL,
	"vehicle_id"	bigint NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("assigned_by_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("completed_by_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("parking_space_id") REFERENCES "parking_parkingspace"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("vehicle_id") REFERENCES "parking_vehicle"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "parking_parkingconfiguration" (
	"id"	integer NOT NULL,
	"total_floors"	integer unsigned NOT NULL CHECK("total_floors" >= 0),
	"spaces_per_floor"	integer unsigned NOT NULL CHECK("spaces_per_floor" >= 0),
	"is_active"	bool NOT NULL,
	"created_at"	datetime NOT NULL,
	"updated_at"	datetime NOT NULL,
	"created_by_id"	integer,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("created_by_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "parking_parkingfloor" (
	"id"	integer NOT NULL,
	"floor_number"	integer unsigned NOT NULL CHECK("floor_number" >= 0),
	"floor_name"	varchar(50) NOT NULL,
	"is_active"	bool NOT NULL,
	"created_at"	datetime NOT NULL,
	"configuration_id"	bigint NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("configuration_id") REFERENCES "parking_parkingconfiguration"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "parking_parkingreservation" (
	"id"	integer NOT NULL,
	"status"	varchar(20) NOT NULL,
	"reservation_date"	datetime NOT NULL,
	"duration_minutes"	integer unsigned NOT NULL CHECK("duration_minutes" >= 0),
	"notes"	text NOT NULL,
	"created_at"	datetime NOT NULL,
	"updated_at"	datetime NOT NULL,
	"user_id"	integer,
	"parking_space_id"	bigint,
	"created_by_id"	integer,
	"customer_email"	varchar(254) NOT NULL,
	"customer_name"	varchar(100) NOT NULL,
	"customer_phone"	varchar(20) NOT NULL,
	"is_quick_reservation"	bool NOT NULL,
	"vehicle_plate"	varchar(20) NOT NULL,
	"vehicle_type_temp"	varchar(20) NOT NULL,
	"vehicle_id"	bigint,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("created_by_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("parking_space_id") REFERENCES "parking_parkingspace"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("vehicle_id") REFERENCES "parking_vehicle"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "parking_parkingspace" (
	"id"	integer NOT NULL,
	"space_number"	integer unsigned NOT NULL CHECK("space_number" >= 0),
	"status"	varchar(20) NOT NULL,
	"is_active"	bool NOT NULL,
	"created_at"	datetime NOT NULL,
	"updated_at"	datetime NOT NULL,
	"floor_id"	bigint NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("floor_id") REFERENCES "parking_parkingfloor"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "parking_vehicle" (
	"id"	integer NOT NULL,
	"vehicle_type"	varchar(20) NOT NULL,
	"brand"	varchar(50) NULL,
	"model"	varchar(50) NULL,
	"year"	integer unsigned  NULL,
	"color"	varchar(30) NOT NULL,
	"license_plate"	varchar(20) NOT NULL UNIQUE,
	"is_active"	bool NOT NULL,
	"created_at"	datetime NOT NULL,
	"updated_at"	datetime NOT NULL,
	"owner_id"	integer NOT NULL,
	"registered_by_id"	integer,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("owner_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("registered_by_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "parking_vehicletariff" (
	"id"	integer NOT NULL,
	"vehicle_type"	varchar(20) NOT NULL UNIQUE,
	"rate_per_hour"	decimal NOT NULL,
	"is_active"	bool NOT NULL,
	"created_at"	datetime NOT NULL,
	"updated_at"	datetime NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "auth_group" VALUES (1,'administrador');
INSERT INTO "auth_group" VALUES (2,'trabajador');
INSERT INTO "auth_group" VALUES (3,'usuario');

INSERT INTO "parking_vehicletariff" (id,vehicle_type,rate_per_hour,is_active,created_at,updated_at) VALUES (1,'CAR',3.00,1,'2025-10-18 00:00:00','2025-10-18 00:00:00');
INSERT INTO "parking_vehicletariff" (id,vehicle_type,rate_per_hour,is_active,created_at,updated_at) VALUES (2,'TRUCK',5.00,1,'2025-10-18 00:00:00','2025-10-18 00:00:00');
INSERT INTO "parking_vehicletariff" (id,vehicle_type,rate_per_hour,is_active,created_at,updated_at) VALUES (3,'MOTORCYCLE',2.00,1,'2025-10-18 00:00:00','2025-10-18 00:00:00');
INSERT INTO "parking_parkingconfiguration" (id,total_floors,spaces_per_floor,is_active,created_at,updated_at,created_by_id) VALUES (1,3,50,1,'2025-10-18 00:00:00','2025-10-18 00:00:00',1);

