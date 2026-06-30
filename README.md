# Cloud Development – SQL & NoSQL Database Lab

A hands-on cloud development project demonstrating how to deploy, connect, and manage relational and NoSQL databases using Docker. This project explores PostgreSQL and MongoDB through CRUD operations, Python integration, data modeling, performance optimization, and cloud architecture best practices.

---

## 📖 Project Overview

The project simulates a real-world cloud development scenario for **NovaStore**, a growing Nordic e-commerce platform experiencing several database-related challenges:

- Slow database queries
- Duplicate customer records
- Negative inventory caused by concurrent purchases
- Complex product data
- Increasing traffic and scalability requirements

The goal is to evaluate when to use SQL versus NoSQL while learning modern cloud development practices.

---

## 🎯 Learning Objectives

- Deploy databases using Docker
- Connect to PostgreSQL and MongoDB locally
- Implement CRUD operations
- Compare SQL and NoSQL data modeling
- Integrate databases using Python
- Identify database bottlenecks
- Discuss scalability and architectural trade-offs

---

## 🛠 Technologies Used

| Technology | Purpose |
|------------|---------|
| Docker | Containerization |
| Docker Compose | Multi-container management |
| PostgreSQL 16 | Relational database |
| MongoDB 7 | NoSQL document database |
| Python 3 | Database integration |
| psycopg2 | PostgreSQL Python driver |
| PyMongo | MongoDB Python driver |
| Redis (Stretch Goal) | In-memory caching |

---

# Project Structure

```text
Cloud_development/
│
├── docker-compose.yml
├── postgres_test.py
├── mongo_test.py
├── README.md
└── DEL8-Stretch-Goals.md
```

---

# System Architecture

```text
                 Users
                    │
                    ▼
            Client Application
                    │
                    ▼
               Python Backend
                    │
      ┌─────────────┼──────────────┐
      ▼             ▼              ▼
 PostgreSQL      MongoDB         Redis
 Orders          Products        Cache
 Payments        Catalog         Sessions
 Inventory
```

---

# Getting Started

## Prerequisites

Install the following software:

- Docker Desktop
- Python 3.11+
- Git
- Visual Studio Code (recommended)

---

# Clone the Repository

```bash
git clone https://github.com/yourusername/cloud-development.git
cd cloud-development
```

---

# Start the Databases

```bash
docker compose up -d
```

Verify containers:

```bash
docker ps
```

Expected containers:

- sql-demo
- nosql-demo

---

# PostgreSQL Connection

Connect to PostgreSQL:

```bash
docker exec -it sql-demo psql -U student -d shop
```

Test connection:

```sql
SELECT NOW();
```

---

# MongoDB Connection

Connect to MongoDB:

```bash
docker exec -it nosql-demo mongosh
```

Switch database:

```javascript
use shop
```

---

# SQL Database Schema

The relational database contains four tables:

- customers
- products
- orders
- order_items

Relationships are implemented using foreign keys.

---

# PostgreSQL CRUD Operations

### Create

```sql
INSERT INTO customers(name,email)
VALUES('Sara','sara@example.com');
```

### Read

```sql
SELECT * FROM customers;
```

### Update

```sql
UPDATE orders
SET status='paid'
WHERE id=1;
```

### Delete

```sql
DELETE FROM order_items
WHERE product_id=1;

DELETE FROM products
WHERE id=1;
```

---

# MongoDB CRUD Operations

### Create

```javascript
db.customers.insertOne({
    name:"Sara",
    email:"sara@example.com"
})
```

### Read

```javascript
db.customers.find().pretty()
```

### Update

```javascript
db.orders.updateOne(
    {order_id:"order_1"},
    {$set:{status:"paid"}}
)
```

### Delete

```javascript
db.customers.deleteOne({
    email:"sara@example.com"
})
```

---

# Python Integration

## PostgreSQL

Install dependency

```bash
py -m pip install psycopg2-binary
```

Run

```bash
py postgres_test.py
```

---

## MongoDB

Install dependency

```bash
py -m pip install pymongo
```

Run

```bash
py mongo_test.py
```

---

# Database Design

## PostgreSQL

Used for:

- Customers
- Orders
- Payments
- Inventory

Advantages

- ACID transactions
- Foreign keys
- Strong consistency
- Relational queries
- JOIN support

---

## MongoDB

Used for:

- Product catalog
- Flexible product attributes
- Embedded documents

Advantages

- Flexible schema
- Horizontal scaling
- Fast document retrieval

---

# Performance Improvements

## SQL

Created index

```sql
CREATE INDEX idx_customers_email
ON customers(email);
```

Benefits

- Faster search by email
- Reduced query time

---

## MongoDB

Created unique index

```javascript
db.customers.createIndex(
    {email:1},
    {unique:true}
)
```

Benefits

- Prevent duplicate customers
- Improved data integrity

---

# Common Issues Solved

## Slow Queries

Problem

Using

```sql
LOWER(email)
```

prevented index usage.

Solution

- Create indexes
- Store normalized data

---

## Duplicate Users

Solution

Create a unique MongoDB index on email.

---

## Negative Inventory

Problem

Concurrent purchases may reduce stock below zero.

Solution

- Database transactions
- Row locking
- Conditional updates

---

# Stretch Goals

Implemented and practiced:

- Pagination
- Redis caching
- Database transactions
- Docker volumes
- Architecture design

---

# Future Improvements

- REST API
- Authentication
- Redis integration
- Docker volumes
- Kubernetes deployment
- CI/CD pipeline
- Unit testing
- Logging and monitoring

---

# Skills Demonstrated

- Docker containerization
- PostgreSQL
- MongoDB
- SQL CRUD
- NoSQL CRUD
- Python database connectivity
- Database indexing
- Transactions
- Performance optimization
- Cloud architecture
- Data modeling

---

# References

- PostgreSQL Documentation
- MongoDB Documentation
- Docker Documentation
- Python Documentation

---

# License

This project was developed for educational purposes as part of a Cloud Development course.

---

## Author

**Muhammad Jubayer Akanda**

Cloud Development | Data Engineering | Software Development

GitHub: https://github.com/muhaka-1
