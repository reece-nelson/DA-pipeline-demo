CREATE SCHEMA bronze;
CREATE SCHEMA silver;
CREATE SCHEMA gold;

CREATE TABLE IF NOT EXISTS bronze.raw_eia (
    Period VARCHAR(50),
    StateID CHAR(50),
    StateDescription VARCHAR(50),
    SectorID VARCHAR(50),
    SectorName VARCHAR(50),
    Customers INT,
    Price DECIMAL(12,5),     
    Revenue DECIMAL(12,5),    
    Sales DECIMAL(12,5),         
    CustomersUnits VARCHAR(50),
    PriceUnits VARCHAR(50),
    RevenueUnits VARCHAR(50),
    SalesUnits VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS bronze.raw_nhl_us_teams (
    Team_Name   VARCHAR(50),
    City        VARCHAR(50),
    State       VARCHAR(50),
    State_ID    CHAR(50)
);