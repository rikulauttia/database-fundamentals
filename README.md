# 🛢️ Database Fundamentals

<div align="center">
  
![Database Banner](https://img.shields.io/badge/Database-Fundamentals-blue?style=for-the-badge&logo=postgresql)

[![SQL](https://img.shields.io/badge/SQL-Advanced-orange?style=flat-square&logo=postgresql)](https://github.com/rikulauttia/database-fundamentals)
[![NoSQL](https://img.shields.io/badge/NoSQL-MongoDB-green?style=flat-square&logo=mongodb)](https://github.com/rikulauttia/database-fundamentals)
[![Python](https://img.shields.io/badge/Python-SQLite-blue?style=flat-square&logo=python)](https://github.com/rikulauttia/database-fundamentals)
[![Transactions](https://img.shields.io/badge/ACID-Transactions-red?style=flat-square)](https://github.com/rikulauttia/database-fundamentals)
[![Indexing](https://img.shields.io/badge/Performance-Indexing-yellow?style=flat-square)](https://github.com/rikulauttia/database-fundamentals)

</div>

## 📋 Overview

This repository contains practical exercises and implementations from a database fundamentals course. It explores both theoretical concepts and hands-on applications of database systems, from SQL queries to NoSQL databases, indexing performance, and transaction management.

## 🧩 Exercise Collection

### 1️⃣ Database Programming with SQLite

Implementations of Python functions to query and analyze city bike trip data stored in SQLite. Features include:

- User distance and speed calculations
- City-based trip duration analysis
- User tracking across multiple cities
- Daily trip statistics
- Popular starting points identification

<details>
<summary>View Implementation Details</summary>

```python
# Sample function: Finding the total distance traveled by a user
def distance_of_user(user):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT SUM(distance)
    FROM Trips
    JOIN Users ON Trips.user_id = Users.id
    WHERE Users.name = ?
    """

    cursor.execute(query, (user,))
    result = cursor.fetchone()[0]
    conn.close()
    return result
```

</details>

### 2️⃣ Database Design & Schema Creation

Design and implementation of a university course management system with:

- Tables for teachers, courses, students, credits, and groups
- Advanced query capabilities for course-student-teacher relationships
- Grade distribution analysis
- Cross-relational statistics gathering

<details>
<summary>View Database Schema</summary>

```sql
CREATE TABLE teachers (
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE courses (
    id INTEGER PRIMARY KEY,
    name TEXT,
    credits INTEGER
);

CREATE TABLE course_teachers (
    id INTEGER PRIMARY KEY,
    course_id INTEGER,
    teacher_id INTEGER,
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(id)
);

/* Additional tables for students, credits, groups, etc. */
```

</details>

### 3️⃣ Indexing Performance Analysis

Experimental evaluation of database indexing strategies, measuring:

- Query performance with and without indexes
- Effect of index creation timing (before vs. after data insertion)
- Database file size impacts
- Performance metrics across different strategies

<details>
<summary>View Test Results</summary>

| Test Scenario | Row Insertion Time | Query Execution Time | Database Size |
| ------------- | :----------------: | :------------------: | :-----------: |
| No Index      |      1.50 sec      |      25.25 sec       |   19.19 MB    |
| Index Before  |      2.03 sec      |       0.18 sec       |   30.97 MB    |
| Index After   |      1.51 sec      |       0.17 sec       |   29.70 MB    |

</details>

### 4️⃣ Transaction Behavior Analysis

Investigation of how multiple concurrent transactions interact in SQLite, examining:

- Lock behavior between transactions
- Transaction isolation levels
- Conflict resolution strategies
- Success/failure patterns in concurrent operations

<details>
<summary>View Transaction Test Cases</summary>

**Test Case Example:**

```
Transaction 1                Transaction 2
--------------                --------------
BEGIN;
SELECT x FROM Test;
                             BEGIN;
                             SELECT x FROM Test;
                             UPDATE Test SET x=2;
                             COMMIT;
UPDATE Test SET x=3;
COMMIT;
```

**Result Analysis:**
Transaction isolation demonstrates that Transaction 2's changes are not visible to Transaction 1 until committed, while Transaction 1's lock prevents Transaction 2 from modifying the same data concurrently.

</details>

### 5️⃣ NoSQL Database Queries (MongoDB)

Implementation of MongoDB queries using Python to analyze real estate data:

- Filtering by zip code, construction year, and apartment size
- Transaction history analysis
- Complex aggregation pipelines
- Document-based data retrieval

<details>
<summary>View MongoDB Query Examples</summary>

```python
# Finding apartments sold between 2010-2012
myynti_count = apartments.count_documents({
    "transactions": {
        "$elemMatch": {
            "date": {
                "$gte": "2010-01-01",
                "$lte": "2012-12-31"
            }
        }
    }
})

# Finding maximum selling price using aggregation
pipeline = [
    {"$unwind": "$transactions"},
    {"$group": {"_id": None, "max_price": {"$max": "$transactions.selling_price"}}},
    {"$project": {"_id": 0, "max_price": 1}}
]
result = list(apartments.aggregate(pipeline))
max_price = result[0]["max_price"]
```

</details>

## 🧠 Key Database Concepts Covered

<table>
  <tr>
    <td align="center"><b>Relational Model</b></td>
    <td align="center"><b>NoSQL</b></td>
    <td align="center"><b>Performance</b></td>
  </tr>
  <tr>
    <td>
      • SQL Queries<br>
      • Normalization<br>
      • Relationships<br>
      • Schema Design
    </td>
    <td>
      • Document Databases<br>
      • MongoDB Queries<br>
      • Non-relational Modeling<br>
      • Aggregation Pipelines
    </td>
    <td>
      • Indexing Strategies<br>
      • Query Optimization<br>
      • Execution Analysis<br>
      • Performance Testing
    </td>
  </tr>
  <tr>
    <td align="center"><b>Transactions</b></td>
    <td align="center"><b>Database Theory</b></td>
    <td align="center"><b>Implementation</b></td>
  </tr>
  <tr>
    <td>
      • ACID Properties<br>
      • Concurrency Control<br>
      • Lock Management<br>
      • Conflict Resolution
    </td>
    <td>
      • Relational Algebra<br>
      • Functional Dependencies<br>
      • Normal Forms<br>
      • Constraints & Keys
    </td>
    <td>
      • Python Integration<br>
      • SQLite Operations<br>
      • MongoDB Access<br>
      • Performance Measurement
    </td>
  </tr>
</table>

## 📊 Performance Insights from Indexing Analysis

The implementation demonstrates significant query optimization through proper indexing:

```
Query execution without index:    25.25 seconds
Query execution with index:       0.17 seconds
Speedup factor:                   ~148x
```

This highlights how critical indexing is for real-world database performance, especially for frequently queried fields.

## 🔍 Transaction Isolation Observations

Analysis of transaction behavior reveals:

1. **Transaction Locks** - Active transactions can block other transactions from modifying the same data
2. **Visibility Rules** - Changes are only visible to other transactions after being committed
3. **Concurrent Operations** - Read operations don't block other reads, but writes can block both reads and writes

## 🌐 Future Work

- [ ] Implement more complex database scenarios
- [ ] Add distributed database examples
- [ ] Compare performance across different database engines
- [ ] Explore advanced indexing techniques

## 📖 References

- Database Systems: The Complete Book
- MongoDB Documentation
- SQLite Documentation
- Transaction Processing: Concepts and Techniques

---

<div align="center">
  <sub>Built with ❤️ by Riku Lauttia</sub>
</div>
