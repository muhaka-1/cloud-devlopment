# Cloud Data Platforms, Data Integration & Database Architecture

## Overview

This project explores modern cloud-based data platform concepts through the design and implementation of a hybrid SQL and NoSQL solution for a fictional e-commerce company, **NovaStore**.

The project covers relational databases, document databases, containerization, data modeling, CRUD operations, performance optimization, scalability, and cloud architecture principles.

## Learning Objectives

* Design relational and document-based data models
* Work with PostgreSQL and MongoDB
* Implement CRUD operations
* Understand database consistency and transactions
* Analyze bottlenecks and optimization techniques
* Connect databases through Python applications
* Explore cloud-native deployment using Docker
* Evaluate scalability and caching strategies

---

# Technologies Used

| Technology     | Purpose                  |
| -------------- | ------------------------ |
| PostgreSQL     | Relational Database      |
| MongoDB        | NoSQL Document Database  |
| Redis          | Caching Layer            |
| Docker Compose | Container Orchestration  |
| Python         | Database Integration     |
| psycopg2       | PostgreSQL Python Driver |
| PyMongo        | MongoDB Python Driver    |
| Git & GitHub   | Version Control          |

---

# Project Structure

```text
.
├── docker-compose.yml
├── postgres_test.py
├── mongo_test.py
├── README.md
└── docs/
```
# System Architecture

```text
Users
   │
Frontend
   │
Backend API
   │
 ┌───────────────┬───────────────┬───────────────┐
 │ PostgreSQL    │ MongoDB       │ Redis         │
 │ Orders        │ Products      │ Cache         │
 │ Payments      │ Documents     │ Sessions      │
 │ Inventory     │ Analytics     │ Performance   │
 └───────────────┴───────────────┴───────────────┘
```
---

# Del 1 – Environment Setup

Configured a local development environment using Docker Compose.

### Services

* PostgreSQL
* MongoDB
* Redis

### Start Containers

```bash
docker compose up -d
```

### Verify Containers

```bash
docker ps
```

You should see something similar to:

    CONTAINER ID   IMAGE         NAMES
    xxxxxx         postgres:16   sql-demo
    xxxxxx         mongo:7       nosql-demo

# Del 2a Start Databes
# Test PostgreSQL

 Connect to PostgreSQL:

    docker exec -it sql-demo psql -U student -d shop

If successful, you will enter the PostgreSQL shell:

    shop=#

 Run:

    SELECT NOW();

You should see the current date and time returned by the database.

     2026-06-22 16:43:45.234018+00
    (1 row)

Exit PostgreSQL with:

    \q
# Test MongoDB

Connect to MongoDB:

    docker exec -it nosql-demo mongosh

If successful, you will enter the MongoDB shell:

    test>

List available databases:

    show dbs   
### You should see 
    admin   40.00 KiB
    config  60.00 KiB
    local   40.00 KiB 

Exit MongoDB:

    exit
---

# Del 2b – Data Modeling

Designed data structures for an e-commerce platform.

## Relational Model (PostgreSQL)

### Customers

```sql
customers
```

### Products

```sql
products
```

### Orders

```sql
orders
```

### Order Items

```sql
order_items
```

### Relationships

```text
Customer
   │
   ├── Orders
            │
            └── Order Items
                        │
                        └── Products
```

---

## NoSQL Model (MongoDB)

Order documents were stored using embedded data.

Example:

```json
{
  "order_id": "order_1",
  "customer": {
    "name": "Sara",
    "email": "sara@example.com"
  },
  "items": [
    {
      "name": "Laptop",
      "price": 12990,
      "quantity": 1
    }
  ],
  "status": "created"
}
```

---

# Del 3 - SQL (PostgreSQL)

## Overview

This section demonstrates how to create and manage a relational database for the NovaStore e-commerce platform using PostgreSQL.

Topics covered:

* Database schema design
* CRUD operations
* JOIN queries
* Indexing
* Data relationships

---

## 1. Connect to PostgreSQL

Start the PostgreSQL container and connect to the database:

```bash
docker exec -it sql-demo psql -U student -d shop
```

2. Verify the connection:

```sql
SELECT NOW();
```

---

# 3. Create Database Schema

### Customers Table

```sql
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);
```

### Products Table

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL NOT NULL,
    category TEXT,
    stock INT DEFAULT 0
);
```

### Orders Table

```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(id),
    status TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Order Items Table

