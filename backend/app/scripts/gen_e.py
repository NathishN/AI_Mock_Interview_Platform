"""Generator for Category E: SQL and Data Analytics (50 questions).
25 questions in 01.json, 25 in 02.json.
Technical category: queries, analytics frameworks, business metric formulas, key points, common mistakes, follow-ups.
"""
import json
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parents[2] / "data" / "src" / "E_sql"

PART1 = [
    {
        "q": "What is the logical query processing order in SQL? How does it differ from lexical written order?",
        "sub": "SQL Execution Order",
        "d": "Intermediate",
        "ans": "SQL queries are written in lexical order: `SELECT -> FROM -> WHERE -> GROUP BY -> HAVING -> ORDER BY -> LIMIT`. However, the relational database engine executes clauses in a different logical order: 1) `FROM` and `JOIN` (identify source tables and Cartesian products), 2) `WHERE` (filter individual rows before grouping), 3) `GROUP BY` (aggregate rows into buckets), 4) `HAVING` (filter grouped buckets), 5) `SELECT` (evaluate expressions and assign column aliases), 6) `DISTINCT` (eliminate duplicate rows), 7) `ORDER BY` (sort output rows), and 8) `LIMIT / OFFSET` (truncate result set). This explains why column aliases declared in `SELECT` cannot be referenced in `WHERE` or `GROUP BY` clauses, but are available in `ORDER BY`.",
        "kp": ["Logical order: FROM/JOIN -> WHERE -> GROUP BY -> HAVING -> SELECT -> DISTINCT -> ORDER BY -> LIMIT", "Column aliases defined in SELECT are not visible to WHERE or GROUP BY", "WHERE filters individual base rows; HAVING filters aggregated groups", "ORDER BY runs after SELECT, allowing sorting on computed column aliases"],
        "cm": ["Attempting to filter by a calculated column alias in the WHERE clause", "Confusing lexical syntax order with relational execution order", "Placing aggregation functions like SUM() inside WHERE clauses"],
        "fu": ["Why can aliases be referenced in `ORDER BY` but not in `HAVING` in standard SQL?", "How do subqueries or CTEs allow filtering by calculated aliases?"],
        "tags": ["sql", "execution-order", "query-lifecycle", "rdbms"]
    },
    {
        "q": "Explain the difference between the `WHERE` clause and the `HAVING` clause in SQL.",
        "sub": "Filtering & Aggregation",
        "d": "Beginner",
        "ans": "Both clauses filter data, but operate at different stages of query execution. `WHERE` filters individual rows BEFORE any grouping or aggregation takes place; it cannot contain aggregate functions like `SUM()`, `AVG()`, or `COUNT()`. `HAVING` filters aggregated group records AFTER the `GROUP BY` clause has evaluated; it operates on group properties and conditions involving aggregate functions. For example, `WHERE salary > 50000` filters out low-earning employees before grouping by department, while `HAVING COUNT(*) > 5` filters out departments that have 5 or fewer employees after grouping. Using WHERE to eliminate irrelevant rows early improves query performance.",
        "kp": ["`WHERE` filters individual rows before grouping; cannot use aggregate functions", "`HAVING` filters aggregated groups after GROUP BY; uses aggregate functions", "Conditions on non-aggregated columns should be placed in `WHERE` for speed", "Can be used together in the same query"],
        "cm": ["Placing row-level non-aggregated filters inside `HAVING`, slowing down queries", "Attempting to write `WHERE COUNT(*) > 1` (causes SQL syntax error)", "Thinking HAVING can replace WHERE entirely without performance penalties"],
        "fu": ["Can a query have a `HAVING` clause without an explicit `GROUP BY` clause?", "What happens to NULL values when evaluating conditions in WHERE vs HAVING?"],
        "tags": ["sql", "where-vs-having", "aggregation", "filtering"]
    },
    {
        "q": "Explain the differences between INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL OUTER JOIN, and CROSS JOIN.",
        "sub": "SQL Joins",
        "d": "Beginner",
        "ans": "1) `INNER JOIN`: returns only rows where matching keys exist in both tables. 2) `LEFT JOIN` (LEFT OUTER JOIN): returns all rows from the left table, with matched data from the right table, or NULLs where no match exists. 3) `RIGHT JOIN`: returns all rows from the right table, matched data from the left, or NULLs. 4) `FULL OUTER JOIN`: returns all rows when there is a match in either table; unmatched sides are populated with NULLs. 5) `CROSS JOIN`: produces the Cartesian product of both tables, pairing every row from table A with every row from table B (yielding count(A) * count(B) rows), useful for generating grid combinations without join predicates.",
        "kp": ["INNER JOIN: intersection of matching keys from both tables", "LEFT JOIN: all left rows preserved; right unmatched filled with NULL", "RIGHT JOIN: all right rows preserved; left unmatched filled with NULL", "FULL OUTER JOIN: union of all rows from both tables with NULL padding", "CROSS JOIN: Cartesian product of all rows without join conditions"],
        "cm": ["Accidentally converting a LEFT JOIN into an INNER JOIN by placing a right-table condition in the WHERE clause instead of ON", "Executing unintended CROSS JOINs on large tables, causing massive memory spikes", "Confusing NULL values produced by outer joins with actual stored NULL values in data"],
        "fu": ["How does placing a filter condition in the `ON` clause differ from placing it in the `WHERE` clause during a LEFT JOIN?", "How do you simulate a FULL OUTER JOIN in MySQL using UNION?"],
        "tags": ["sql", "joins", "inner-join", "left-join", "cross-join"]
    },
    {
        "q": "What is a self join in SQL and when is it typically used? Provide a concrete example.",
        "sub": "SQL Joins",
        "d": "Intermediate",
        "ans": "A self join is a regular join in which a table is joined with itself. It requires distinct table aliases (e.g., `e` for employee, `m` for manager) to differentiate the two roles in the query. Self joins are typically used to model hierarchical data, parent-child relationships within a single table, or compare rows within the same table. A classic example is querying employee and manager names from an `Employees` table where `manager_id` references `employee_id`:\n\n```sql\nSELECT e.name AS employee_name, m.name AS manager_name\nFROM employees e\nLEFT JOIN employees m ON e.manager_id = m.employee_id;\n```\nUsing LEFT JOIN ensures top-level executives without a manager are not excluded from results.",
        "kp": ["Join table with itself using distinct table aliases", "Essential for hierarchical and recursive data structures (e.g., Employee-Manager)", "Can compare rows within the same table (e.g., finding price changes over time)", "Use LEFT JOIN to retain root nodes that lack parent references"],
        "cm": ["Forgetting table aliases, resulting in ambiguous column name errors", "Using INNER JOIN and accidentally filtering out the CEO/root record with NULL parent ID", "Unbounded self joins that inadvertently produce Cartesian products"],
        "fu": ["How do recursive Common Table Expressions (CTEs) handle deep organizational hierarchies better than chained self joins?", "How would you find all pairs of customers living in the same city using a self join?"],
        "tags": ["sql", "self-join", "hierarchical-data", "aliases"]
    },
    {
        "q": "What is the difference between `UNION` and `UNION ALL` in SQL? When should you prefer one over the other?",
        "sub": "Set Operations",
        "d": "Beginner",
        "ans": "Both operators combine result sets from two or more SELECT queries into a single result set. Requirement: all queries must have the identical number of columns with compatible data types in corresponding positions. 1) `UNION ALL` combines all rows directly, preserving duplicates; it requires no sorting and is fast with minimal computational overhead. 2) `UNION` combines rows and performs an internal distinct sorting operation to eliminate all duplicate rows across queries. Rule of thumb: always prefer `UNION ALL` unless duplicate elimination is explicitly required by business rules, as `UNION` introduces expensive disk and memory sorting overhead on large datasets.",
        "kp": ["UNION ALL retains duplicates; fast with no sort overhead", "UNION removes duplicates; requires sorting/hashing across results", "Queries must have matching column counts and compatible data types", "Default to UNION ALL unless duplicate elimination is strictly needed"],
        "cm": ["Defaulting to `UNION` blindly when data is already disjoint, incurring needless performance penalties", "Trying to combine queries with mismatched column counts or incompatible types", "Expecting UNION to maintain a predictable row order without an explicit outer ORDER BY"],
        "fu": ["What other set operators exist in SQL (INTERSECT, EXCEPT / MINUS)?", "How does UNION compare with JOIN in terms of combining data?"],
        "tags": ["sql", "union", "union-all", "set-operations", "performance"]
    },
    {
        "q": "What are window functions in SQL and how do they differ from standard aggregate functions with `GROUP BY`?",
        "sub": "Window Functions",
        "d": "Intermediate",
        "ans": "Standard aggregate functions (like `SUM()`, `AVG()`) combined with `GROUP BY` collapse multiple rows into a single aggregated summary row, losing individual row identities and detail columns. Window functions perform calculations across a set of table rows related to the current row (the 'window' defined by the `OVER()` clause), but do NOT collapse rows: every individual row retains its separate identity and detail values while displaying the computed aggregate alongside it. Window clauses support `PARTITION BY` (to divide rows into calculation partitions) and `ORDER BY` (to define calculation sequence for ranking, running totals, and moving averages).",
        "kp": ["Window functions compute over partitions without collapsing individual rows", "`GROUP BY` collapses multiple rows into a single summary record", "`OVER(PARTITION BY ... ORDER BY ...)` defines calculation window", "Allows simultaneous display of row-level details and aggregate values"],
        "cm": ["Attempting to use window functions directly inside WHERE or HAVING clauses", "Confusing PARTITION BY with GROUP BY", "Forgetting the ORDER BY clause in window specifications when calculating running totals or ranks"],
        "fu": ["Why are window functions evaluated after WHERE and HAVING clauses in the logical query order?", "How can you filter by the output of a window function using a CTE or subquery?"],
        "tags": ["sql", "window-functions", "over-clause", "analytics"]
    },
    {
        "q": "Explain the differences between `ROW_NUMBER()`, `RANK()`, and `DENSE_RANK()` in SQL with a tie-breaking example.",
        "sub": "Ranking Functions",
        "d": "Intermediate",
        "ans": "All three are window ranking functions that assign integer positions based on an `ORDER BY` clause, but handle identical duplicate values (ties) differently: 1) `ROW_NUMBER()` assigns a strict, unique sequential integer (1, 2, 3, 4...) to every row regardless of ties, arbitrarily breaking ties unless further order columns are provided. 2) `RANK()` assigns identical ranks to tied values, but skips subsequent rank numbers by the number of ties (e.g., scores 90, 80, 80, 70 receive ranks 1, 2, 2, 4). 3) `DENSE_RANK()` assigns identical ranks to tied values, but does NOT skip any rank numbers (scores 90, 80, 80, 70 receive ranks 1, 2, 2, 3). For finding the N-th highest value without gaps, `DENSE_RANK()` is preferred.",
        "kp": ["`ROW_NUMBER()`: strictly sequential (1, 2, 3, 4), no ties", "`RANK()`: identical ranks for ties, skips subsequent numbers (1, 2, 2, 4)", "`DENSE_RANK()`: identical ranks for ties, no gap in numbering (1, 2, 2, 3)", "Used with `OVER (PARTITION BY ... ORDER BY ...)`"],
        "cm": ["Using `ROW_NUMBER()` for leaderboard ranks where tied candidates deserve equal standing", "Using `RANK()` to find the second-highest salary, which fails if two employees tie for first", "Forgetting the ORDER BY clause inside the OVER specification"],
        "fu": ["Which ranking function is ideal for deduplicating exact duplicate records?", "How do you retrieve the top 3 highest-earning employees in each department using `DENSE_RANK()`?"],
        "tags": ["sql", "row-number", "rank", "dense-rank", "window-functions"]
    },
    {
        "q": "How do you write a query to find the N-th highest salary from an `Employee` table in SQL?",
        "sub": "SQL Problem Solving",
        "d": "Intermediate",
        "ans": "Using `DENSE_RANK()` within a Common Table Expression (CTE) handles ties correctly and is database-agnostic:\n\n```sql\nWITH RankedSalaries AS (\n    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rank_pos\n    FROM employees\n)\nSELECT DISTINCT salary\nFROM RankedSalaries\nWHERE rank_pos = 2; -- replace 2 with N\n```\n\nAlternative database-specific approach using `LIMIT / OFFSET`:\n```sql\nSELECT DISTINCT salary\nFROM employees\nORDER BY salary DESC\nLIMIT 1 OFFSET 1; -- for 2nd highest (N-1)\n```\nThe CTE with `DENSE_RANK()` is preferred because it handles cases where multiple employees share the top salary.",
        "kp": ["`DENSE_RANK() OVER (ORDER BY salary DESC)` ranks salaries without gaps", "CTE or subquery wraps the window function so it can be filtered in WHERE", "`DISTINCT` ensures clean return of the unique salary value", "`LIMIT 1 OFFSET N-1` is an alternative for databases like MySQL/PostgreSQL"],
        "cm": ["Using `LIMIT 1 OFFSET 1` without `DISTINCT`, returning the highest salary again if two people share top salary", "Using `RANK()` instead of `DENSE_RANK()`, causing N-th rank to be skipped during ties", "Not handling empty tables or tables with fewer than N distinct salaries"],
        "fu": ["What does the query return if there are fewer than N distinct salaries in the table?", "How do you solve this using a correlated subquery without window functions?"],
        "tags": ["sql", "dense-rank", "second-highest-salary", "cte", "problem-solving"]
    },
    {
        "q": "How do you calculate running totals (cumulative sum) and moving averages in SQL using window functions?",
        "sub": "Window Calculations",
        "d": "Intermediate",
        "ans": "A running total computes the cumulative sum of a metric from the beginning of a partition up to the current row:\n\n```sql\nSELECT order_date, amount,\n       SUM(amount) OVER (ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total\nFROM orders;\n```\nOmitting the window frame defaults to `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`, but explicit `ROWS BETWEEN` is faster and handles duplicate dates properly. A 7-day moving average uses a sliding frame:\n\n```sql\nSELECT order_date, amount,\n       AVG(amount) OVER (ORDER BY order_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS moving_avg_7d\nFROM orders;\n```",
        "kp": ["`SUM(col) OVER (ORDER BY col)` calculates cumulative running totals", "`ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` defines cumulative frame", "`ROWS BETWEEN N PRECEDING AND CURRENT ROW` calculates moving rolling averages", "`PARTITION BY` resets running calculations per category or customer"],
        "cm": ["Confusing `ROWS` (physical row count) with `RANGE` (logical value range) in frame clauses", "Forgetting the ORDER BY in the OVER clause, which converts it to a total grand sum", "Using self joins to compute running totals, which degrades to O(n^2) performance"],
        "fu": ["What is the difference between `ROWS` and `RANGE` window frame specifications?", "How does `PARTITION BY customer_id` reset the running total for each individual customer?"],
        "tags": ["sql", "running-total", "moving-average", "window-functions", "cumulative-sum"]
    },
    {
        "q": "Explain `LAG()` and `LEAD()` window functions. Provide a use case such as calculating month-over-month growth.",
        "sub": "Window Navigation",
        "d": "Intermediate",
        "ans": "`LAG(column, offset, default)` accesses data from a preceding row in the same result set without a self join, while `LEAD(column, offset, default)` accesses data from a subsequent row. Default offset is 1. They are used for time-series comparisons, calculating deltas, and detecting status transitions. Example calculating Month-over-Month (MoM) revenue growth:\n\n```sql\nWITH MonthlyRevenue AS (\n    SELECT DATE_TRUNC('month', order_date) AS month, SUM(amount) AS revenue\n    FROM orders\n    GROUP BY 1\n)\nSELECT month, revenue,\n       LAG(revenue, 1) OVER (ORDER BY month) AS prev_month_revenue,\n       ROUND(100.0 * (revenue - LAG(revenue, 1) OVER (ORDER BY month)) / \n             NULLIF(LAG(revenue, 1) OVER (ORDER BY month), 0), 2) AS mom_growth_pct\nFROM MonthlyRevenue;\n```",
        "kp": ["`LAG()` looks back N rows; `LEAD()` looks ahead N rows", "Eliminates complex and slow self-joins on timestamps", "Essential for period-over-period growth rates, churn analysis, and gaps", "Use `NULLIF(val, 0)` in division to prevent division-by-zero errors"],
        "cm": ["Forgetting `ORDER BY` in the window clause, resulting in nondeterministic previous values", "Dividing by zero when the previous period had 0 revenue without `NULLIF`", "Not handling the first row where `LAG()` naturally returns NULL"],
        "fu": ["What default value does `LAG()` return for the first row if no default is specified?", "How do you find inactive gaps between consecutive user logins using `LAG()`?"],
        "tags": ["sql", "lag", "lead", "mom-growth", "analytics"]
    },
    {
        "q": "What is a Common Table Expression (CTE) in SQL, and how does it compare to subqueries and temporary tables?",
        "sub": "CTEs & Modularity",
        "d": "Beginner",
        "ans": "A Common Table Expression (CTE) is a named, temporary result set defined within the execution scope of a single SQL statement using the `WITH` keyword: `WITH cte_name AS (SELECT ... ) SELECT ... FROM cte_name;`. Compared to subqueries, CTEs improve query readability, eliminate deeply nested parenthesis structures, and can be referenced multiple times within the same query. Compared to temporary tables (`CREATE TEMPORARY TABLE`), CTEs do not write metadata to disk, require no manual cleanup, and exist only for the query duration. Many modern optimizers materialize non-trivial CTEs or inline them for cost-based optimization.",
        "kp": ["Defined using `WITH cte_name AS (...)` preceding main query", "Dramatically improves readability over deeply nested subqueries", "Can be referenced multiple times within the same statement", "Exists strictly for query execution scope; no disk cleanup needed"],
        "cm": ["Believing CTEs persist across separate query executions in a session", "Creating dozens of sequential CTEs for operations that could be combined simply", "Assuming CTEs always materialize or index data like temporary tables"],
        "fu": ["How do recursive CTEs work for traversing graph or tree structures (e.g., BOM or Org charts)?", "What does the `MATERIALIZED` vs `NOT MATERIALIZED` hint do in PostgreSQL 12+ CTEs?"],
        "tags": ["sql", "cte", "with-clause", "subqueries", "readability"]
    },
    {
        "q": "How does three-valued logic work in SQL when handling `NULL` values? How do `COALESCE` and `NULLIF` help?",
        "sub": "NULL Handling",
        "d": "Intermediate",
        "ans": "In SQL, `NULL` represents the absence of a value or an unknown value. As a result, comparisons with NULL using standard equality operators (`=`, `!=`, `<>`) do not evaluate to `TRUE` or `FALSE`, but to `UNKNOWN`. This is SQL's three-valued logic (TRUE, FALSE, UNKNOWN). A condition in `WHERE` only passes rows when it evaluates strictly to `TRUE`; `UNKNOWN` is treated as false. To test for NULL, you must use `IS NULL` or `IS NOT NULL`. Two helper functions are vital: 1) `COALESCE(val1, val2, ...)` returns the first non-NULL argument, useful for providing default fallback values. 2) `NULLIF(a, b)` returns `NULL` if `a == b`, otherwise returns `a`, commonly used to prevent division-by-zero (`val / NULLIF(divisor, 0)`).",
        "kp": ["Three-valued logic: TRUE, FALSE, UNKNOWN; comparisons with NULL return UNKNOWN", "`col = NULL` is ALWAYS UNKNOWN; must use `IS NULL` or `IS NOT NULL`", "`COALESCE(a, b, c)` returns first non-null expression", "`NULLIF(a, b)` returns NULL if a equals b; prevents division by zero"],
        "cm": ["Writing `WHERE status = NULL` instead of `WHERE status IS NULL`", "Not realizing `NOT IN (SELECT col FROM table)` returns zero rows if ANY returned value is NULL", "Ignoring NULL handling in aggregate functions like `AVG()` which ignore NULLs"],
        "fu": ["Why does `WHERE id NOT IN (1, 2, NULL)` evaluate to UNKNOWN and return zero rows?", "How does `COUNT(*)` differ from `COUNT(column_name)` regarding NULL values?"],
        "tags": ["sql", "null-handling", "three-valued-logic", "coalesce", "nullif"]
    },
    {
        "q": "Explain the difference between `COUNT(*)`, `COUNT(1)`, and `COUNT(column_name)` in SQL.",
        "sub": "Aggregate Functions",
        "d": "Beginner",
        "ans": "`COUNT(*)` counts the total number of rows in the result set, including rows that contain NULL values across any or all columns. `COUNT(1)` evaluates the constant literal 1 for every row and counts the occurrences; in modern relational database optimizers (PostgreSQL, MySQL, SQL Server, Oracle), `COUNT(1)` and `COUNT(*)` generate identical query execution plans and have identical performance. `COUNT(column_name)`, however, counts only rows where the specified `column_name` is NOT NULL, skipping all NULL entries. `COUNT(DISTINCT column_name)` counts unique non-NULL values.",
        "kp": ["`COUNT(*)`: counts total rows regardless of NULL values", "`COUNT(1)`: identical execution plan and performance to `COUNT(*)` in modern DBs", "`COUNT(column_name)`: counts only rows where `column_name` IS NOT NULL", "`COUNT(DISTINCT column_name)`: counts unique non-null values"],
        "cm": ["Believing `COUNT(1)` is faster than `COUNT(*)` on modern databases (urban myth)", "Using `COUNT(column)` expecting total row count when column contains NULLs", "Thinking `COUNT(*)` scans all table columns in memory"],
        "fu": ["How does `COUNT(DISTINCT status)` handle NULL values in its tally?", "Why can `COUNT(*)` on an indexed table in PostgreSQL be slower than on MySQL MyISAM?"],
        "tags": ["sql", "count", "aggregates", "nulls", "performance"]
    },
    {
        "q": "What is the difference between correlated subqueries and non-correlated subqueries? Which is faster and why?",
        "sub": "Subqueries",
        "d": "Intermediate",
        "ans": "A non-correlated subquery is completely independent of the outer query; it can be executed standalone once, and its scalar value or result set is passed to the outer query (e.g., `WHERE salary > (SELECT AVG(salary) FROM employees)`). It executes once for the entire query. A correlated subquery references columns from the outer query table (e.g., `WHERE salary > (SELECT AVG(salary) FROM employees e2 WHERE e2.dept_id = e1.dept_id)`). Conceptually, the inner subquery must be re-evaluated for every row evaluated by the outer query. While database optimizers often rewrite correlated subqueries into joins or window functions, poorly written correlated subqueries can cause severe O(n*m) performance degradation.",
        "kp": ["Non-correlated: independent of outer query; executes once", "Correlated: references outer query columns; conceptually runs per outer row", "Correlated subqueries can create quadratic performance bottlenecks", "Often rewritten more efficiently using window functions or JOINs"],
        "cm": ["Using correlated subqueries inside the SELECT list when a single window function suffices", "Not realizing a correlated subquery executes repeatedly for each row in unoptimized engines", "Confusing EXISTS with IN for subquery membership checks"],
        "fu": ["How does `EXISTS` optimize correlated subqueries via short-circuit evaluation?", "When is `EXISTS` faster than `IN` when subqueries contain NULL values?"],
        "tags": ["sql", "subqueries", "correlated-subqueries", "optimization", "performance"]
    },
    {
        "q": "Explain `EXISTS` vs `IN` in SQL. How do they handle performance and `NULL` values differently?",
        "sub": "Subqueries & Predicates",
        "d": "Intermediate",
        "ans": "`IN` evaluates whether a value matches any member of an explicit list or subquery result. If the subquery contains even a single `NULL` value, `NOT IN` fails completely, evaluating to `UNKNOWN` and returning zero rows. `EXISTS` tests for the existence of rows returned by a subquery (`WHERE EXISTS (SELECT 1 FROM ...)`), returning a boolean `TRUE` or `FALSE` without inspecting actual column values; it handles NULLs safely. Performance: `EXISTS` uses short-circuit evaluation, stopping as soon as the first matching row is found. On modern optimizers, correlated `EXISTS` and `IN` on indexed columns often yield similar plans, but `EXISTS` is safer and faster on large subqueries with potential NULLs.",
        "kp": ["`EXISTS` checks boolean row existence and short-circuits on first match", "`IN` compares values; dangerous with `NOT IN` if subquery contains NULLs", "`EXISTS` ignores NULL value traps in subquery data", "`NOT EXISTS` is strongly preferred over `NOT IN` for safety with NULLs"],
        "cm": ["Using `NOT IN (SELECT ...)` where the subquery can return NULL, yielding an empty result set", "Writing `SELECT *` inside EXISTS instead of `SELECT 1` (though optimizers optimize both)", "Assuming IN is always faster without checking index availability"],
        "fu": ["Why does `WHERE id NOT IN (SELECT id FROM ...)` return empty if any id is NULL?", "How does an anti-join using LEFT JOIN ... WHERE right.id IS NULL compare to NOT EXISTS?"],
        "tags": ["sql", "exists", "in-clause", "subqueries", "null-traps"]
    },
    {
        "q": "How do you identify and delete duplicate rows from a table while keeping one copy in SQL?",
        "sub": "Data Cleaning in SQL",
        "d": "Intermediate",
        "ans": "Using a CTE with `ROW_NUMBER()` is the standard, safest method:\n\n```sql\nWITH DuplicateCTE AS (\n    SELECT id, email,\n           ROW_NUMBER() OVER (PARTITION BY email ORDER BY id ASC) AS row_num\n    FROM users\n)\nDELETE FROM users\nWHERE id IN (\n    SELECT id FROM DuplicateCTE WHERE row_num > 1\n);\n```\n`PARTITION BY email` groups identical records together, while `ROW_NUMBER()` assigns sequential numbers starting at 1. The first instance (`row_num = 1`) is preserved, while duplicates (`row_num > 1`) are targeted for deletion. In PostgreSQL/MySQL, this can also be done using a self join with `DELETE u1 FROM users u1 JOIN users u2 ON u1.email = u2.email AND u1.id > u2.id`.",
        "kp": ["`ROW_NUMBER() OVER (PARTITION BY key ORDER BY id)` identifies duplicates", "Keeps `row_num = 1` and deletes `row_num > 1`", "Enforces deterministic retention via `ORDER BY id ASC`", "Alternative self-join deletion using primary key comparison (`u1.id > u2.id`)"],
        "cm": ["Deleting based on `COUNT(*) > 1` without retaining a single unique record, wiping all data", "Using non-deterministic sorting in `ROW_NUMBER()`, deleting the wrong record version", "Not wrapping mass deletions in a transaction to verify affected row counts"],
        "fu": ["How do you prevent duplicate records from ever being inserted in the first place?", "How do you execute this deletion safely in batches on a table with 10 million rows?"],
        "tags": ["sql", "duplicates", "row-number", "data-cleaning", "delete"]
    },
    {
        "q": "What are primary keys, foreign keys, and unique constraints? What is referential integrity?",
        "sub": "Relational Constraints",
        "d": "Beginner",
        "ans": "1) Primary Key (PK): a column or set of columns (composite PK) that uniquely identifies each row in a table. It strictly enforces uniqueness and cannot contain `NULL` values; a table can have only one primary key. 2) Unique Constraint: enforces uniqueness across column values, but permits `NULL` values (one or multiple depending on SQL dialect); tables can have multiple unique constraints. 3) Foreign Key (FK): a column that references a primary or unique key in another table, enforcing referential integrity. Referential integrity guarantees that relationships between tables remain consistent: child rows cannot point to non-existent parent rows, and parent rows cannot be deleted if children exist unless cascading actions (`ON DELETE CASCADE`, `ON DELETE SET NULL`) are declared.",
        "kp": ["Primary Key: unique identifier, strictly NOT NULL, one per table", "Unique Constraint: enforces uniqueness, permits NULLs, multiple per table", "Foreign Key: enforces referential integrity by referencing valid parent keys", "Cascading actions: `ON DELETE CASCADE`, `SET NULL`, `RESTRICT`"],
        "cm": ["Assuming unique constraints forbid NULL values like primary keys do", "Omitting foreign keys and relying on application code to maintain referential integrity", "Using `ON DELETE CASCADE` blindly on critical audit data"],
        "fu": ["What is a surrogate key vs a natural key? What are the trade-offs of each?", "What happens when an `ON DELETE RESTRICT` constraint is triggered?"],
        "tags": ["sql", "primary-key", "foreign-key", "referential-integrity", "constraints"]
    },
    {
        "q": "What are the ACID properties in database management systems? Explain each with a banking transaction example.",
        "sub": "Database Transactions",
        "d": "Intermediate",
        "ans": "ACID guarantees reliable processing of database transactions: 1) Atomicity: 'all-or-nothing'. If transferring $100 from Account A to B, both debiting A and crediting B must succeed; if crediting B fails, debiting A is rolled back completely. 2) Consistency: transactions transition the database from one valid state to another, satisfying all schema rules, constraints (e.g., account balance >= 0), and triggers. 3) Isolation: concurrent transactions execute without interfering with each other; intermediate uncommitted states of transaction 1 are invisible to transaction 2 based on isolation levels. 4) Durability: once committed, transaction results survive power failures, crashes, or reboots, guaranteed via write-ahead logging (WAL) to disk.",
        "kp": ["Atomicity: all operations succeed or all rollback (all-or-nothing)", "Consistency: preserves all schema constraints, checks, and foreign keys", "Isolation: concurrent transactions execute independently without race conditions", "Durability: committed changes persist permanently across crashes via WAL"],
        "cm": ["Confusing Consistency in ACID with Consistency in the CAP theorem", "Assuming all databases provide maximum Serializable isolation by default", "Thinking Durability means data is immune to hardware disk destruction without backups"],
        "fu": ["What are the four standard SQL transaction isolation levels (Read Uncommitted to Serializable)?", "What is a dirty read, non-repeatable read, and phantom read?"],
        "tags": ["database", "acid", "transactions", "rdbms", "concurrency"]
    },
    {
        "q": "Explain transaction isolation levels in SQL. What anomalies do they prevent?",
        "sub": "Transaction Isolation",
        "d": "Advanced",
        "ans": "SQL defines four standard isolation levels that balance concurrency performance against data consistency anomalies: 1) `Read Uncommitted`: permits Dirty Reads (reading uncommitted changes from another transaction that might rollback). 2) `Read Committed` (default in PostgreSQL/SQL Server): prevents Dirty Reads, but permits Non-Repeatable Reads (reading the same row twice yields different values because another transaction committed an update). 3) `Repeatable Read` (default in MySQL InnoDB): prevents Dirty Reads and Non-Repeatable Reads, but may permit Phantom Reads (new rows inserted by another transaction appear in subsequent range queries). 4) `Serializable`: highest isolation; eliminates all anomalies by executing transactions as if strictly serial, using range locks or Multi-Version Concurrency Control (MVCC) with serialization failure retries.",
        "kp": ["Dirty Read: reading uncommitted data that may rollback", "Non-Repeatable Read: re-reading a row shows modified committed data", "Phantom Read: re-running range query shows newly inserted committed rows", "Levels: Read Uncommitted -> Read Committed -> Repeatable Read -> Serializable"],
        "cm": ["Assuming Read Committed prevents phantom rows or duplicate calculations", "Running Serializable isolation everywhere without handling serialization conflict retries", "Not knowing the default isolation level of your production database"],
        "fu": ["How does Multi-Version Concurrency Control (MVCC) achieve high concurrency without read locks?", "What error does PostgreSQL throw when a Serializable transaction conflicts?"],
        "tags": ["sql", "isolation-levels", "mvcc", "transactions", "concurrency"]
    },
    {
        "q": "Explain Database Normalization: First Normal Form (1NF), Second Normal Form (2NF), and Third Normal Form (3NF).",
        "sub": "Database Normalization",
        "d": "Intermediate",
        "ans": "Normalization organizes relational tables to eliminate data redundancy and insertion, update, and deletion anomalies. 1) 1NF (First Normal Form): requires atomic (indivisible) column values, unique row identities (primary key), and no repeating groups or comma-separated lists. 2) 2NF (Second Normal Form): satisfies 1NF AND eliminates partial dependencies—all non-key attributes must depend on the FULL primary key (applies to composite primary keys). 3) 3NF (Third Normal Form): satisfies 2NF AND eliminates transitive dependencies—non-key attributes must depend directly on the primary key, not on another non-key attribute ('the key, the whole key, and nothing but the key, so help me Codd').",
        "kp": ["1NF: atomic values, unique primary key, no repeating columns or arrays", "2NF: satisfies 1NF + no partial dependency on composite primary key", "3NF: satisfies 2NF + no transitive dependencies between non-key columns", "Prevents update, insert, and delete anomalies; saves storage space"],
        "cm": ["Storing comma-separated strings in a column, violating 1NF", "Confusing 2NF (partial key dependency) with 3NF (non-key transitive dependency)", "Believing extreme normalization (BCNF/5NF) is always optimal for analytical data warehouses"],
        "fu": ["What is Boyce-Codd Normal Form (BCNF) and when does 3NF fall short of it?", "Why do data warehouses deliberately denormalize tables into Star Schemas?"],
        "tags": ["database", "normalization", "1nf", "2nf", "3nf", "schema-design"]
    },
    {
        "q": "What is database denormalization? When and why would an engineer intentionally denormalize a database?",
        "sub": "Schema Design",
        "d": "Intermediate",
        "ans": "Denormalization is the deliberate strategy of introducing redundant data or pre-aggregated columns into a normalized relational schema to optimize read performance. While 3NF minimizes storage and eliminates update anomalies, querying highly normalized schemas requires expensive multi-table joins that degrade read throughput at scale. Engineers denormalize when: 1) Read traffic vastly outnumbers write traffic (e.g., e-commerce product catalogs), 2) Complex joins on high-volume tables cause latency bottlenecks, and 3) In analytical data warehouses where Star and Snowflake schemas store dimensional redundancies for rapid aggregation. Trade-offs: increased storage consumption and the requirement for application code or triggers to keep duplicate data synchronized.",
        "kp": ["Deliberate redundancy introduced to eliminate costly table joins", "Optimizes heavy read workloads at the expense of slower write operations", "Common in OLAP data warehouses, search caches, and reporting dashboards", "Requires synchronization mechanisms (triggers, background jobs) to prevent data drift"],
        "cm": ["Denormalizing prematurely without empirical query profiling measurements", "Failing to implement synchronization, leading to stale or conflicting data", "Confusing sloppy schema design with intentional engineering denormalization"],
        "fu": ["How does a Star Schema in a data warehouse exemplify intentional denormalization?", "What are materialized views and how do they automate denormalized caching?"],
        "tags": ["database", "denormalization", "performance", "olap", "schema-design"]
    },
    {
        "q": "How do database indexes (B-Tree indexes) work? What are clustered vs non-clustered indexes?",
        "sub": "Database Indexing",
        "d": "Intermediate",
        "ans": "A database index is a data structure (typically a self-balancing B-Tree) that speeds up data retrieval on specific columns at the cost of additional storage and slower writes (INSERT, UPDATE, DELETE must update index trees). B-Trees maintain sorted data with logarithmic O(log n) lookup, range scans, and insertions. 1) Clustered Index: dictates the physical on-disk storage order of the actual table rows; a table can have only ONE clustered index (usually the primary key). Leaf nodes contain the complete data rows. 2) Non-Clustered (Secondary) Index: a separate structure sorted by the indexed column; leaf nodes contain index keys and row pointers (or clustered key references) that point to the physical table location.",
        "kp": ["B-Tree structure provides O(log n) search, insert, and range queries", "Clustered index defines physical row order on disk; strictly one per table", "Non-clustered index stores sorted keys with pointers to base table data", "Trade-off: faster SELECT queries vs slower INSERT/UPDATE and extra disk storage"],
        "cm": ["Indexing every single column, severely degrading write/insert throughput", "Assuming an index is always used (optimizers ignore indexes on low-cardinality columns)", "Creating multiple clustered indexes on the same table (physically impossible)"],
        "fu": ["What is an index-only scan (covering index) and why is it exceptionally fast?", "Why are B-Trees preferred over Hash indexes or Binary Search Trees in databases?"],
        "tags": ["sql", "indexing", "b-tree", "clustered-index", "performance"]
    },
    {
        "q": "What is a composite index and why is column ordering (the Leftmost Prefix Rule) critical?",
        "sub": "Database Indexing",
        "d": "Intermediate",
        "ans": "A composite (multi-column) index is an index on two or more columns of a table: `CREATE INDEX idx_user_status ON users(department_id, status, created_at);`. Column ordering is critical due to the Leftmost Prefix Rule: the database can only use the index for queries that filter by the leftmost column(s) in sequence. The index on `(A, B, C)` can speed up queries filtering by `(A)`, `(A, B)`, or `(A, B, C)`. However, it CANNOT be used efficiently for queries filtering by `(B)` alone, `(C)` alone, or `(B, C)` without `A`. Best practice: place columns used in equality filters with highest selectivity first, followed by range filter columns.",
        "kp": ["Composite index covers multiple columns in a specific defined order", "Leftmost Prefix Rule: can only be used if leading leftmost columns are queried", "Index on (A, B, C) accelerates queries on A, (A,B), (A,B,C); useless for B or C alone", "Place highest-cardinality equality columns first, followed by range filter columns"],
        "cm": ["Creating an index on `(A, B)` and wondering why `WHERE B = 10` does a full table scan", "Creating separate individual indexes on A and B instead of one composite index", "Putting a range condition (`created_at > ...`) before an equality column in index definition"],
        "fu": ["What happens when a query filters on `A = 1 AND C = 2` with an index on `(A, B, C)`?", "How do covering indexes eliminate table lookups by using the `INCLUDE` clause?"],
        "tags": ["sql", "composite-index", "leftmost-prefix", "indexing", "query-optimization"]
    },
    {
        "q": "How do you use `EXPLAIN` and `EXPLAIN ANALYZE` to diagnose and optimize slow SQL queries?",
        "sub": "Query Optimization",
        "d": "Advanced",
        "ans": "`EXPLAIN` displays the query execution plan generated by the database optimizer without running the query, showing cost estimates, index choices, and join algorithms. `EXPLAIN ANALYZE` (or `EXPLAIN (ANALYZE, BUFFERS)` in PostgreSQL) actually executes the query, outputting real execution times and disk buffer statistics alongside optimizer estimates. Key warning signs: 1) `Seq Scan` (Sequential / Full Table Scan) on large tables instead of `Index Scan`, 2) High discrepancy between estimated row counts and actual row counts (indicating stale table statistics needing `ANALYZE`), 3) Expensive nested loop joins on large unindexed tables, and 4) Disk spills during sorting or hash aggregates.",
        "kp": ["`EXPLAIN`: estimates query execution plan, costs, and index usage", "`EXPLAIN ANALYZE`: executes query, reporting actual milliseconds and disk buffer hits", "Spot bottlenecks: Seq Scan vs Index Scan, nested loops, memory sort vs disk spills", "Discrepancies in estimated vs actual rows indicate stale table statistics"],
        "cm": ["Running `EXPLAIN ANALYZE` on destructive DELETE or UPDATE queries in production without transactions", "Relying on cost numbers alone without comparing actual execution milliseconds", "Ignoring full table scans on multi-million row tables"],
        "fu": ["What is the difference between an `Index Scan` and a `Bitmap Index Scan` in PostgreSQL?", "How does running `ANALYZE table_name` update optimizer statistics?"],
        "tags": ["sql", "explain", "explain-analyze", "query-optimization", "postgresql"]
    },
    {
        "q": "Why is `SELECT *` considered a dangerous anti-pattern in production SQL queries?",
        "sub": "SQL Best Practices",
        "d": "Beginner",
        "ans": "Using `SELECT *` in production code causes several problems: 1) Performance and I/O overhead: retrieves all columns from disk, consuming unnecessary I/O, network bandwidth, and application memory, especially for large TEXT, BLOB, or JSONB columns. 2) Prevents Covering Indexes: a covering index scan cannot be used because columns not in the index must be fetched from base table pages. 3) Fragility: if a column is added, renamed, or reordered in the table schema, application unpackers, positional tuples, and ORM projections can break silently. Explicitly naming required columns (`SELECT id, name, email`) ensures predictable contracts and optimal performance.",
        "kp": ["Fetches unnecessary columns, wasting disk I/O, network transit, and RAM", "Destroys ability of optimizer to use covering index scans", "Fragile to schema changes (breaks positional array unpackers)", "Explicitly specifying columns produces self-documenting, maintainable queries"],
        "cm": ["Using `SELECT *` inside subqueries or production API endpoint queries", "Ignoring bandwidth costs when tables contain massive JSON or text columns", "Thinking `SELECT *` makes code easier to maintain"],
        "fu": ["When is `SELECT *` acceptable (e.g., inside `EXISTS (SELECT * FROM ...)` or ad-hoc CLI exploration)?", "How does GraphQL address over-fetching on the API layer similar to explicit column selection?"],
        "tags": ["sql", "anti-patterns", "best-practices", "performance", "select-star"]
    }
]

