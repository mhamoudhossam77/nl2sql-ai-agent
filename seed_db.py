from database import get_connection, init_db
import datetime

def seed():
    init_db()
    conn = get_connection()
    cursor = conn.cursor()

    # Seed Sites
    cursor.execute("INSERT OR IGNORE INTO Sites (SiteCode, SiteName, City, Country) VALUES (?, ?, ?, ?)",
                   ('S001', 'Main Warehouse', 'New York', 'USA'))
    cursor.execute("INSERT OR IGNORE INTO Sites (SiteCode, SiteName, City, Country) VALUES (?, ?, ?, ?)",
                   ('S002', 'West Coast Hub', 'San Francisco', 'USA'))

    # Seed Vendors
    cursor.execute("INSERT OR IGNORE INTO Vendors (VendorCode, VendorName, Email) VALUES (?, ?, ?)",
                   ('V001', 'Global Tech Solutions', 'sales@globaltech.com'))
    cursor.execute("INSERT OR IGNORE INTO Vendors (VendorCode, VendorName, Email) VALUES (?, ?, ?)",
                   ('V002', 'Office Depot', 'support@officedepot.com'))

    # Seed Customers
    cursor.execute("INSERT OR IGNORE INTO Customers (CustomerCode, CustomerName, Email) VALUES (?, ?, ?)",
                   ('C001', 'Acme Corp', 'info@acme.com'))

    # Seed Items
    cursor.execute("INSERT OR IGNORE INTO Items (ItemCode, ItemName, Category, UnitOfMeasure) VALUES (?, ?, ?, ?)",
                   ('I001', 'Laptop Pro', 'Electronics', 'Each'))
    cursor.execute("INSERT OR IGNORE INTO Items (ItemCode, ItemName, Category, UnitOfMeasure) VALUES (?, ?, ?, ?)",
                   ('I002', 'Office Chair', 'Furniture', 'Each'))

    # Seed Assets
    cursor.execute("INSERT OR IGNORE INTO Assets (AssetTag, AssetName, SiteId, Status, Cost, Category) VALUES (?, ?, ?, ?, ?, ?)",
                   ('TAG001', 'MacBook Pro 16', 1, 'Active', 2500.00, 'Electronics'))
    cursor.execute("INSERT OR IGNORE INTO Assets (AssetTag, AssetName, SiteId, Status, Cost, Category) VALUES (?, ?, ?, ?, ?, ?)",
                   ('TAG002', 'Dell XPS 15', 1, 'Active', 2000.00, 'Electronics'))
    cursor.execute("INSERT OR IGNORE INTO Assets (AssetTag, AssetName, SiteId, Status, Cost, Category) VALUES (?, ?, ?, ?, ?, ?)",
                   ('TAG003', 'Ergonomic Chair', 2, 'Active', 500.00, 'Furniture'))
    cursor.execute("INSERT OR IGNORE INTO Assets (AssetTag, AssetName, SiteId, Status, Cost, Category) VALUES (?, ?, ?, ?, ?, ?)",
                   ('TAG004', 'Broken Monitor', 2, 'Disposed', 300.00, 'Electronics'))

    # Seed Purchase Orders
    cursor.execute("INSERT OR IGNORE INTO PurchaseOrders (PONumber, VendorId, PODate, Status, SiteId) VALUES (?, ?, ?, ?, ?)",
                   ('PO-2023-001', 1, '2023-01-15', 'Closed', 1))

    # Seed Sales Orders
    cursor.execute("INSERT OR IGNORE INTO SalesOrders (SONumber, CustomerId, SODate, Status, SiteId) VALUES (?, ?, ?, ?, ?)",
                   ('SO-2023-001', 1, '2023-11-20', 'Open', 1))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    seed()