```sql
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(id),
    product_id INT REFERENCES products(id),
    quantity INT NOT NULL
);
```

---

## 4. Verify Tables

List all tables:

```sql
\dt
```

Expected output:

```text
customers
products
orders
order_items
```

---

# 5.CRUD Operations

## Create

### 5.1 Create Customer

```sql
INSERT INTO customers(name, email)
VALUES ('Sara', 'sara@example.com');
```

### 5.2 Create Product

```sql
INSERT INTO products(name, price, category, stock)
VALUES ('Laptop', 12990, 'Electronics', 5);
```

### 5.3 Create Order

```sql
INSERT INTO orders(customer_id, status)
VALUES (1, 'created');
```

### 5.3 Add Product to Order

```sql
INSERT INTO order_items(order_id, product_id, quantity)
VALUES (1, 1, 1);
```

---

## 6. Read

### View Customers

```sql
SELECT * FROM customers;
```

### 7. View Products

```sql
SELECT * FROM products;
```

### 8. View Orders

```sql
SELECT * FROM orders;
```

---

## 9. Update

### Update Order Status

```sql
UPDATE orders
SET status = 'paid'
WHERE id = 1;
```

### Update Product Stock

```sql
UPDATE products
SET stock = 10
WHERE id = 1;
```

---

## 10. Delete

### Delete Product

```sql
DELETE FROM products
WHERE id = 1;
```

---

# 11. JOIN Example

Retrieve customer names together with their orders:

```sql
SELECT customers.name,
       orders.id,
       orders.status
FROM orders
JOIN customers
ON orders.customer_id = customers.id;
```

Example result:

| Name | Order ID | Status |
| ---- | -------- | ------ |
| Sara | 1        | paid   |

---

# 12. Indexing

Create an index on customer email to improve search performance:

```sql
CREATE INDEX idx_customers_email
ON customers(email);
```

---

# Database Relationships

```text
customers
    |
    | 1:N
    |
orders
    |
    | 1:N
    |
order_items
    |
    | N:1
    |
products
```

---

# Useful PostgreSQL Commands

Show tables:

```sql
\dt
```

Describe a table:

```sql
\d customers
```

Exit PostgreSQL:

```sql
\q
```

---

# Summary

The SQL implementation provides:

* Strong consistency
* Structured relational data
* Foreign key constraints
* Efficient JOIN operations
* Index support for fast lookups

This makes PostgreSQL well suited for customers, products, inventory, and transactional order data in NovaStore.


---

# Del 4 – NoSQL (MongoDB)

## Overview

In this exercise, we use MongoDB to perform CRUD operations and model order data using embedded documents.

MongoDB stores data in **collections** and **documents** rather than tables and rows.

---

# 1. Connect to MongoDB

Start the MongoDB shell:

```bash
docker exec -it nosql-demo mongosh
```

Expected prompt:

```text
test>
```

---

# 2. Create and Use a Database

Switch to the `shop` database:

```javascript
use shop
```

MongoDB will automatically create the database when data is inserted.

---

# 3. Create a Customer Document

Insert a customer into the `customers` collection:

```javascript
db.customers.insertOne({
  name: "Sara",
  email: "sara@example.com"
})
```

Expected result:

```json
{
  acknowledged: true,
  insertedId: ObjectId("...")
}
```

---

# 4. Create a Product Document

Insert a product into the `products` collection:

```javascript
db.products.insertOne({
  name: "Laptop",
  price: 12990,
  category: "Electronics",
  stock: 5
})
```

---

# 5. Create an Order Document

Insert an order containing customer and product information:

```javascript
db.orders.insertOne({
  order_id: "order_1",

  customer: {
    id: "customer_1",
    name: "Sara",
    email: "sara@example.com"
  },

  items: [
    {
      product_id: "product_1",
      name: "Laptop",
      price: 12990,
      quantity: 1
    }
  ],

  status: "created"
})
```

Example document structure:

```json
{
  "order_id": "order_1",
  "customer": {
    "id": "customer_1",
    "name": "Sara",
    "email": "sara@example.com"
  },
  "items": [
    {
      "product_id": "product_1",
      "name": "Laptop",
      "price": 12990,
      "quantity": 1
    }
  ],
  "status": "created"
}
```

---

# 6. Read Data (CRUD – Read)

## Show All Customers

```javascript
db.customers.find()
```

## Show All Customers (Formatted)

