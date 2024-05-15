DROP TABLE IF EXISTS LegoBrick, LegoSet, StorageLocation, LegoSetContent, Customer, ShippingAdress, `Order`, OrderContent;

CREATE TABLE StorageLocation
(
	ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Quantity INT,
    House VARCHAR(1),
    Section VARCHAR(2),
    Drawer INT
);

CREATE TABLE LegoBrick
(
	ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Dim_X INT,
    Dim_Y INT,
    Dim_Z INT,
    Colour VARCHAR(6) DEFAULT "FFFFFF",
    StorageLocation INT NOT NULL,
    FOREIGN KEY (StorageLocation) REFERENCES StorageLocation(ID)
);

CREATE TABLE LegoSet
(
	ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `Name` VARCHAR(200),
    Price FLOAT
);

CREATE TABLE Customer
(
	ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    CompanyName VARCHAR(200),
    Country VARCHAR(2),
    Email VARCHAR(320)
);

CREATE TABLE ShippingAdress
(
	ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    StreetAdress VARCHAR(200),
    PostCode VARCHAR(20),
    City VARCHAR(200),
    Country VARCHAR(2)
);

CREATE TABLE `Order`
(
	ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    TotalSum FLOAT,
    OrderDate DATE,
    ShippingDate DATE,
    ArrivalDate DATE,
    Customer INT NOT NULL,
    ShippingAdress INT NOT NULL,    
	FOREIGN KEY (Customer) REFERENCES Customer(ID),
	FOREIGN KEY (ShippingAdress) REFERENCES ShippingAdress(ID)
);

CREATE TABLE LegoSetContent
(
	LegoSet INT NOT NULL,
    LegoBrick INT NOT NULL,    
    FOREIGN KEY (LegoSet) REFERENCES LegoSet(ID),
	FOREIGN KEY (LegoBrick) REFERENCES LegoBrick(ID),
    PRIMARY KEY (LegoSet, LegoBrick),
    Quantity INT
);

CREATE TABLE OrderContent
(
	`Order` INT NOT NULL,
    LegoSet INT NOT NULL,    
    FOREIGN KEY (`Order`) REFERENCES `Order`(ID),
	FOREIGN KEY (LegoSet) REFERENCES LegoSet(ID),
    PRIMARY KEY (`Order`, LegoSet),
    Quantity INT
);


