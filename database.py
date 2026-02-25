import sqlite3
import os

DB_PATH = "inventory.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Adapted DDL for SQLite
    schema = """
    CREATE TABLE IF NOT EXISTS Customers (
        CustomerId INTEGER PRIMARY KEY AUTOINCREMENT,
        CustomerCode TEXT UNIQUE NOT NULL,
        CustomerName TEXT NOT NULL,
        Email TEXT NULL,
        Phone TEXT NULL,
        BillingAddress1 TEXT NULL,
        BillingCity TEXT NULL,
        BillingCountry TEXT NULL,
        CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UpdatedAt DATETIME NULL,
        IsActive INTEGER NOT NULL DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS Vendors (
        VendorId INTEGER PRIMARY KEY AUTOINCREMENT,
        VendorCode TEXT UNIQUE NOT NULL,
        VendorName TEXT NOT NULL,
        Email TEXT NULL,
        Phone TEXT NULL,
        AddressLine1 TEXT NULL,
        City TEXT NULL,
        Country TEXT NULL,
        CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UpdatedAt DATETIME NULL,
        IsActive INTEGER NOT NULL DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS Sites (
        SiteId INTEGER PRIMARY KEY AUTOINCREMENT,
        SiteCode TEXT UNIQUE NOT NULL,
        SiteName TEXT NOT NULL,
        AddressLine1 TEXT NULL,
        City TEXT NULL,
        Country TEXT NULL,
        TimeZone TEXT NULL,
        CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UpdatedAt DATETIME NULL,
        IsActive INTEGER NOT NULL DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS Locations (
        LocationId INTEGER PRIMARY KEY AUTOINCREMENT,
        SiteId INTEGER NOT NULL,
        LocationCode TEXT NOT NULL,
        LocationName TEXT NOT NULL,
        ParentLocationId INTEGER NULL,
        CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UpdatedAt DATETIME NULL,
        IsActive INTEGER NOT NULL DEFAULT 1,
        UNIQUE (SiteId, LocationCode),
        FOREIGN KEY (SiteId) REFERENCES Sites(SiteId),
        FOREIGN KEY (ParentLocationId) REFERENCES Locations(LocationId)
    );

    CREATE TABLE IF NOT EXISTS Items (
        ItemId INTEGER PRIMARY KEY AUTOINCREMENT,
        ItemCode TEXT UNIQUE NOT NULL,
        ItemName TEXT NOT NULL,
        Category TEXT NULL,
        UnitOfMeasure TEXT NULL,
        CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UpdatedAt DATETIME NULL,
        IsActive INTEGER NOT NULL DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS Assets (
        AssetId INTEGER PRIMARY KEY AUTOINCREMENT,
        AssetTag TEXT UNIQUE NOT NULL,
        AssetName TEXT NOT NULL,
        SiteId INTEGER NOT NULL,
        LocationId INTEGER NULL,
        SerialNumber TEXT NULL,
        Category TEXT NULL,
        Status TEXT NOT NULL DEFAULT 'Active',
        Cost REAL NULL,
        PurchaseDate DATE NULL,
        VendorId INTEGER NULL,
        CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UpdatedAt DATETIME NULL,
        FOREIGN KEY (SiteId) REFERENCES Sites(SiteId),
        FOREIGN KEY (LocationId) REFERENCES Locations(LocationId),
        FOREIGN KEY (VendorId) REFERENCES Vendors(VendorId)
    );

    CREATE TABLE IF NOT EXISTS Bills (
        BillId INTEGER PRIMARY KEY AUTOINCREMENT,
        VendorId INTEGER NOT NULL,
        BillNumber TEXT NOT NULL,
        BillDate DATE NOT NULL,
        DueDate DATE NULL,
        TotalAmount REAL NOT NULL,
        Currency TEXT NOT NULL DEFAULT 'USD',
        Status TEXT NOT NULL DEFAULT 'Open',
        CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UpdatedAt DATETIME NULL,
        UNIQUE (VendorId, BillNumber),
        FOREIGN KEY (VendorId) REFERENCES Vendors(VendorId)
    );

    CREATE TABLE IF NOT EXISTS PurchaseOrders (
        POId INTEGER PRIMARY KEY AUTOINCREMENT,
        PONumber TEXT NOT NULL UNIQUE,
        VendorId INTEGER NOT NULL,
        PODate DATE NOT NULL,
        Status TEXT NOT NULL DEFAULT 'Open',
        SiteId INTEGER NULL,
        CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UpdatedAt DATETIME NULL,
        FOREIGN KEY (VendorId) REFERENCES Vendors(VendorId),
        FOREIGN KEY (SiteId) REFERENCES Sites(SiteId)
    );

    CREATE TABLE IF NOT EXISTS PurchaseOrderLines (
        POLineId INTEGER PRIMARY KEY AUTOINCREMENT,
        POId INTEGER NOT NULL,
        LineNumber INTEGER NOT NULL,
        ItemId INTEGER NULL,
        ItemCode TEXT NOT NULL,
        Description TEXT NULL,
        Quantity REAL NOT NULL,
        UnitPrice REAL NOT NULL,
        UNIQUE (POId, LineNumber),
        FOREIGN KEY (POId) REFERENCES PurchaseOrders(POId),
        FOREIGN KEY (ItemId) REFERENCES Items(ItemId)
    );

    CREATE TABLE IF NOT EXISTS SalesOrders (
        SOId INTEGER PRIMARY KEY AUTOINCREMENT,
        SONumber TEXT NOT NULL UNIQUE,
        CustomerId INTEGER NOT NULL,
        SODate DATE NOT NULL,
        Status TEXT NOT NULL DEFAULT 'Open',
        SiteId INTEGER NULL,
        CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UpdatedAt DATETIME NULL,
        FOREIGN KEY (CustomerId) REFERENCES Customers(CustomerId),
        FOREIGN KEY (SiteId) REFERENCES Sites(SiteId)
    );

    CREATE TABLE IF NOT EXISTS SalesOrderLines (
        SOLineId INTEGER PRIMARY KEY AUTOINCREMENT,
        SOId INTEGER NOT NULL,
        LineNumber INTEGER NOT NULL,
        ItemId INTEGER NULL,
        ItemCode TEXT NOT NULL,
        Description TEXT NULL,
        Quantity REAL NOT NULL,
        UnitPrice REAL NOT NULL,
        UNIQUE (SOId, LineNumber),
        FOREIGN KEY (SOId) REFERENCES SalesOrders(SOId),
        FOREIGN KEY (ItemId) REFERENCES Items(ItemId)
    );

    CREATE TABLE IF NOT EXISTS AssetTransactions (
        AssetTxnId INTEGER PRIMARY KEY AUTOINCREMENT,
        AssetId INTEGER NOT NULL,
        FromLocationId INTEGER NULL,
        ToLocationId INTEGER NULL,
        TxnType TEXT NOT NULL,
        Quantity INTEGER NOT NULL DEFAULT 1,
        TxnDate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        Note TEXT NULL,
        FOREIGN KEY (AssetId) REFERENCES Assets(AssetId),
        FOREIGN KEY (FromLocationId) REFERENCES Locations(LocationId),
        FOREIGN KEY (ToLocationId) REFERENCES Locations(LocationId)
    );
    """
    cursor.executescript(schema)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