```javascript
db.customers.find().pretty()
```

## Show All Orders

```javascript
db.orders.find().pretty()
```

---

# 7. Update Data (CRUD – Update)

Update the order status:

```javascript
db.orders.updateOne(
  { order_id: "order_1" },
  {
    $set: {
      status: "paid"
    }
  }
)
```

Verify the update:

```javascript
db.orders.find().pretty()
```

---

# 8. Delete Data (CRUD – Delete)

Delete a customer document:

```javascript
db.customers.deleteOne({
  email: "sara@example.com"
})
```

---

# 9. Soft Delete

Instead of permanently deleting a document, mark it as deleted:

```javascript
db.products.updateOne(
  { name: "Laptop" },
  {
    $set: {
      deleted: true
    }
  }
)
```

This technique is called **Soft Delete**.

Benefits:

* Preserves historical data
* Allows recovery of deleted records
* Prevents broken references

---

# 10. Prevent Duplicate Emails

Create a unique index on the email field:

```javascript
db.customers.createIndex(
  { email: 1 },
  { unique: true }
)
```

---

# 11. Test Duplicate Protection

Insert the first customer:

```javascript
db.customers.insertOne({
  name: "Sara",
  email: "sara@example.com"
})
```

Attempt to insert a duplicate:

```javascript
db.customers.insertOne({
  name: "Sara Backup",
  email: "sara@example.com"
})
```

Expected result:

```text
E11000 duplicate key error
```

MongoDB rejects the duplicate email.

---

# 12. Show Existing Collections

```javascript
show collections
```

Example output:

```text
customers
orders
products
```

---

# 13. Exit MongoDB

```javascript
exit
```

---

# SQL vs MongoDB

| PostgreSQL (SQL) | MongoDB (NoSQL)        |
| ---------------- | ---------------------- |
| Tables           | Collections            |
| Rows             | Documents              |
| Fixed Schema     | Flexible Schema        |
| JOIN Operations  | Embedded Documents     |
| Relational Data  | Document-Oriented Data |

Example MongoDB document:

```json
{
  "customer": {
    "name": "Sara"
  },
  "items": [
    {
      "name": "Laptop"
    }
  ]
}
```

---

# Completed Learning Objectives

* Connect to MongoDB
* Create Collections and Documents
* Perform CRUD Operations
* Model Data Using Embedded Documents
* Implement Soft Delete
* Prevent Duplicate Data with Unique Indexes
* Understand SQL vs NoSQL Tradeoffs
* Prepare for Del 5 (Buggar och Flaskhalsar)


---

# Del 5 – Bug Analysis & Bottlenecks

## Problem A- Slow Queries in PostgreSQL 

Problem:

```sql
SELECT *
FROM customers
WHERE LOWER(email) = LOWER('sara@example.com');
```

Why is it slow?

Because:

      LOWER(email)

forces PostgreSQL to apply a function on every row.

That means the normal index on email cannot be used efficiently.

PostgreSQL may perform a:

      * full table scan
      * checking every row one by one

This becomes very slow with millions of customers.

### Solution

Create indexes:

```sql
CREATE INDEX idx_customers_email
ON customers(email);
```
Then query:

      SELECT *
      FROM customers
      WHERE email = 'sara@example.com';

Now the index works efficiently.

What we resolve
Functions in WHERE clauses can break index optimization
Indexes improve lookup speed
Large datasets require optimized queries
---

## Problem B- Duplicate Users in MongoDB

Code:

      db.customers.insertMany([
        { name: "Sara", email: "sara@example.com" },
        { name: "Sara Backup", email: "sara@example.com" }
      ])
Why is this a problem?

MongoDB has flexible schema and no automatic uniqueness.

So duplicate emails are allowed unless explicitly prevented.

This can cause:

      * duplicate accounts
      * login issues
      * inconsistent customer data

Solution — Unique index

Create unique constraint:

      db.customers.createIndex(
        { email: 1 },
        { unique: true }
      )

Now duplicate emails are rejected automatically.

What to say in discussion
* MongoDB is flexible but requires manual constraints
* SQL databases usually enforce stricter integrity
* NoSQL gives flexibility but more responsibility to developers

---

## Problem C — Negative Stock

Code:

UPDATE products
SET stock = stock - 1
WHERE id = 1;
What is the problem?

Two users buy the last product at the same time.

Example:

Current stock = 1