PART2 = [
    {
        "q": "What is the difference between VLOOKUP, HLOOKUP, XLOOKUP, and INDEX-MATCH in Excel?",
        "sub": "Excel Analytics",
        "d": "Beginner",
        "ans": "1) `VLOOKUP(val, table, col_idx, [approx])`: searches vertically in the leftmost column of a table and returns values to the right; limitation: cannot look left, breaks if columns are inserted. 2) `HLOOKUP`: searches horizontally across the top row and looks downward. 3) `INDEX(array, row_num, [col_num]) + MATCH(lookup_val, lookup_array, [match_type])`: combination where MATCH finds the row index and INDEX retrieves the value; can look left or right, does not break when columns are inserted, and executes faster on large sheets. 4) `XLOOKUP`: modern formula (Excel 365) replacing all previous lookup functions; can search in any direction, defaults to exact match, handles missing values natively (`if_not_found`), and supports wildcard searches.",
        "kp": ["VLOOKUP searches leftmost column only and reads rightward", "INDEX-MATCH looks in any direction and remains resilient to column insertions", "XLOOKUP (Excel 365) modern standard: bidirectional, exact match default, built-in error handling", "Approximate match vs exact match (0 / FALSE)"],
        "cm": ["Forgetting the fourth argument `FALSE` (or 0) in VLOOKUP, causing erroneous approximate matches", "Inserting a column into a VLOOKUP table range, corrupting hardcoded column indices", "Using resource-heavy VLOOKUP across 100,000 rows when INDEX-MATCH or Power Query is faster"],
        "fu": ["Why is INDEX-MATCH computationally more efficient than VLOOKUP on large workbooks?", "How does XLOOKUP handle two-dimensional lookups (row and column simultaneously)?"],
        "tags": ["excel", "vlookup", "xlookup", "index-match", "data-analytics"]
    },
    {
        "q": "What are Pivot Tables in Excel and how do they facilitate rapid Exploratory Data Analysis (EDA)?",
        "sub": "Excel Analytics",
        "d": "Beginner",
        "ans": "A Pivot Table is an interactive Excel tool that rapidly summarizes, aggregates, groups, and slices large tabular datasets without writing complex formulas. It features four functional quadrants: 1) Rows: categorical grouping dimensions displayed vertically. 2) Columns: categorical dimensions displayed horizontally for cross-tabulation. 3) Values: numerical fields aggregated using functions like SUM, COUNT, AVERAGE, or percentage of total. 4) Filters (and Slicers): global subset filters. Pivot Tables allow analysts to quickly discover summary statistics, identify outliers, spot missing values, and analyze cross-dimensional patterns during initial EDA before formal SQL or Python modeling.",
        "kp": ["Four quadrants: Rows, Columns, Values, Filters/Slicers", "Rapid cross-tabulation and aggregation without formulas", "Dynamic drill-down and grouping (dates into months/quarters)", "Shows distribution, totals, and outliers in initial EDA"],
        "cm": ["Creating Pivot Tables on uncleaned raw data containing mixed types or blank header rows", "Forgetting to refresh Pivot Tables after underlying data source changes", "Overcomplicating layouts with 10 stacked row hierarchies"],
        "fu": ["What is the difference between 'Show Values As' (e.g., % of Grand Total) and basic aggregations?", "How does Power Pivot extend traditional Pivot Tables using the Data Model and DAX?"],
        "tags": ["excel", "pivot-tables", "eda", "data-analytics"]
    },
    {
        "q": "Explain the difference between a Star Schema and a Snowflake Schema in data warehousing.",
        "sub": "Data Warehousing",
        "d": "Intermediate",
        "ans": "Both are multi-dimensional modeling schemas centered around Fact tables (containing quantitative numeric metrics/foreign keys) and Dimension tables (containing descriptive textual attributes). 1) Star Schema: dimension tables are intentionally denormalized and connect directly to the central Fact table, forming a star shape. Benefits: simpler queries, fewer table joins, and superior read performance in BI tools like Power BI. 2) Snowflake Schema: dimension tables are further normalized into sub-dimension tables (e.g., Product -> Subcategory -> Category). Benefits: reduced data redundancy and smaller storage. Star Schema is universally preferred in modern BI and analytical reporting due to join simplicity and fast query execution.",
        "kp": ["Fact tables store numerical metrics (revenue, quantity) and dimension foreign keys", "Dimension tables store descriptive context (customers, dates, products)", "Star Schema: denormalized dimensions; fewer joins; optimal for BI performance", "Snowflake Schema: normalized dimensions; reduces storage; requires more joins"],
        "cm": ["Putting descriptive categorical text attributes inside fact tables", "Over-normalizing dimensional models into complex snowflakes that slow down Power BI", "Confusing OLTP operational schemas with OLAP dimensional models"],
        "fu": ["Why do columnar databases (ClickHouse, BigQuery, Snowflake) excel at querying Star Schemas?", "What is a Slowly Changing Dimension (SCD Type 2) and how does it preserve historical changes?"],
        "tags": ["data-warehouse", "star-schema", "snowflake-schema", "power-bi", "olap"]
    },
    {
        "q": "In Power BI, what is the core difference between a Calculated Column and a DAX Measure?",
        "sub": "Power BI & DAX",
        "d": "Intermediate",
        "ans": "1) Calculated Column: computed row-by-row during data model refresh using Row Context; the computed values are physically stored in the in-memory VertiPaq database on disk/RAM. It consumes memory proportional to table row count and does NOT respond dynamically to user visual slicers or filters. 2) DAX Measure: computed on-the-fly at query time during visual rendering using Filter Context; it consumes zero storage memory and dynamically recalculates based on user slicers, filters, and matrix rows. Rule of thumb: always create DAX Measures for aggregations and metrics (`Total Sales = SUM(Sales[Amount])`); use Calculated Columns only when values are needed as slicers, rows, or grouping dimensions.",
        "kp": ["Calculated Column: computed row-by-row at refresh, stored in RAM/disk, row context", "DAX Measure: computed dynamically on visual render, consumes no storage, filter context", "Measures respond dynamically to user dashboard slicers and filters", "Use Measures for aggregations; Columns for categorization and slicing"],
        "cm": ["Creating Calculated Columns for aggregations like `Total Profit = SUM(...)`, wasting memory", "Wondering why a Calculated Column doesn't update when slicers change", "Not understanding that measures recalculate based on the current visual's filter context"],
        "fu": ["What is the difference between Row Context and Filter Context in DAX?", "How does the `CALCULATE()` function transition Row Context into Filter Context?"],
        "tags": ["power-bi", "dax", "calculated-columns", "measures", "business-intelligence"]
    },
    {
        "q": "Explain the role of the `CALCULATE()` function in DAX. Why is it considered the most powerful function in Power BI?",
        "sub": "Power BI & DAX",
        "d": "Advanced",
        "ans": "`CALCULATE(Expression, Filter1, Filter2, ...)` is the cornerstone of DAX because it is the ONLY function capable of modifying or overriding the existing Filter Context of a visual calculation. When executed, `CALCULATE`: 1) Evaluates filter arguments and creates a new filter context, 2) Performs context transition (converting an active row context into an equivalent filter context), and 3) Evaluates the expression within this modified context. For instance, `CALCULATE(SUM(Sales[Amount]), Sales[Region] = \"South\")` overrides active slicers on region to compute strictly southern sales, enabling custom KPIs like Year-over-Year growth, percentage of total via `ALL()`, and cumulative metrics.",
        "kp": ["Only DAX function that modifies or overrides Filter Context", "Enables context transition: transforms row context into filter context", "Accepts filter modifiers like `ALL()`, `REMOVEFILTERS()`, `KEEPFILTERS()`, `USERELATIONSHIP()`", "Powers time-intelligence and comparative KPI benchmarks"],
        "cm": ["Using complex nested IF statements instead of modifying filter context via CALCULATE", "Not knowing that calling a measure inside another measure implicitly wraps it in CALCULATE", "Overriding filter contexts unintentionally without `KEEPFILTERS()`"],
        "fu": ["What is Context Transition and how does calling a measure inside `ITERATOR` functions trigger it?", "How does `CALCULATE(..., ALL(Table))` compute percentage of grand total?"],
        "tags": ["power-bi", "dax", "calculate", "filter-context", "analytics"]
    },
    {
        "q": "What is the difference between `SUM()` and `SUMX()` in DAX? What are iterator functions?",
        "sub": "Power BI & DAX",
        "d": "Intermediate",
        "ans": "`SUM()` is a standard aggregation function that operates on a single column reference, summing all values currently visible in the active filter context: `SUM(Sales[Revenue])`. `SUMX(Table, Expression)` is an iterator (X-function) that establishes a Row Context: it iterates through the specified table row-by-row, evaluates the expression for each row, and then sums the resulting row values. For example, calculating total sales when price and quantity reside in separate columns requires an iterator: `SUMX(Sales, Sales[Quantity] * Sales[UnitPrice])`. Calculating `SUM(Qty) * SUM(Price)` produces mathematically incorrect results due to multiplying totals.",
        "kp": ["`SUM(col)` aggregates a single existing column across current filter context", "`SUMX(table, expr)` iterates row-by-row, computes expression, and sums results", "Iterators establish Row Context across table rows", "Essential when computing row-level multiplication (Quantity * UnitPrice) without adding stored columns"],
        "cm": ["Writing `SUM(Sales[Qty] * Sales[Price])` which is invalid syntax in DAX", "Multiplying column sums `SUM(Qty) * SUM(Price)` which yields mathematically incorrect totals", "Using iterator functions across 10-million row tables when a pre-aggregated column is faster"],
        "fu": ["What other iterator functions exist in DAX (AVERAGEX, MINX, MAXX, COUNTX)?", "How does iterating over a small dimension table compare to iterating over a large fact table?"],
        "tags": ["power-bi", "dax", "sum", "sumx", "iterators"]
    },
    {
        "q": "How do you detect and handle outliers in an analytical dataset using Python and statistics?",
        "sub": "Data Cleaning & EDA",
        "d": "Intermediate",
        "ans": "Outliers are data points that deviate significantly from the overall distribution. Common detection methods: 1) Z-Score Method: measures standard deviations from the mean (`Z = (X - mean) / std`). Data points with `|Z| > 3` are flagged as outliers; assumes normal distribution. 2) Interquartile Range (IQR) Method (robust to non-normal distributions): computes `IQR = Q3 - Q1`. Outliers lie outside `[Q1 - 1.5*IQR, Q3 + 1.5*IQR]`. Handling options: a) Removal (if outliers stem from measurement or data entry errors), b) Winsorization/Capping (replacing extreme values with 1st and 99th percentiles), c) Transformation (log or Box-Cox transformations to compress skewness), or d) Segregation (analyzing outliers as a distinct business segment like fraud or whale spenders).",
        "kp": ["IQR Method: `Q1 - 1.5*IQR` to `Q3 + 1.5*IQR` (non-parametric, robust to skewness)", "Z-score Method: `|Z| > 3` (assumes normal distribution)", "Handling strategies: delete (if erroneous), cap/winsorize, log-transform, or analyze separately", "Never delete outliers automatically without investigating business cause"],
        "cm": ["Deleting outliers blindly without understanding if they represent genuine high-value events", "Using Z-score on heavily skewed or bimodal distributions where mean/std are distorted", "Leaving severe outliers in linear regression models, pulling regression slopes wildly"],
        "fu": ["How do boxplots visually communicate the IQR outlier boundaries?", "Why is the median and IQR preferred over mean and standard deviation for skewed distributions?"],
        "tags": ["data-cleaning", "eda", "outliers", "iqr", "statistics"]
    },
    {
        "q": "How do you handle missing values in data analytics? What are the mechanisms of missing data (MCAR, MAR, MNAR)?",
        "sub": "Data Cleaning & Statistics",
        "d": "Intermediate",
        "ans": "Missing data mechanisms determine the valid imputation strategy: 1) MCAR (Missing Completely at Random): missingness is entirely independent of observed and unobserved data; safe to drop (listwise deletion) without statistical bias. 2) MAR (Missing at Random): missingness depends on other observed variables (e.g., younger users omitting salary, but age is known); can be imputed using predictive models or grouped statistics. 3) MNAR (Missing Not at Random): missingness depends on the unobserved value itself (e.g., people with high debt refusing to report debt); dropping or simple imputation introduces severe bias. Imputation strategies: median for skewed numeric data, mode for categorical data, KNN/MICE for complex relationships, or adding an indicator flag `is_missing`.",
        "kp": ["MCAR: completely random; safe for listwise deletion", "MAR: depends on observed variables; impute with grouped stats or regression", "MNAR: depends on the missing value itself; requires domain modeling", "Imputation techniques: median/mode, KNN, forward-fill for time-series, indicator flags"],
        "cm": ["Replacing missing values with 0 blindly, skewing means and variance calculations", "Dropping all rows with missing values, shrinking dataset size and introducing bias", "Imputing test dataset using test dataset statistics (data leakage)"],
        "fu": ["What is MICE (Multivariate Imputation by Chained Equations)?", "Why is median imputation preferred over mean imputation for skewed variables like income?"],
        "tags": ["data-cleaning", "missing-data", "mcar", "imputation", "statistics"]
    },
    {
        "q": "Explain Customer Churn Rate and Retention Rate. How are they calculated and why are they critical business metrics?",
        "sub": "Business Metrics",
        "d": "Beginner",
        "ans": "1) Churn Rate: the percentage of customers or subscribers who cancel or discontinue their relationship over a given period: `Churn Rate = (Customers Lost during Period) / (Customers at Start of Period) * 100`. 2) Retention Rate: the percentage of existing customers who remain active over the period: `Retention Rate = ((Customers at End of Period - New Customers Acquired) / Customers at Start of Period) * 100`. Churn and Retention are inversely related (`Retention ≈ 100% - Churn`). They are critical because acquiring a new customer costs 5 to 7 times more than retaining an existing one. High churn creates a 'leaky bucket' where growth is unsustainable, directly impairing Customer Lifetime Value (LTV).",
        "kp": ["Churn Rate: percentage of starting customers lost during a time window", "Retention Rate: percentage of starting customers retained, excluding new signups", "Acquisition cost is significantly higher than retention cost", "High churn severely damages LTV and indicates product-market fit issues"],
        "cm": ["Including newly acquired customers in the numerator when calculating retention rate", "Calculating churn across different time intervals (daily vs annual) without standardizing", "Failing to distinguish between customer churn (logos) and revenue churn (MRR/ARR)"],
        "fu": ["What is Net Revenue Retention (NRR) and how can it exceed 100% through expansion?", "What is cohort retention analysis and how does a heatmap visualize it?"],
        "tags": ["business-metrics", "churn-rate", "retention-rate", "saas", "kpi"]
    },
    {
        "q": "What is Customer Lifetime Value (LTV) and Customer Acquisition Cost (CAC)? What is an ideal LTV:CAC ratio?",
        "sub": "Business Metrics",
        "d": "Intermediate",
        "ans": "1) Customer Acquisition Cost (CAC): the total sales and marketing spend divided by the number of new customers acquired during that period: `CAC = Total S&M Expenses / New Customers Acquired`. 2) Customer Lifetime Value (LTV): the total net revenue a customer is projected to generate over their entire relationship with the company: `LTV = (Average Revenue Per User * Gross Margin %) / Churn Rate`. 3) LTV:CAC Ratio: measures marketing efficiency and business model sustainability. An ideal benchmark for healthy SaaS/growth companies is 3:1 (a customer generates 3x what it cost to acquire them). A ratio < 1:1 means the company loses money on every customer; a ratio > 5:1 indicates under-investing in marketing and leaving growth on the table.",
        "kp": ["CAC = Total Sales & Marketing Spend / New Customers Acquired", "LTV = (ARPU * Gross Margin %) / Churn Rate", "LTV:CAC Ratio benchmark: 3:1 is healthy and sustainable", "Ratio < 1:1 implies unsustainable burn; > 5:1 implies under-investing in acquisition"],
        "cm": ["Calculating LTV on gross revenue without accounting for gross margin %", "Omitting marketing salaries and software tooling costs when computing CAC", "Assuming churn rate remains constant indefinitely"],
        "fu": ["What is CAC Payback Period and what is a healthy target for enterprise software?", "How does reducing churn by 5% dramatically boost LTV?"],
        "tags": ["business-metrics", "ltv", "cac", "unit-economics", "saas"]
    },
    {
        "q": "Explain Monthly Recurring Revenue (MRR) and Annual Recurring Revenue (ARR). What components drive MRR changes?",
        "sub": "Business Metrics",
        "d": "Beginner",
        "ans": "Monthly Recurring Revenue (MRR) is the predictable, normalized revenue a subscription-based business earns each month: `MRR = Active Subscribers * Average Monthly Subscription Fee`. Annual Recurring Revenue (ARR) is `MRR * 12`. Net New MRR tracks business growth and has four core components: 1) New MRR: revenue from brand new customers acquired this month. 2) Expansion MRR (Upsell): additional revenue from existing customers upgrading tiers or adding seats. 3) Contraction MRR (Downgrade): lost revenue from existing customers downgrading plans. 4) Churned MRR: lost revenue from customers who canceled subscriptions entirely. Formula: `Net New MRR = New MRR + Expansion MRR - Contraction MRR - Churned MRR`.",
        "kp": ["MRR: predictable normalized monthly subscription revenue; ARR = MRR * 12", "Net New MRR = New + Expansion - Contraction - Churn", "Expansion MRR measures net revenue expansion from existing accounts", "Excludes one-time setup fees, professional services, and non-recurring transactions"],
        "cm": ["Including one-time payments or variable consulting fees in MRR", "Counting bookings or contract commitments as recognized MRR before service delivery", "Ignoring contraction MRR when evaluating growth health"],
        "fu": ["What is the difference between recognized revenue (GAAP) and MRR?", "Why do investors scrutinize Expansion MRR as a signal of product stickiness?"],
        "tags": ["business-metrics", "mrr", "arr", "saas", "subscription-analytics"]
    },
    {
        "q": "What is Average Revenue Per User (ARPU) and how is it used across telecom, SaaS, and e-commerce?",
        "sub": "Business Metrics",
        "d": "Beginner",
        "ans": "Average Revenue Per User (ARPU) measures the average revenue generated per active user or subscriber over a specified period (typically monthly or annually): `ARPU = Total Revenue / Total Active Users`. It measures customer monetization depth. In Indian telecom (e.g., Jio, Airtel), ARPU is the primary competitive KPI, reflecting mobile tariff increases. In SaaS, it is called ARPA (Average Revenue Per Account) and tracks pricing tier expansion. In e-commerce, it connects to Average Order Value (AOV) and purchase frequency (`ARPU = AOV * Purchases per User`). Increasing ARPU allows companies to grow top-line revenue without necessarily adding new users.",
        "kp": ["Formula: Total Revenue / Total Active Users over period", "Measures monetization depth and customer account value", "Key metric in Indian telecom, SaaS, and consumer tech", "Growth lever: upsells, cross-sells, premium tiers, and price optimizations"],
        "cm": ["Calculating ARPU across total registered accounts instead of active paying users", "Mixing monthly revenue with quarterly user counts, skewing results", "Ignoring customer segmentation: a blended ARPU can hide high-value enterprise accounts"],
        "fu": ["What is the difference between ARPU (all users) and ARPPU (Average Revenue Per Paying User) in freemium apps?", "How does cohort segmentation reveal if newer cohorts have higher ARPU than older cohorts?"],
        "tags": ["business-metrics", "arpu", "kpi", "monetization", "telecom"]
    },
    {
        "q": "What are the core principles of effective dashboard design and visual hierarchy in Business Intelligence?",
        "sub": "Dashboard Design",
        "d": "Intermediate",
        "ans": "Effective dashboard design ensures stakeholders understand key business insights within 5 seconds without cognitive overload: 1) Visual Hierarchy (inverted pyramid): high-level summary KPIs (Single Value Cards) placed at the top, followed by trends and distributions in the middle (line charts, bar charts), and granular detail tables at the bottom. 2) Purposeful Color: use color intentionally to signal status (green = good, red = alert) or group categories; avoid decorative rainbow palettes. 3) Chart-to-Data Matching: use line charts for continuous time-series, horizontal bars for categorical comparisons, and avoid 3D charts or pie charts with > 5 slices. 4) Context & Benchmarks: always display targets, period-over-period deltas, or benchmark comparisons alongside numbers (e.g., '$1.2M (+12% vs budget)').",
        "kp": ["Inverted pyramid visual hierarchy: Top KPIs -> Trends -> Detailed Tables", "Intentional semantic color usage; avoid unnecessary rainbow clutter", "Match chart types to data relationships (lines for trends, bars for comparison)", "Always provide contextual comparisons (vs target, vs previous period)"],
        "cm": ["Cluttering the dashboard with 25 unorganized visual widgets", "Using pie charts with 15 thin slices that cannot be compared visually", "Displaying raw metric numbers with zero context or historical trends"],
        "fu": ["What is the '5-second rule' in executive dashboard usability testing?", "When is a simple clean table superior to a graphical chart?"]
    },
    {
        "q": "How do you present data findings and technical insights to non-technical business executives?",
        "sub": "Data Storytelling",
        "d": "Beginner",
        "ans": "Business executives care about decisions, risks, revenue impact, and actionable recommendations—not SQL queries, p-values, or algorithms. Present using the 'Bottom Line Up Front' (BLUF) or Minto Pyramid Principle: 1) Start with the primary takeaway and business recommendation in plain language, 2) Present the supporting data insights, key metrics, and financial implications, and 3) Keep technical methodology, data cleaning caveats, and statistical confidence intervals in an appendix for questions. Focus on: 'What happened? Why does it matter to the business? What action should we take next?'",
        "kp": ["Bottom Line Up Front (BLUF): lead with recommendation and financial impact", "Answer: 'So what?' and 'What should we do next?'", "Translate statistical terms into commercial outcomes (revenue, cost, time saved)", "Relegate technical methodology and raw SQL queries to appendix slides"],
        "cm": ["Opening presentations with 10 slides on data cleaning and SQL joins", "Using statistical jargon (p-value, R-squared) without explaining business meaning", "Presenting data without a clear, actionable recommendation"],
        "fu": ["How do you handle an executive who challenges the validity of your data sources?", "How do you communicate uncertainty or margin of error without undermining credibility?"]
    },
    {
        "q": "Explain the difference between Correlation and Causation in data analytics with a real-world example.",
        "sub": "Statistical Analytics",
        "d": "Beginner",
        "ans": "Correlation measures a statistical association between two variables—when one changes, the other tends to change in a predictable direction (e.g., Pearson's r between -1 and +1). Causation means that a change in variable A directly produces or causes the change in variable B. 'Correlation does not imply causation' because: 1) Confounding variables (a third variable causes both; e.g., ice cream sales and drowning rates both correlate strongly because warm summer weather causes both), 2) Reverse causality (B causes A rather than A causing B), or 3) Pure coincidence / spurious correlation. To establish true causation, analysts must conduct controlled A/B testing (randomized controlled trials) or use quasi-experimental methods like Difference-in-Differences.",
        "kp": ["Correlation: mathematical association/co-movement between variables", "Causation: change in one variable directly produces change in another", "Confounding variable: unseen third factor causing both observed variables", "Causation established through Randomized Controlled Trials (A/B testing) or quasi-experiments"],
        "cm": ["Assuming an A/B test is unnecessary because historical observational data shows strong correlation", "Recommending expensive product changes based on spurious correlations", "Confusing correlation coefficient r with causal effect size"],
        "fu": ["What is an A/B test and how does random assignment eliminate confounders?", "What is Simpson's Paradox and how can a trend reverse when data is aggregated?"]
    },
    {
        "q": "What is an A/B test (split test) in product analytics? What are p-values, statistical power, and sample size?",
        "sub": "Product Analytics & A/B Testing",
        "d": "Intermediate",
        "ans": "An A/B test is a randomized experiment where users are split between a control variant (A) and a treatment variant (B) to determine if a change produces a statistically significant improvement in a target metric (conversion rate, click-through rate). Key concepts: 1) Null Hypothesis (H0): assumes no difference between variants. 2) p-value: the probability of observing results as extreme as the actual test data assuming the null hypothesis is true; a p-value < 0.05 indicates statistical significance. 3) Statistical Power (typically 80%): the probability of detecting a real effect if one exists (avoiding Type II False Negatives). 4) Minimum Detectable Effect (MDE) and sample size calculations determine how many users must run through the test before drawing conclusions.",
        "kp": ["Randomized controlled experiment comparing control vs treatment", "p-value < 0.05 indicates observed difference is unlikely due to random chance", "Statistical power (80%) guards against Type II False Negatives", "Pre-calculate sample size based on baseline conversion, MDE, and power"],
        "cm": ["Peeking at test results daily and stopping the test early as soon as p < 0.05 (causes severe false positives)", "Running A/B tests with insufficient sample size, resulting in underpowered tests", "Changing test parameters or traffic allocations midway through an active experiment"],
        "fu": ["What is the 'Peeking Problem' in A/B testing and how does sequential testing mitigate it?", "What is the difference between a Type I error (False Positive) and a Type II error (False Negative)?"]
    },
    {
        "q": "What is cohort analysis in data analytics, and how do you construct a customer retention cohort heatmap?",
        "sub": "Cohort Analytics",
        "d": "Intermediate",
        "ans": "Cohort analysis groups users who share a common characteristic or event within a defined time frame (typically signup month or first purchase date) and tracks their behavior over time. A retention cohort heatmap plots cohort acquisition periods along the vertical axis (e.g., Jan 2024, Feb 2024) and elapsed time periods along the horizontal axis (Month 0, Month 1, Month 2...). Each cell displays the percentage of that cohort remaining active. This decouples user growth from retention quality, revealing whether product improvements are increasing long-term stickiness for newer cohorts or whether older cohorts decay rapidly.",
        "kp": ["Groups users by shared starting event and time window (e.g., Jan signup cohort)", "Tracks behavioral metric (retention, spend) across successive time periods (M0, M1, M2)", "Visualized via triangular cohort retention heatmaps", "Isolates product improvements from seasonal acquisition spikes"],
        "cm": ["Looking only at aggregate monthly active users (MAU), which masks deteriorating cohort retention", "Comparing cohorts of different ages without normalizing by elapsed months", "Confusing acquisition cohorts with behavioral cohorts (e.g., users who used a specific feature)"],
        "fu": ["What does a 'flattening' retention curve signify regarding Product-Market Fit?", "How do you write a SQL query to generate a monthly retention cohort matrix?"]
    },
    {
        "q": "Explain Funnel Analysis in product analytics. How do you identify drop-off points and conversion bottlenecks?",
        "sub": "Product Analytics",
        "d": "Beginner",
        "ans": "Funnel analysis tracks the progression of users through a predefined, sequential series of steps toward a conversion goal (e.g., Landing Page -> Product View -> Add to Cart -> Checkout -> Payment Success). At each step, the analysis measures conversion rate and drop-off rate (`Drop-off % = (Users at Step N - Users at Step N+1) / Users at Step N * 100`). Identifying the step with the highest drop-off rate directs engineering and design focus to the exact bottleneck—such as complicated checkout forms, unexpected shipping costs, or slow page load times. Segmenting funnels by device (mobile vs desktop) or acquisition channel reveals targeted usability issues.",
        "kp": ["Maps sequential user steps toward a conversion milestone", "Measures step-by-step conversion and drop-off percentages", "Pinpoints exact stages causing highest friction and user abandonment", "Segment funnels by device, browser, and traffic source to isolate issues"],
        "cm": ["Assuming the largest numerical drop-off is the easiest or highest-priority step to fix", "Not checking if users can take alternative paths that bypass formal funnel steps", "Ignoring technical performance (page load latency) at high-drop-off steps"],
        "fu": ["What is the difference between an open funnel and a closed funnel?", "How do session recording tools (Hotjar) complement quantitative funnel analytics?"]
    },
    {
        "q": "What is Simpson's Paradox in statistics and data analytics? Provide a classic business example.",
        "sub": "Statistical Analytics",
        "d": "Intermediate",
        "ans": "Simpson's Paradox is a statistical phenomenon where a trend or relationship that appears across several individual sub-groups disappears or reverses when the groups are aggregated together. It occurs when a confounding lurking variable creates disproportionate group sample sizes. Classic example: an e-commerce company tests a new checkout page. Across mobile users, Variant B has higher conversion (15% vs 10%). Across desktop users, Variant B also wins (30% vs 25%). Yet when combined into overall totals, Variant A appears to have higher conversion overall because Variant A had 90% desktop traffic (higher baseline) while Variant B had 90% mobile traffic. Always segment aggregated data to detect confounding variables.",
        "kp": ["Aggregated data trend reverses when broken down into sub-groups", "Caused by confounding variables and unequal subgroup sample distributions", "Warns against drawing business decisions solely from high-level blended averages", "Always slice aggregate metrics across key dimensions (device, geography, tier)"],
        "cm": ["Making executive decisions on blended averages without segmenting key dimensions", "Assuming higher overall averages guarantee performance superiority in sub-segments", "Ignoring unequal traffic distribution across test variants"],
        "fu": ["How did the famous 1973 UC Berkeley gender admissions study demonstrate Simpson's Paradox?", "How does stratified sampling prevent Simpson's Paradox during experimental design?"]
    },
    {
        "q": "What is the difference between OLTP (Online Transaction Processing) and OLAP (Online Analytical Processing)?",
        "sub": "Database Architectures",
        "d": "Beginner",
        "ans": "1) OLTP (Online Transaction Processing): optimized for high-concurrency, low-latency, real-time read/write transactions affecting single or small sets of rows (e.g., banking transactions, e-commerce orders). Characterized by normalized (3NF) relational tables, row-oriented storage (PostgreSQL, MySQL), frequent INSERT/UPDATE/DELETE, and strict ACID guarantees. 2) OLAP (Online Analytical Processing): optimized for complex, read-heavy analytical queries scanning millions of historical rows for aggregations (e.g., quarterly sales trends, customer segmentation). Characterized by denormalized star schemas, columnar storage (Snowflake, BigQuery, ClickHouse), batch ETL/ELT loading, and fast aggregations over subsets of columns.",
        "kp": ["OLTP: operational systems, high concurrent writes, normalized row-oriented storage, ACID", "OLAP: analytical systems, read-heavy complex aggregations, columnar storage, Star schema", "OLTP updates individual rows; OLAP scans millions of rows across few columns", "Separated via ETL/ELT pipelines to prevent analytical queries from locking transactional databases"],
        "cm": ["Running heavy analytical multi-table aggregation reports directly on the primary OLTP production database", "Using an OLAP columnar database for row-by-row transactional web application backends", "Confusing row-oriented storage with columnar storage performance characteristics"],
        "fu": ["Why does columnar storage provide 10x-100x compression and faster aggregations for OLAP queries?", "What is an ELT pipeline (Extract, Load, Transform) and how does it leverage modern cloud data warehouses?"]
    },
    {
        "q": "Explain the difference between ETL (Extract, Transform, Load) and ELT (Extract, Load, Transform) data pipelines.",
        "sub": "Data Engineering",
        "d": "Beginner",
        "ans": "1) ETL (Extract, Transform, Load): raw data is extracted from source operational databases, transformed in a specialized external staging engine (cleaning, aggregation, anonymization), and loaded into the destination warehouse. Historically used when storage was expensive and on-premise warehouses lacked processing power. 2) ELT (Extract, Load, Transform): raw data is extracted and loaded immediately into the cloud data warehouse (Snowflake, BigQuery, Databricks) in its raw state; transformations are executed directly inside the warehouse using SQL tools like dbt. ELT is the modern standard because cloud storage is cheap and cloud warehouses possess massive parallel processing (MPP) compute power, preserving raw data for future re-transformation.",
        "kp": ["ETL: transforms data on a separate compute server before loading; historic pattern", "ELT: loads raw data directly into cloud warehouse; transforms using warehouse MPP compute", "ELT preserves raw data lineage, enabling re-transformation without re-extracting", "Modern ELT stack: Fivetran/Airbyte (Extract/Load) + dbt (Transform) + Snowflake/BigQuery"],
        "cm": ["Discarding raw data permanently during ETL transformations without backup", "Running heavy transformations on source OLTP production databases", "Assuming ETL is obsolete for privacy-sensitive data where PII must be masked before leaving networks"],
        "fu": ["When is ETL still preferred over ELT (e.g., HIPAA compliance, PII masking)?", "What is dbt (data build tool) and how does it bring software engineering practices to SQL transformations?"]
    },
    {
        "q": "What is data lineage and why is it essential for analytical governance and debugging?",
        "sub": "Data Governance",
        "d": "Intermediate",
        "ans": "Data lineage traces the complete lifecycle of data: where it originated (source database, API, tracking event), what transformations and business logic were applied across ETL/ELT pipelines, and where it is consumed downstream (dashboards, ML models, executive reports). Lineage is essential for: 1) Root-Cause Debugging: when a dashboard metric looks corrupted, lineage traces upstream to identify the exact failed job or schema change that caused it. 2) Impact Analysis: before modifying an upstream table column, lineage identifies every downstream dashboard or report that will break. 3) Regulatory Compliance: auditing data privacy (GDPR/CCPA) and financial reporting accuracy.",
        "kp": ["Traces data journey from source origin through transformations to consumption", "Enables rapid root-cause analysis when dashboard numbers break", "Provides impact analysis prior to upstream database schema modifications", "Essential for data governance, quality audits, and regulatory compliance"],
        "cm": ["Modifying upstream table columns without checking downstream report dependencies", "Relying on tribal knowledge instead of automated lineage graphing tools (dbt Docs, Monte Carlo)", "Ignoring data lineage until an executive report displays incorrect revenue numbers"],
        "fu": ["How does dbt automatically generate directed acyclic graphs (DAGs) representing data lineage?", "What is data observability and how does it monitor data freshness and schema drift?"]
    },
    {
        "q": "How do you handle currency conversions and time-zone conversions in global analytical datasets?",
        "sub": "Data Engineering & Analytics",
        "d": "Intermediate",
        "ans": "1) Time-Zones: best practice is to convert all timestamps to UTC at the ingestion boundary and store them with timezone awareness (`TIMESTAMP WITH TIME ZONE`). Local business day aggregations convert UTC to the user's or store's local timezone (e.g., using `AT TIME ZONE 'Asia/Kolkata'`) before grouping, preventing transactions near midnight from shifting into the wrong calendar date. 2) Currency Conversion: daily foreign exchange rates should be maintained in a dedicated rate table. Historical transactions should be converted using the exchange rate on the exact transaction date, rather than a single current exchange rate. Both original local currency and standardized reporting currency (e.g., USD or INR) should be retained in the fact table.",
        "kp": ["Store all database timestamps in UTC with timezone awareness", "Convert UTC to local timezone before performing date-based aggregations", "Use historical exchange rates matching transaction dates, not current spot rates", "Preserve both original local currency and standardized reporting currency columns"],
        "cm": ["Grouping by UTC dates directly, shifting Asian or Pacific midnight transactions into the wrong local business day", "Converting historical multi-year sales using today's exchange rate, distorting growth numbers", "Storing timestamps as ambiguous local strings without timezone offsets"],
        "fu": ["How does Daylight Saving Time (DST) create non-existent or duplicate hours in local timestamp analytics?", "What is purchasing power parity (PPP) and when is it useful for cross-country pricing analysis?"]
    },
    {
        "q": "What is exploratory data analysis (EDA) and what sequential steps do you take when exploring a new dataset?",
        "sub": "Exploratory Data Analysis",
        "d": "Beginner",
        "ans": "Exploratory Data Analysis (EDA) is the disciplined process of investigating a new dataset to understand its structure, distributions, anomalies, and relationships before formal modeling: 1) Structural Overview: inspect row/column counts, data types, and sample records (`df.info()`, `df.head()`). 2) Data Quality Audit: check missing value percentages per column, duplicate rows, and invalid data formats. 3) Univariate Analysis: examine summary statistics (`df.describe()`), central tendencies, skewness, and frequency histograms for numeric data; value counts for categorical data. 4) Bivariate Analysis: inspect correlations between numerical features (correlation heatmaps) and relationships with the target variable (scatter plots, grouped boxplots). 5) Hypothesis Generation: formulate clear business questions based on findings.",
        "kp": ["Step 1: Structure and schema audit (`df.info()`)", "Step 2: Missing data and duplicate detection", "Step 3: Univariate analysis (distributions, skewness, central tendencies)", "Step 4: Bivariate analysis (correlations, scatter plots, grouped cross-tabs)", "Step 5: Synthesize business hypotheses and data cleaning requirements"],
        "cm": ["Jumping directly into training ML models or building dashboards without checking data quality", "Relying on correlation alone without visualizing distributions and scatter plots", "Ignoring data types (e.g., dates loaded as text strings or zip codes as numeric integers)"],
        "fu": ["What is Anscombe's Quartet and why does it prove the necessity of visualizing data beyond summary statistics?", "How do automated profiling tools like YData Profiling accelerate initial EDA?"]
    },
    {
        "q": "What are the common chart selection rules for visualizing comparisons, compositions, distributions, and relationships?",
        "sub": "Data Visualization",
        "d": "Beginner",
        "ans": "Matching chart type to data relationship is essential for clear communication: 1) Comparison across categories: Horizontal Bar Chart (superior when category names are long) or Vertical Column Chart. 2) Trend over time: Line Chart (continuous time) or Area Chart. 3) Distribution of a single numeric variable: Histogram (frequency bins) or Boxplot (median, quartiles, outliers). 4) Relationship between two continuous variables: Scatter Plot (shows correlation, clusters, non-linear patterns). 5) Composition / Parts of a whole: 100% Stacked Bar Chart or Waterfall Chart; limit Pie/Donut charts strictly to 2-4 distinct slices. Avoid 3D charts, dual-axis charts with deceptive scaling, and radial radar charts with > 6 axes.",
        "kp": ["Comparisons: Bar/Column charts (horizontal for long text labels)", "Trends over time: Line charts", "Distributions: Histograms and Boxplots", "Relationships: Scatter plots", "Composition: 100% Stacked Bar or Waterfall charts; minimize pie charts"],
        "cm": ["Using pie charts with 15 slices where slices cannot be compared accurately", "Using line charts for discrete categorical data that has no temporal continuity", "Truncating bar chart Y-axes to start at non-zero values, visually exaggerating minor differences"],
        "fu": ["Why must bar charts always start at a zero baseline, whereas line charts can have broken Y-axes?", "How does a Waterfall chart visualize positive and negative contributions to a net total?"]
    }
]

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    f1 = OUT_DIR / "01.json"
    f2 = OUT_DIR / "02.json"
    f1.write_text(json.dumps(PART1, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    f2.write_text(json.dumps(PART2, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(PART1)} to 01.json, {len(PART2)} to 02.json (Total: {len(PART1) + len(PART2)})")

if __name__ == "__main__":
    main()
