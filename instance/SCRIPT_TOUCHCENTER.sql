/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     19/07/2023 3:55:53 p. m.                     */
/*==============================================================*/


drop table if exists ITEM CASCADE;
drop table if exists VENTA CASCADE;
drop table if exists ARTICULO CASCADE;
drop table if exists PROVEEDOR CAsCADE;
drop table if exists CLIENTE CASCADE;

drop table if exists USUARIO CASCADE;


/*==============================================================*/
/* Table: ARTICULO                                              */
/*==============================================================*/
create table ARTICULO
(
   K_ARTICULO           int not null AUTO_INCREMENT,
   K_PROVEEDOR          int not null,
   N_ARTICULO           varchar(50) not null,
   DESC_ARTICULO        varchar(200),
   V_ARTICULO           numeric(10,2) not null,
   Q_ARTICULO           numeric(6,0),
   primary key (K_ARTICULO)
);

/*==============================================================*/
/* Table: CLIENTE                                               */
/*==============================================================*/
create table CLIENTE
(
   K_CLIENTE            int not null AUTO_INCREMENT,
   ID_CLIENTE           varchar(20) not null,
   N_CLIENTE            varchar(30) not null,
   TEL_CLIENTE          varchar(20),
   EMAIL_CLIENTE        varchar(30),
   primary key (K_CLIENTE)
);

/*==============================================================*/
/* Table: ITEM                                                  */
/*==============================================================*/
create table ITEM
(
   K_ITEM               int not null AUTO_INCREMENT,
   K_ARTICULO           int not null,
   K_VENTA              int not null,
   Q_ITEM               numeric(5,0) not null,
   VU_ITEM              numeric(10,2) not null,
   primary key (K_ITEM)
);

/*==============================================================*/
/* Table: PROVEEDOR                                             */
/*==============================================================*/
create table PROVEEDOR
(
   K_PROVEEDOR          int not null AUTO_INCREMENT,
   N_PROVEEDOR          varchar(20) not null,
   DIR_PROVEEDOR        varchar(30),
   TEL_PROVEEDOR        varchar(20),
   primary key (K_PROVEEDOR)
);

/*==============================================================*/
/* Table: USUARIO                                               */
/*==============================================================*/
create table USUARIO
(
   N_USUARIO            varchar(30) not null,
   PWD_USUARIO          varchar(40) not null,
   primary key (N_USUARIO)
);

/*==============================================================*/
/* Table: VENTA                                                 */
/*==============================================================*/
create table VENTA
(
   K_VENTA              int not null AUTO_INCREMENT,
   K_CLIENTE            int not null,
   N_USUARIO            varchar(30) not null,
   F_VENTA              timestamp not null,
   V_VENTA              numeric(12,2),
   primary key (K_VENTA)
);

alter table ARTICULO add constraint FK_PROVEEDOR_ARTICULO foreign key (K_PROVEEDOR)
      references PROVEEDOR (K_PROVEEDOR) on delete restrict on update restrict;

alter table ITEM add constraint FK_ARTICULO_ITEM foreign key (K_ARTICULO)
      references ARTICULO (K_ARTICULO) on delete restrict on update restrict;

alter table ITEM add constraint FK_VENTA_ITEM foreign key (K_VENTA)
      references VENTA (K_VENTA) on delete restrict on update restrict;

alter table VENTA add constraint FK_USUARIO_VENTA foreign key (N_USUARIO)
      references USUARIO (N_USUARIO) on delete restrict on update restrict;

alter table VENTA add constraint FK_VENTA_CLIENTE foreign key (K_CLIENTE)
      references CLIENTE (K_CLIENTE) on delete restrict on update restrict;