User A buys:

      stock becomes 0

At the same moment User B also buys:

      stock becomes -1

Now inventory is corrupted.

This is called a:

* race condition
* concurrency problem

### Solution  — Conditional update
      UPDATE products
      SET stock = stock - 1
      WHERE id = 1
      AND stock > 0;

Now stock only updates if inventory exists.

What to say in discussion
* Concurrent users create consistency problems
* Inventory systems require strong consistency
* Transactions are important in e-commerce

---

# Del 6 – Database Integration with Python

Part A — PostgreSQL in Python

1. Install PostgreSQL driver

Install:

    py -m pip install psycopg2-binary 
### or 
      pip install psycopg2-binary
      
2. Create Python file

Example:

    touch postgres_test.py
### or 
      nano postgres_test.py

Verify installation

Run:

      pip list

You should see something like:

      psycopg2-binary
## 4. PostgreSQL Connection

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="student",
    password="student",
    database="shop"
)

cursor = conn.cursor()

cursor.execute("SELECT * FROM customers")

rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.close()
conn.close()
```

### 5. Query Example

```python

cursor.execute("SELECT * FROM customers")

rows = cursor.fetchall()

```
### 6. Run the program in terminal:

    python postgres_test.py

Expected output:

    (1, 'Sara', 'sara@example.com')

---
# Part B — MongoDB in Python

### 1. Install MongoDB driver
### Run:
    pip install pymongo
### or 
      py -m pip install pymongo

Expected:

      Successfully installed pymongo

### 2. Create Python file
    touch mongo_test.py
 ### or 
    nano mongo_test.py
    
###3. Add MongoDB code / MongoDB Connection

Paste this:
```python
from pymongo import MongoClient

client = MongoClient(
    "mongodb://localhost:27017"
)

db = client["shop"]

print("Connected!")

collections = db.list_collection_names()

print(collections)
```

### 4. Run the MongoDB program
    python mongo_test.py

Expected output:

    Connected!
    ['customers', 'products', 'orders']

### Query Example

```python
orders = db.orders.find()

for order in orders:
    print(order)
```
Run:

      python mongo_test.py

Expected output:

      {
        '_id': ObjectId(...),
        'order_id': 'order_1',
        ...
      }
---

# Important concepts for presentation
PostgreSQL connection

Uses:

      psycopg2

Relational SQL database access.

MongoDB connection

Uses:

      pymongo

Document-based NoSQL access.

Difference in querying
PostgreSQL

SQL query string:

      cursor.execute("SELECT * FROM customers")
MongoDB

Collection method:

      db.orders.find()
What this exercise demonstrates

You can now:

* connect cloud applications to databases
* fetch SQL data
* fetch NoSQL documents
* use Dockerized databases locally
* integrate databases with Python apps


# Del 7 – Discussion & Architecture

## When to Use SQL

Best for:

* Orders
* Payments
* Inventory
* Financial Transactions

Benefits:

* ACID Transactions
* Strong Consistency
* Relationships
* Constraints

---

## When to Use NoSQL

Best for:

* Product Catalogs
* Analytics
* Logs
* Flexible Data Structures

Benefits:

* Flexible Schema
* Horizontal Scaling
* Fast Document Retrieval

---

## Consistency Models

### Strong Consistency

Required for:

* Payments
* Inventory
* Order Processing

### Eventual Consistency

Acceptable for:

* Recommendations
* Analytics
* Search Results

---
Simple architecture explanation

We can say:

      PostgreSQL handled transactional data
      (orders, payments, inventory)
      
      MongoDB handled flexible product and document data.
      
      Redis could be added for caching and performance.

# Del 8 – Stretch Goals

## Objective

This section explores advanced cloud development concepts:

- Pagination
- Redis Caching
- Database Transactions
- Docker Volumes
- Architecture Diagrams

---

# 1. Pagination

Pagination loads data in smaller chunks instead of returning everything at once.

## Why?

Without pagination:

```sql
SELECT * FROM products;
```

Create a table containing millions of rows can become very slow.

Practice in PostgreSQL

Insert many products:

      INSERT INTO products(name, price, stock)
      VALUES
      ('Laptop 1', 1000, 5),
      ('Laptop 2', 1000, 5),
      ('Laptop 3', 1000, 5),
      ('Laptop 4', 1000, 5),
      ('Laptop 5', 1000, 5),
      ('Laptop 6', 1000, 5),
      ('Laptop 7', 1000, 5),
      ('Laptop 8', 1000, 5),
      ('Laptop 9', 1000, 5),
      ('Laptop 10', 1000, 5),
      ('Laptop 11', 1000, 5);

## Pagination query

First 5 products in First page:

```sql
SELECT *
FROM products
LIMIT 5 OFFSET 0;
```

Next 5 products in Second page:

```sql
SELECT *
FROM products
LIMIT 5 OFFSET 5;
```

### Benefits

- Faster queries
- Lower memory usage
- Better user experience

---

# 2. Redis Caching

Redis is an in-memory database used for caching frequently accessed data.

## Add Redis to Docker Compose

```yaml
redis:
  image: redis:7
  container_name: redis-demo
  ports:
    - "6379:6379"
