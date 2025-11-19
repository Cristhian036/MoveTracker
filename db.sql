BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "auth_group" (
	"id"	integer NOT NULL,
	"name"	varchar(150) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_permission" (
	"id"	integer NOT NULL,
	"content_type_id"	integer NOT NULL,
	"codename"	varchar(100) NOT NULL,
	"name"	varchar(255) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED
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

INSERT INTO "auth_permission" VALUES (1,1,'add_logentry','Can add log entry');
INSERT INTO "auth_permission" VALUES (2,1,'change_logentry','Can change log entry');
INSERT INTO "auth_permission" VALUES (3,1,'delete_logentry','Can delete log entry');
INSERT INTO "auth_permission" VALUES (4,1,'view_logentry','Can view log entry');
INSERT INTO "auth_permission" VALUES (5,2,'add_permission','Can add permission');
INSERT INTO "auth_permission" VALUES (6,2,'change_permission','Can change permission');
INSERT INTO "auth_permission" VALUES (7,2,'delete_permission','Can delete permission');
INSERT INTO "auth_permission" VALUES (8,2,'view_permission','Can view permission');
INSERT INTO "auth_permission" VALUES (9,3,'add_group','Can add group');
INSERT INTO "auth_permission" VALUES (10,3,'change_group','Can change group');
INSERT INTO "auth_permission" VALUES (11,3,'delete_group','Can delete group');
INSERT INTO "auth_permission" VALUES (12,3,'view_group','Can view group');
INSERT INTO "auth_permission" VALUES (13,4,'add_user','Can add user');
INSERT INTO "auth_permission" VALUES (14,4,'change_user','Can change user');
INSERT INTO "auth_permission" VALUES (15,4,'delete_user','Can delete user');
INSERT INTO "auth_permission" VALUES (16,4,'view_user','Can view user');
INSERT INTO "auth_permission" VALUES (17,5,'add_contenttype','Can add content type');
INSERT INTO "auth_permission" VALUES (18,5,'change_contenttype','Can change content type');
INSERT INTO "auth_permission" VALUES (19,5,'delete_contenttype','Can delete content type');
INSERT INTO "auth_permission" VALUES (20,5,'view_contenttype','Can view content type');
INSERT INTO "auth_permission" VALUES (21,6,'add_session','Can add session');
INSERT INTO "auth_permission" VALUES (22,6,'change_session','Can change session');
INSERT INTO "auth_permission" VALUES (23,6,'delete_session','Can delete session');
INSERT INTO "auth_permission" VALUES (24,6,'view_session','Can view session');
INSERT INTO "auth_permission" VALUES (25,7,'add_token','Can add Token');
INSERT INTO "auth_permission" VALUES (26,7,'change_token','Can change Token');
INSERT INTO "auth_permission" VALUES (27,7,'delete_token','Can delete Token');
INSERT INTO "auth_permission" VALUES (28,7,'view_token','Can view Token');
INSERT INTO "auth_permission" VALUES (29,8,'add_tokenproxy','Can add Token');
INSERT INTO "auth_permission" VALUES (30,8,'change_tokenproxy','Can change Token');
INSERT INTO "auth_permission" VALUES (31,8,'delete_tokenproxy','Can delete Token');
INSERT INTO "auth_permission" VALUES (32,8,'view_tokenproxy','Can view Token');
INSERT INTO "auth_permission" VALUES (33,9,'add_profile','Can add Perfil');
INSERT INTO "auth_permission" VALUES (34,9,'change_profile','Can change Perfil');
INSERT INTO "auth_permission" VALUES (35,9,'delete_profile','Can delete Perfil');
INSERT INTO "auth_permission" VALUES (36,9,'view_profile','Can view Perfil');
INSERT INTO "auth_permission" VALUES (37,10,'add_vehicletariff','Can add Tarifa de Vehículo');
INSERT INTO "auth_permission" VALUES (38,10,'change_vehicletariff','Can change Tarifa de Vehículo');
INSERT INTO "auth_permission" VALUES (39,10,'delete_vehicletariff','Can delete Tarifa de Vehículo');
INSERT INTO "auth_permission" VALUES (40,10,'view_vehicletariff','Can view Tarifa de Vehículo');
INSERT INTO "auth_permission" VALUES (41,11,'add_parkingconfiguration','Can add Configuración de Estacionamiento');
INSERT INTO "auth_permission" VALUES (42,11,'change_parkingconfiguration','Can change Configuración de Estacionamiento');
INSERT INTO "auth_permission" VALUES (43,11,'delete_parkingconfiguration','Can delete Configuración de Estacionamiento');
INSERT INTO "auth_permission" VALUES (44,11,'view_parkingconfiguration','Can view Configuración de Estacionamiento');
INSERT INTO "auth_permission" VALUES (45,12,'add_parkingfloor','Can add Piso de Estacionamiento');
INSERT INTO "auth_permission" VALUES (46,12,'change_parkingfloor','Can change Piso de Estacionamiento');
INSERT INTO "auth_permission" VALUES (47,12,'delete_parkingfloor','Can delete Piso de Estacionamiento');
INSERT INTO "auth_permission" VALUES (48,12,'view_parkingfloor','Can view Piso de Estacionamiento');
INSERT INTO "auth_permission" VALUES (49,13,'add_parkingspace','Can add Espacio de Estacionamiento');
INSERT INTO "auth_permission" VALUES (50,13,'change_parkingspace','Can change Espacio de Estacionamiento');
INSERT INTO "auth_permission" VALUES (51,13,'delete_parkingspace','Can delete Espacio de Estacionamiento');
INSERT INTO "auth_permission" VALUES (52,13,'view_parkingspace','Can view Espacio de Estacionamiento');
INSERT INTO "auth_permission" VALUES (53,14,'add_vehicle','Can add Vehículo');
INSERT INTO "auth_permission" VALUES (54,14,'change_vehicle','Can change Vehículo');
INSERT INTO "auth_permission" VALUES (55,14,'delete_vehicle','Can delete Vehículo');
INSERT INTO "auth_permission" VALUES (56,14,'view_vehicle','Can view Vehículo');
INSERT INTO "auth_permission" VALUES (57,15,'add_parkingreservation','Can add Reserva de Estacionamiento');
INSERT INTO "auth_permission" VALUES (58,15,'change_parkingreservation','Can change Reserva de Estacionamiento');
INSERT INTO "auth_permission" VALUES (59,15,'delete_parkingreservation','Can delete Reserva de Estacionamiento');
INSERT INTO "auth_permission" VALUES (60,15,'view_parkingreservation','Can view Reserva de Estacionamiento');
INSERT INTO "auth_permission" VALUES (61,16,'add_parkingassignment','Can add Asignación de Estacionamiento');
INSERT INTO "auth_permission" VALUES (62,16,'change_parkingassignment','Can change Asignación de Estacionamiento');
INSERT INTO "auth_permission" VALUES (63,16,'delete_parkingassignment','Can delete Asignación de Estacionamiento');
INSERT INTO "auth_permission" VALUES (64,16,'view_parkingassignment','Can view Asignación de Estacionamiento');
INSERT INTO "parking_vehicletariff" (id,vehicle_type,rate_per_hour,is_active,created_at,updated_at) VALUES (1,'car',3.00,1,'2025-10-18 00:00:00','2025-10-18 00:00:00');
INSERT INTO "parking_vehicletariff" (id,vehicle_type,rate_per_hour,is_active,created_at,updated_at) VALUES (2,'camioneta',5.00,1,'2025-10-18 00:00:00','2025-10-18 00:00:00');
INSERT INTO "parking_vehicletariff" (id,vehicle_type,rate_per_hour,is_active,created_at,updated_at) VALUES (3,'moto',2.00,1,'2025-10-18 00:00:00','2025-10-18 00:00:00');
INSERT INTO "parking_parkingconfiguration" (id,total_floors,spaces_per_floor,is_active,created_at,updated_at,created_by_id) VALUES (1,3,50,1,'2025-10-18 00:00:00','2025-10-18 00:00:00',1);

