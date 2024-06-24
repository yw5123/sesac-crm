CREATE TABLE IF NOT EXISTS "users"(
    "Id" TEXT PRIMARY KEY, 
    "Name" TEXT NOT NULL, 
    "Gender" TEXT, 
    "Age" INTEGER,
    "Birthdate" DATE, 
    "Address" TEXT
);
CREATE TABLE IF NOT EXISTS "stores"(
    "Id" TEXT PRIMARY KEY, 
    "Name" TEXT NOT NULL, 
    "Type" TEXT, 
    "Address" TEXT
);
CREATE TABLE IF NOT EXISTS "orders"(
    "Id" TEXT PRIMARY KEY, 
    "OrderAt" DATETIME NOT NULL CHECK(OrderAt <= CURRENT_TIMESTAMP), 
    "StoreId" TEXT NOT NULL, 
    "UserId" TEXT NOT NULL,
    FOREIGN KEY ("StoreId") REFERENCES "stores"("Id"),
    FOREIGN KEY ("UserId") REFERENCES "useres"("Id")
);
CREATE TABLE IF NOT EXISTS "items"(
    "Id" TEXT PRIMARY KEY, 
    "Name" TEXT NOT NULL, 
    "Type" TEXT, 
    "UnitPrice" INTEGER CHECK (UnitPrice >= 0)
);
CREATE TABLE IF NOT EXISTS "orderitems"(
    "Id" TEXT PRIMARY KEY, 
    "OrderId" TEXT NOT NULL, 
    "ItemId" TEXT,
    FOREIGN KEY ("orderId") REFERENCES "orders"("Id") ON DELETE CASCADE,
    FOREIGN KEY ("ItemId") REFERENCES "items"("Id") 
);