```

## Start Containers

```bash
docker compose up -d
```

## Verify

```bash
docker ps
```

Expected:

```text
redis-demo
```

## Test Redis

Connect:

```bash
docker exec -it redis-demo redis-cli
```

Ping:

```bash
PING
```

Expected:

```text
PONG
```

Store data:

```bash
SET product_1 "Laptop"
```

Read data:

```bash
GET product_1
```
## Expected output 
      "Laptop"

### Why Redis matters

Redis is useful for:

- Shopping carts
- User sessions
- Product cache
- Frequently viewed items

---

# 3. Transactions

Transactions guarantee that multiple operations succeed or fail together.

## Example

Start transaction:

```sql
BEGIN;
```

Reduce stock:

```sql
UPDATE products
SET stock = stock - 1
WHERE id = 1;
```

Create order:

```sql
INSERT INTO orders(customer_id, status)
VALUES (1, 'paid');
```

Commit:

```sql
COMMIT;
```

## Rollback

```sql
ROLLBACK;
```

### Benefits

- Prevents partial updates
- Ensures consistency
- Essential for payments and orders

---
Why transactions matter

If payment succeeds but stock update fails:

      customer charged
      inventory incorrect

Transactions prevent partial failures.

# 4. Docker Volumes

Volumes keep data even when containers are recreated.

## PostgreSQL Volume Example

```yaml
postgres:
  image: postgres:16
  container_name: sql-demo
  environment:
    POSTGRES_USER: student
    POSTGRES_PASSWORD: student
    POSTGRES_DB: shop
  ports:
    - "5432:5432"
  volumes:
    - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Restart

```bash
docker compose down
docker compose up -d
```

### Benefits

- Persistent storage
- Prevents data loss
- Production-ready setup

---

# 5. Architecture Diagram

Example architecture:

```text
                Users
                  |
                  ▼
           Frontend UI
                  |
                  ▼
             Backend API
                  |
    ┌─────────────┼─────────────┐
    ▼             ▼             ▼
 PostgreSQL    MongoDB       Redis
 Orders        Products      Cache
 Payments      Catalog       Sessions
 Inventory
```

## Database Responsibilities

### PostgreSQL

Used for:

- Orders
- Payments
- Inventory

Reason:

- Strong consistency
- Transactions
- Relational data

### MongoDB

Used for:

- Product catalog
- Flexible product attributes
- Document storage

Reason:

- Flexible schema
- Easy horizontal scaling

### Redis

Used for:

- Sessions
- Caching
- Shopping carts

Reason:

- Extremely fast reads and writes

---

# Discussion

## When SQL is best

- Financial transactions
- Inventory management
- Order processing
- Strong consistency

## When NoSQL is best

- Product catalogs
- Analytics
- Logs
- Flexible schemas

## Eventual Consistency

Suitable for:

- Recommendations
- Analytics
- Search indexing

## Strong Consistency

Required for:

- Payments
- Orders
- Inventory

---

# Conclusion

This stretch goal demonstrates:

- Performance optimization with pagination
- Fast caching with Redis
- Safe transactions
- Persistent storage using Docker volumes
- Scalable cloud architecture design

---

# Key Skills Demonstrated

* Data Modeling
* SQL & NoSQL Databases
* CRUD Operations
* Query Optimization
* Database Indexing
* Docker Containerization
* Python Database Integration
* Cloud Architecture Design
* Caching Strategies
* Scalability Concepts
* Transactions & Consistency
* System Design

---

# Author

**Muhammad Akanda**

IoT & Embedded Systems Developer
Cloud Development | Data Platforms | Python | Docker | Databases
