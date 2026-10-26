"""Seed Custom Curated Questions requested by the user:
1. DBMS & SQL + Web/Networking questions
2. Top 30 Coding Questions (Arrays, Strings, Basic Algorithms)
3. Operating Systems (OS) Questions (Processes, Threads, Deadlocks, Scheduling, Memory)
"""

import logging
from sqlalchemy import select
from app.db.session import SessionLocal
from app.models.question import Question, question_fingerprint
from app.models.enums import QuestionCategory, Difficulty, QuestionType

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("seed_custom_curated")

CURATED_QUESTIONS = [
    # =========================================================================
    # 1. DBMS & SQL (+ NETWORKING / WEB BASICS FROM LIST)
    # =========================================================================
    {
        "q": "What is normalization? Why is it needed in relational databases?",
        "cat": "SQL & Analytics", "sub": "Database Normalization", "d": "Intermediate", "type": "technical",
        "roles": ["Software Development Engineer", "Backend Developer", "Data Analyst"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Normalization is the systematic technique of organizing tables and attributes in a relational database to minimize data redundancy and prevent data anomalies (insertion, update, and deletion anomalies).\n\nWhy It Is Needed:\n1) Eliminates Data Redundancy: Prevents identical data (e.g., student department name) from being stored redundantly across thousands of student rows, reducing storage footprint.\n2) Prevents Insertion Anomaly: You cannot insert a department without an enrolled student unless nullable columns are permitted.\n3) Prevents Update Anomaly: Modifying a department head's name requires updating thousands of rows; missing one creates inconsistent states.\n4) Prevents Deletion Anomaly: Deleting the last student in a department unintentionally wipes out the department's record entirely.\n\nNormal Forms Summary:\n- 1NF: Atomic (indivisible) column values, unique row identifier (primary key), no repeating groups.\n- 2NF: Meets 1NF + eliminates Partial Dependencies (every non-key attribute depends on the full composite primary key).\n- 3NF: Meets 2NF + eliminates Transitive Dependencies (non-key attributes depend solely on the primary key: 'the key, the whole key, and nothing but the key').\n- BCNF: Stricter 3NF where every determinant must be a candidate key.",
        "kp": [
            "Organizes schemas to minimize redundancy and prevent insert/update/delete anomalies",
            "1NF: Atomic values and primary key; no repeating groups",
            "2NF: Eliminates partial dependencies on composite keys",
            "3NF: Eliminates transitive dependencies (A -> B -> C)"
        ],
        "crit": ["Systematic breakdown of 1NF, 2NF, 3NF with clear rationale", "Accurate explanation of the 3 anomaly types"],
        "cm": ["Assuming normalization improves query read speed (it often slows reads due to extra joins)", "Confusing 2NF with 3NF definitions"],
        "fu": ["When would you intentionally denormalize a database?", "What is Boyce-Codd Normal Form (BCNF)?"],
        "tags": ["master-bank", "sql", "dbms", "normalization", "top-30"]
    },
    {
        "q": "Explain ACID properties in database management with a real-world example.",
        "cat": "SQL & Analytics", "sub": "Transaction Management", "d": "Intermediate", "type": "technical",
        "roles": ["Software Development Engineer", "Backend Developer", "Data Analyst"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "ACID properties ensure reliable execution of database transactions in concurrent environments:\n\n1) Atomicity ('All-or-Nothing'): The transaction is treated as a single indivisible unit. If any part fails, all prior operations roll back completely.\nExample: Transferring $100 from Account A to B involves (1) debiting A and (2) crediting B. If the server crashes after debiting A, Atomicity ensures the $100 is refunded to A.\n\n2) Consistency: The database moves from one valid state to another, strictly satisfying all schema rules, constraints, primary/foreign keys, and cascade triggers.\nExample: An account balance cannot drop below zero if `CHECK (balance >= 0)` is defined.\n\n3) Isolation: Concurrently executing transactions cannot see or interfere with each other's intermediate uncommitted modifications. Controlled via transaction isolation levels (Read Uncommitted, Read Committed, Repeatable Read, Serializable).\nExample: If User 1 and User 2 purchase the last airline ticket at the exact same millisecond, Isolation ensures only one transaction commits.\n\n4) Durability: Once a transaction is committed, its changes are permanently recorded in non-volatile storage (via Write-Ahead Logging / WAL) and survive system crashes or power failures.",
        "kp": [
            "Atomicity: all-or-nothing execution with automatic rollback on error",
            "Consistency: preserves constraints, foreign keys, and invariants",
            "Isolation: concurrent transactions execute without cross-contamination",
            "Durability: committed data survives reboots and power outages via WAL"
        ],
        "crit": ["Clear, accurate definitions with a concrete banking transfer example", "Understanding transaction log mechanisms (WAL)"],
        "cm": ["Confusing Consistency in ACID with Consistency in CAP theorem", "Vague answers lacking concrete transactional examples"],
        "fu": ["What are dirty reads, non-repeatable reads, and phantom reads?", "How do relational databases implement isolation via MVCC?"],
        "tags": ["master-bank", "sql", "dbms", "acid", "transactions", "top-30"]
    },
    {
        "q": "What is the difference between DELETE, TRUNCATE, and DROP in SQL?",
        "cat": "SQL & Analytics", "sub": "DDL vs DML Commands", "d": "Beginner", "type": "technical",
        "roles": ["Software Development Engineer", "Backend Developer", "Data Analyst"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Comparison across Category, Operation, Rollback, and Identity Counters:\n\n1) DELETE (DML - Data Manipulation Language):\n- Operation: Deletes specific rows matching a `WHERE` clause (or all rows if WHERE is omitted).\n- Mechanism: Row-by-row deletion; each deleted row is logged in the transaction log.\n- Rollback: Fully supported within an explicit transaction (`ROLLBACK`).\n- Triggers: Fires DELETE triggers for each deleted row.\n- Identity: Does NOT reset auto-increment / identity counters.\n- Schema: Table schema and structure remain intact.\n\n2) TRUNCATE (DDL - Data Definition Language):\n- Operation: Removes ALL rows from a table rapidly.\n- Mechanism: Deallocates data pages directly rather than logging row deletions, making it much faster on large tables.\n- WHERE clause: Not allowed (`TRUNCATE TABLE tablename`).\n- Rollback: In PostgreSQL/SQL Server, can be rolled back inside an explicit transaction block; in MySQL (MyISAM/older engines), it commits immediately.\n- Triggers: Does NOT fire individual row delete triggers.\n- Identity: Resets auto-increment / identity counters back to seed.\n- Foreign Keys: Fails if referenced by an active Foreign Key constraint.\n\n3) DROP (DDL - Data Definition Language):\n- Operation: Completely destroys the table data, structure, indexes, constraints, and permissions.\n- Catalog: Removes table definition from the database system catalog.\n- Rollback: Generally non-recoverable without database backups.",
        "kp": [
            "DELETE: DML, row-by-row, supports WHERE, fires triggers, retains identity counter",
            "TRUNCATE: DDL, deallocates pages, removes all rows rapidly, resets identity, cannot use WHERE",
            "DROP: DDL, permanently destroys both data and table structure from schema"
        ],
        "crit": ["Accurate comparison across command type, speed, rollback, triggers, and identity reset", "Awareness of foreign key constraints on TRUNCATE"],
        "cm": ["Believing TRUNCATE can accept a WHERE clause", "Thinking TRUNCATE deletes table definition"],
        "fu": ["Why does TRUNCATE fail if a foreign key points to the target table?", "Can TRUNCATE be rolled back inside a transaction in PostgreSQL?"],
        "tags": ["master-bank", "sql", "dbms", "ddl-dml", "truncate-delete", "top-30"]
    },
    {
        "q": "What is the difference between INNER JOIN and LEFT JOIN in SQL?",
        "cat": "SQL & Analytics", "sub": "SQL Joins", "d": "Beginner", "type": "technical",
        "roles": ["Software Development Engineer", "Backend Developer", "Data Analyst"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Both are relational join operations based on matching conditions (`ON A.id = B.id`), but handle unmatched records differently:\n\n1) INNER JOIN:\n- Returns only the rows that have matching values in BOTH tables.\n- If a row in Table A has no corresponding match in Table B, that row is omitted from the output.\n\nExample:\n```sql\nSELECT e.name, d.department_name\nFROM Employees e\nINNER JOIN Departments d ON e.department_id = d.id;\n```\n(Omits employees without departments and departments without employees).\n\n2) LEFT JOIN (or LEFT OUTER JOIN):\n- Returns ALL rows from the left table (Table A), regardless of whether there is a match in Table B.\n- If a matching row exists in Table B, its columns are populated; if no match exists, columns from Table B are populated with `NULL`.\n\nExample:\n```sql\nSELECT e.name, d.department_name\nFROM Employees e\nLEFT JOIN Departments d ON e.department_id = d.id;\n```\n(Returns every employee; employees with unassigned departments display `NULL` for `department_name`).\n\nPractical Use Case for LEFT JOIN: Finding orphans or missing associations (`WHERE d.id IS NULL`).",
        "kp": [
            "INNER JOIN: Intersection only (requires matching keys in both tables)",
            "LEFT JOIN: All rows from left table + matched right rows (NULL for unmatched right rows)",
            "Use LEFT JOIN with `WHERE right.id IS NULL` to find records without matching associations"
        ],
        "crit": ["Clear, accurate distinction with syntax examples", "Correct handling and explanation of NULL values in outer joins"],
        "cm": ["Putting filter conditions on the right table in the WHERE clause of a LEFT JOIN, inadvertently converting it into an INNER JOIN"],
        "fu": ["What is the difference between LEFT JOIN and FULL OUTER JOIN?", "How does CROSS JOIN differ from INNER JOIN?"],
        "tags": ["master-bank", "sql", "joins", "inner-join", "left-join", "top-30"]
    },
    {
        "q": "Write a SQL query to find the second highest salary from an Employee table.",
        "cat": "SQL & Analytics", "sub": "Complex Queries & Window Functions", "d": "Intermediate", "type": "technical",
        "roles": ["Software Development Engineer", "Backend Developer", "Data Analyst"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Multiple standard solutions with varying portability:\n\nApproach 1: Window Function (DENSE_RANK - Recommended for duplicates):\n```sql\nWITH RankedSalaries AS (\n    SELECT salary,\n           DENSE_RANK() OVER (ORDER BY salary DESC) as rank_pos\n    FROM Employee\n)\nSELECT MAX(salary) as SecondHighestSalary\nFROM RankedSalaries\nWHERE rank_pos = 2;\n```\n(Using DENSE_RANK ensures duplicate top salaries like [100k, 100k, 90k] correctly identify 90k as the 2nd highest; MAX handles cases with fewer than 2 distinct salaries by returning NULL).\n\nApproach 2: Subquery with MAX():\n```sql\nSELECT MAX(salary) AS SecondHighestSalary\nFROM Employee\nWHERE salary < (SELECT MAX(salary) FROM Employee);\n```\n(Portable across all SQL dialects; returns NULL if no second highest salary exists).\n\nApproach 3: LIMIT and OFFSET (Dialect-specific e.g. MySQL/PostgreSQL):\n```sql\nSELECT DISTINCT salary AS SecondHighestSalary\nFROM Employee\nORDER BY salary DESC\nLIMIT 1 OFFSET 1;\n```",
        "kp": [
            "Use DISTINCT or DENSE_RANK to handle duplicate salary ties correctly",
            "DENSE_RANK() OVER (ORDER BY salary DESC) assigns identical ranks to duplicate values without skipping numbers",
            "Handle edge cases where table contains fewer than 2 distinct salaries (should return NULL)"
        ],
        "crit": ["Syntactically valid query handling duplicate salaries", "Awareness of edge cases where only 1 distinct salary exists"],
        "cm": ["Using `LIMIT 1 OFFSET 1` without `DISTINCT` (fails if two employees tie for the highest salary)", "Using `RANK()` instead of `DENSE_RANK()` (skips rank 2 if two people tie for rank 1)"],
        "fu": ["How would you generalize this query to find the N-th highest salary?", "What is the time complexity difference between an index scan vs full table scan for this query?"],
        "tags": ["master-bank", "sql", "queries", "second-highest-salary", "window-functions", "top-30"]
    },
    {
        "q": "What is an index in a database? When should you avoid using one?",
        "cat": "SQL & Analytics", "sub": "Performance & Indexing", "d": "Intermediate", "type": "technical",
        "roles": ["Software Development Engineer", "Backend Developer", "Data Analyst"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "An index is a specialized data structure (most commonly a Balanced Tree / B-Tree, or Hash index) created on one or more table columns to rapidly locate and retrieve rows without scanning the entire table (Full Table Scan).\n\nHow It Works:\nSimilar to an index at the back of a textbook. Instead of reading all N pages (O(N)), the database traverses the B-Tree in O(log N) operations to fetch the physical row pointer (TID/RowID).\n\nWhen You Should AVOID Using an Index:\n1) Low Cardinality Columns: Columns with very few distinct values (e.g., `gender`, `is_active`, `status` with 2 values). The query optimizer will ignore the index and prefer a sequential scan.\n2) Small Tables: On tables with only a few hundred rows, reading the entire table directly into memory is faster than tree traversal overhead.\n3) Write-Heavy / High-Ingestion Tables: Every `INSERT`, `UPDATE`, and `DELETE` must rebalance the index B-Tree, adding significant write latency.\n4) Columns Frequently Updated: Updating indexed columns forces index page splits and re-indexing.\n5) Wide / Unused Columns: Storing indexes on large text blobs wastes memory buffer pool space without adding query performance.",
        "kp": [
            "B-Tree index reduces search from O(N) full table scan to O(log N) tree traversal",
            "Speeds up SELECT queries with WHERE, JOIN, and ORDER BY clauses",
            "Avoid on: low-cardinality columns, small tables, and write-heavy workloads due to index maintenance overhead"
        ],
        "crit": ["Clear explanation of B-Tree lookup mechanics", "Specific, practical scenarios where indexing harms system performance"],
        "cm": ["Assuming indexing every single column in a table makes all queries faster", "Ignoring write overhead (INSERT/UPDATE/DELETE performance degradation)"],
        "fu": ["What is the difference between a clustered index and a non-clustered index?", "What is a composite index and what is the leftmost prefix rule?"],
        "tags": ["master-bank", "sql", "indexing", "performance", "btree", "top-30"]
    },
    {
        "q": "What is the difference between TCP and UDP? Give real-world examples of each.",
        "cat": "Networking & IoT", "sub": "Transport Layer Protocols", "d": "Beginner", "type": "technical",
        "roles": ["Software Development Engineer", "Backend Developer", "Full-Stack Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "TCP (Transmission Control Protocol) and UDP (User Datagram Protocol) are transport layer protocols operating at Layer 4 of the OSI model:\n\n1) TCP (Transmission Control Protocol):\n- Connection-Oriented: Establishes a dedicated connection via a 3-Way Handshake (SYN -> SYN-ACK -> ACK) before sending data.\n- Reliability: Guaranteed delivery via acknowledgments (ACK) and automatic retransmissions of lost packets.\n- Ordering: Packets are numbered; received packets are reassembled in strict original order.\n- Flow & Congestion Control: Regulates transmission speed to avoid overwhelming receiver or network buffers.\n- Overhead: Higher latency and larger header (20-60 bytes).\n- Real-World Use Cases: Web browsing (HTTP/HTTPS), Email (SMTP/IMAP), File Transfers (FTP), SSH, Financial transactions.\n\n2) UDP (User Datagram Protocol):\n- Connectionless: Sends datagrams immediately without handshake or connection teardown.\n- Unreliable (Best-Effort Delivery): No acknowledgments, no retransmissions. Lost packets are discarded.\n- No Ordering: Packets may arrive out of order or duplicated.\n- Overhead: Minimal latency, tiny header (8 bytes).\n- Real-World Use Cases: Real-time multiplayer gaming, live video streaming (Twitch/YouTube Live), VoIP (Zoom/WhatsApp voice calls), DNS queries, DHCP.",
        "kp": [
            "TCP: Connection-oriented, reliable, ordered, error-checked, flow-controlled (HTTP, banking, SSH)",
            "UDP: Connectionless, unreliable, low-latency, lightweight, packet loss tolerant (gaming, VoIP, streaming, DNS)",
            "TCP trades latency for reliability; UDP trades reliability for real-time speed"
        ],
        "crit": ["Systematic comparison across connection, reliability, ordering, flow control, and header size", "Accurate real-world application examples for each"],
        "cm": ["Thinking UDP is 'broken' because it is unreliable (UDP is intentionally lightweight for real-time applications)", "Using TCP for live audio/video calls where delayed packets are useless"],
        "fu": ["Why does DNS use UDP for small queries and TCP for zone transfers?", "What is QUIC protocol (HTTP/3) and how does it combine UDP speed with TCP reliability?"],
        "tags": ["master-bank", "networking", "tcp", "udp", "transport-layer", "top-30"]
    },
    {
        "q": "Explain the TCP Three-Way Handshake with a sequence diagram.",
        "cat": "Networking & IoT", "sub": "TCP Protocol Mechanics", "d": "Intermediate", "type": "technical",
        "roles": ["Software Development Engineer", "Backend Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "The TCP Three-Way Handshake is the process used by TCP to establish a reliable, full-duplex connection between client and server, synchronizing initial sequence numbers (ISN):\n\nHandshake Steps:\n1) Step 1: SYN (Synchronize)\n- The client sends a segment with the `SYN` flag set to 1.\n- Specifies an initial client sequence number (e.g., `Seq = X`).\n- State: Client enters `SYN_SENT` state; Server is in `LISTEN` state.\n\n2) Step 2: SYN-ACK (Synchronize-Acknowledgment)\n- The server responds with both `SYN = 1` and `ACK = 1` flags set.\n- Acknowledges the client's sequence: `Ack = X + 1`.\n- Provides its own initial sequence number: `Seq = Y`.\n- State: Server enters `SYN_RCVD` state.\n\n3) Step 3: ACK (Acknowledgment)\n- The client responds with `ACK = 1` flag set.\n- Acknowledges the server's sequence: `Ack = Y + 1`.\n- State: Both client and server enter `ESTABLISHED` state. Data transmission begins.\n\nWhy Three Steps? Two steps would leave the server vulnerable to half-open ghost connections; three steps ensure both sender and receiver have verified that the other can both transmit and receive.",
        "kp": [
            "SYN (Client -> Server, Seq=X) -> SYN-ACK (Server -> Client, Seq=Y, Ack=X+1) -> ACK (Client -> Server, Ack=Y+1)",
            "Synchronizes sequence numbers for full-duplex communication",
            "Transition states: LISTEN -> SYN_SENT / SYN_RCVD -> ESTABLISHED",
            "Prevents half-open connections and stale packet confusion"
        ],
        "crit": ["Accurate sequence numbers and flag descriptions across all 3 steps", "Understanding why a 2-way handshake is insufficient"],
        "cm": ["Confusing the 3-way connection handshake with the 4-way connection termination handshake (FIN/ACK)", "Assuming data payload is sent in Step 1"],
        "fu": ["What is a SYN Flood attack and how do SYN Cookies mitigate it?", "How does TCP terminate a connection (4-Way Handshake with FIN/ACK)?"],
        "tags": ["master-bank", "networking", "tcp", "handshake", "syn-ack", "top-30"]
    },
    {
        "q": "Explain the 7 layers of the OSI Model with their functions and protocols.",
        "cat": "Networking & IoT", "sub": "Network Architecture", "d": "Beginner", "type": "technical",
        "roles": ["Software Development Engineer", "Backend Developer", "Network Engineer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "The OSI (Open Systems Interconnection) reference model standardizes network communication across 7 modular layers (mnemonic bottom-up: 'Please Do Not Throw Sausage Pizza Away'):\n\n1) Physical Layer (Layer 1):\n- Transmits raw unstructured bit streams over physical media (cables, radio waves, optical fiber).\n- Devices: Cables, Hubs, Repeaters. Unit: Bits.\n\n2) Data Link Layer (Layer 2):\n- Node-to-node framing, physical MAC addressing, error detection (CRC).\n- Protocols: Ethernet, Wi-Fi (802.11). Devices: Switches, Bridges. Unit: Frames.\n\n3) Network Layer (Layer 3):\n- Logical IP addressing, routing packets across multiple networks/subnets.\n- Protocols: IPv4, IPv6, ICMP, OSPF, BGP. Devices: Routers. Unit: Packets.\n\n4) Transport Layer (Layer 4):\n- End-to-end host-to-host delivery, port numbers, reliability, flow and congestion control.\n- Protocols: TCP, UDP. Unit: Segments (TCP) / Datagrams (UDP).\n\n5) Session Layer (Layer 5):\n- Manages, establishes, and terminates communication sessions and dialogues between applications.\n- Protocols: NetBIOS, RPC, PPTP.\n\n6) Presentation Layer (Layer 6):\n- Data translation, character encoding (ASCII, UTF-8), compression (GZIP), and encryption/decryption (TLS/SSL).\n\n7) Application Layer (Layer 7):\n- Direct interface for user applications to access network services.\n- Protocols: HTTP, HTTPS, DNS, FTP, SMTP, SSH, WebSocket.",
        "kp": [
            "7 Layers: Physical -> Data Link -> Network -> Transport -> Session -> Presentation -> Application",
            "Data units: Bits -> Frames -> Packets -> Segments -> Data",
            "Switches operate at Layer 2 (MAC); Routers operate at Layer 3 (IP); TCP/UDP at Layer 4",
            "Encapsulation adds headers as data travels down; decapsulation removes headers as it travels up"
        ],
        "crit": ["Correct ordering of all 7 layers", "Accurate protocol and data unit mapping for each layer"],
        "cm": ["Confusing Layer 2 (Data Link / MAC) with Layer 3 (Network / IP)", "Inability to distinguish OSI 7-layer model from the pragmatic 4-layer TCP/IP model"],
        "fu": ["How does packet encapsulation work as data traverses from Layer 7 to Layer 1?", "At which OSI layers do TLS/SSL and WebSockets operate?"],
        "tags": ["master-bank", "networking", "osi-model", "layers", "protocols", "top-30"]
    },
    {
        "q": "What is DNS (Domain Name System) and how does DNS resolution work step-by-step?",
        "cat": "Networking & IoT", "sub": "Application Protocols & DNS", "d": "Intermediate", "type": "technical",
        "roles": ["Software Development Engineer", "Backend Developer", "Full-Stack Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "DNS (Domain Name System) is the hierarchical, decentralized 'phonebook of the internet' that translates human-friendly domain names (e.g., `interviewace.ai`) into machine-routable IP addresses (e.g., `192.0.2.1` or `2606:4700::1`).\n\nStep-by-Step Resolution Flow (when you type a URL into a browser):\n1) Browser & OS Cache: The browser checks its local DNS cache; if missing, it checks the OS cache (`hosts` file, DNS resolver cache).\n2) Recursive Resolver (ISP or 1.1.1.1 / 8.8.8.8): If not cached locally, the query is sent to the Recursive DNS Server.\n3) Root Nameserver ('.'): The recursive resolver queries a Root Nameserver, which directs the query to the Top-Level Domain (TLD) server for `.ai`.\n4) TLD Nameserver: The `.ai` TLD server responds with the IP of the Authoritative Nameserver responsible for `interviewace.ai` (e.g., Cloudflare Nameserver).\n5) Authoritative Nameserver: The authoritative server contains the actual DNS records (A, AAAA, CNAME). It returns the destination IP address.\n6) Caching & Connection: The recursive resolver caches the result according to its TTL (Time-To-Live) and returns the IP to the client browser, which initiates the TCP handshake.",
        "kp": [
            "Translates human-readable domain names into machine-readable IP addresses",
            "Hierarchical lookup: Local Cache -> Recursive Resolver -> Root Server -> TLD Server -> Authoritative Server",
            "Key record types: A (IPv4), AAAA (IPv6), CNAME (alias), MX (mail), TXT (verification)",
            "TTL (Time to Live) governs how long records remain cached in intermediate resolvers"
        ],
        "crit": ["Clear, accurate hierarchical resolution steps", "Understanding the roles of Recursive vs Authoritative servers and TTL"],
        "cm": ["Believing the browser directly contacts the authoritative server immediately", "Ignoring DNS caching layers"],
        "fu": ["What is the difference between an A Record and a CNAME Record?", "What is DNS propagation and why do record updates take time?"],
        "tags": ["master-bank", "networking", "dns", "domain-resolution", "top-30"]
    },
    {
        "q": "What is the difference between a Router, a Switch, and a Hub?",
        "cat": "Networking & IoT", "sub": "Network Hardware & Devices", "d": "Beginner", "type": "technical",
        "roles": ["Software Development Engineer", "Network Engineer", "Support Engineer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "1) Hub (Layer 1 - Physical Layer):\n- Dumb device with zero intelligence: repeats incoming electrical signals to ALL connected ports indiscriminately.\n- Collision Domain: All ports share a single collision domain and single broadcast domain, causing collisions and network congestion.\n- Transmission: Half-duplex (cannot transmit and receive simultaneously).\n- Security: Insecure (all devices see every packet).\n\n2) Switch (Layer 2 - Data Link Layer):\n- Intelligent device: maintains a MAC Address Table (CAM Table) mapping hardware MAC addresses to specific physical ports.\n- Collision Domain: Each port has its OWN dedicated collision domain; all ports share one broadcast domain.\n- Transmission: Full-duplex (transmits and receives simultaneously without collisions).\n- Scope: Connects devices within the same Local Area Network (LAN).\n\n3) Router (Layer 3 - Network Layer):\n- Connects different networks and subnets (e.g., your home LAN to the public Internet WAN).\n- Addressing: Routes data using IP addresses; maintains a Routing Table and executes routing algorithms (OSPF, BGP).\n- Broadcast Domain: Separates broadcast domains (does not forward broadcast packets by default).\n- Features: NAT (Network Address Translation), DHCP server, Firewall protection.",
        "kp": [
            "Hub: Layer 1, broadcasts to all ports, single collision domain, half-duplex (obsolete)",
            "Switch: Layer 2, forwards frames using MAC addresses, isolated collision domains per port (LAN)",
            "Router: Layer 3, forwards packets across different networks using IP addresses, isolates broadcast domains (LAN to WAN)"
        ],
        "crit": ["Clear mapping to OSI layers (Layer 1 vs 2 vs 3)", "Accurate explanation of collision domains and broadcast domains"],
        "cm": ["Confusing a switch with a router", "Believing a switch routes between different IP subnets"],
        "fu": ["What is a Layer 3 Switch and how does it differ from a traditional router?", "What is the function of ARP (Address Resolution Protocol) in a local switch network?"],
        "tags": ["master-bank", "networking", "hardware", "router", "switch", "hub"]
    },
    {
        "q": "What are Cookies and Sessions? Explain the difference and when each should be used.",
        "cat": "Web Development", "sub": "State Management & Auth", "d": "Beginner", "type": "technical",
        "roles": ["Software Development Engineer", "Full-Stack Developer", "Backend Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "HTTP is inherently a stateless protocol. Cookies and Sessions are mechanisms used to preserve state across multiple HTTP requests:\n\n1) Cookies (Client-Side Storage):\n- Small key-value text pairs (max 4KB) stored inside the user's browser.\n- Automatically sent in the `Cookie` HTTP header with every subsequent request to the originating domain.\n- Security Flags: `HttpOnly` (blocks JavaScript access, preventing XSS theft), `Secure` (sent only over HTTPS), `SameSite=Lax/Strict` (prevents CSRF attacks).\n- Lifespan: Session cookies expire when the browser closes; persistent cookies expire after a defined `Max-Age` / `Expires` date.\n- Use Cases: Storing session IDs, theme preferences (dark mode), language selection, analytics tracking.\n\n2) Sessions (Server-Side Storage):\n- User state is stored on the server (in memory, Redis cache, or a database).\n- When a session is created, the server generates a cryptographically random Session ID and sends it to the browser inside an `HttpOnly` cookie.\n- On future requests, the browser sends the Session ID; the server looks up the user's authenticated state in its session store.\n- Use Cases: Storing authenticated user sessions, shopping cart contents, sensitive role/permission data.\n\nKey Trade-Off: Cookies consume client storage and are vulnerable to tampering if unsigned; Sessions consume server memory/Redis and require shared stores in horizontally scaled clusters.",
        "kp": [
            "Cookies: stored on client browser (4KB max); sent in HTTP headers automatically",
            "Sessions: stored on server (memory/Redis); identified by a session ID cookie",
            "Always protect auth cookies with HttpOnly, Secure, and SameSite flags",
            "Sessions are more secure for sensitive data; JWTs offer a stateless alternative"
        ],
        "crit": ["Clear client-side vs server-side distinction", "Understanding security flags (HttpOnly, Secure, SameSite)"],
        "cm": ["Storing sensitive user data (passwords, credit cards) directly in unencrypted cookies", "Ignoring session scaling across multiple server instances"],
        "fu": ["What is the difference between Session-based authentication and JWT (Token-based) authentication?", "How does SameSite cookie attribute protect against CSRF attacks?"],
        "tags": ["master-bank", "web-dev", "cookies", "sessions", "authentication", "security", "top-30"]
    },

    # =========================================================================
    # 2. TOP 30 CODING QUESTIONS (ARRAYS, STRINGS, BASIC ALGORITHMS)
    # =========================================================================
    # --- ARRAYS (10) ---
    {
        "q": "Write a program to find the maximum element in an array.",
        "cat": "Coding", "sub": "Arrays", "d": "Beginner", "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Iterate through the array maintaining a running maximum variable. Initialize with the first element (or negative infinity).\n\n```python\ndef find_max(arr: list[int]) -> int:\n    if not arr:\n        raise ValueError('Array cannot be empty')\n    max_val = arr[0]\n    for num in arr[1:]:\n        if num > max_val:\n            max_val = num\n    return max_val\n```\nTime Complexity: O(N) single pass. Space Complexity: O(1) auxiliary space.",
        "kp": ["Single pass linear scan O(N) time and O(1) memory", "Initialize with arr[0] rather than 0 to handle negative arrays", "Handle empty array edge case"],
        "crit": ["Clean implementation with edge case validation", "Explanation of time and space complexity"],
        "cm": ["Initializing max_val to 0 (fails if all numbers in array are negative)"],
        "fu": ["How would you find the maximum element in a rotated sorted array in O(log N) time?"],
        "tags": ["top-30", "coding", "arrays", "max-element"]
    },
    {
        "q": "Write a program to find the minimum element in an array.",
        "cat": "Coding", "sub": "Arrays", "d": "Beginner", "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Iterate through the array tracking the minimum element seen so far.\n\n```python\ndef find_min(arr: list[int]) -> int:\n    if not arr:\n        raise ValueError('Array cannot be empty')\n    min_val = arr[0]\n    for num in arr[1:]:\n        if num < min_val:\n            min_val = num\n    return min_val\n```\nTime Complexity: O(N). Space Complexity: O(1).",
        "kp": ["Linear scan O(N) time and O(1) space", "Initialize with arr[0]", "Handle empty input list"],
        "crit": ["Clean logic and edge-case handling"],
        "cm": ["Initializing with 0 which fails for positive numbers"],
        "fu": ["How to find both minimum and maximum in fewer than 2N comparisons (Pairwise comparisons)?"] ,
        "tags": ["top-30", "coding", "arrays", "min-element"]
    },
    {
        "q": "Write a program to find the second-largest element in an array without sorting.",
        "cat": "Coding", "sub": "Arrays", "d": "Beginner", "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Maintain two variables: `first` (largest) and `second` (second largest). In a single pass, update `second` when a new `first` is found, or when a number lies strictly between `second` and `first`.\n\n```python\ndef find_second_largest(arr: list[int]) -> int | None:\n    if len(arr) < 2:\n        return None\n    first = second = float('-inf')\n    for num in arr:\n        if num > first:\n            second = first\n            first = num\n        elif num > second and num != first:\n            second = num\n    return second if second != float('-inf') else None\n```\nTime Complexity: O(N) single pass. Space Complexity: O(1).",
        "kp": ["O(N) single pass without sorting overhead", "Handles duplicate maximums (e.g., [10, 10, 9] -> 9)", "Returns None if all elements are identical"],
        "crit": ["Proper handling of duplicates and negative numbers", "O(N) time and O(1) space"],
        "cm": ["Sorting the array first (takes O(N log N) time unnecessarily)", "Failing on arrays with duplicate largest elements"],
        "fu": ["How would you generalize this to find the K-th largest element (Quickselect / Min-Heap)?"],
        "tags": ["top-30", "coding", "arrays", "second-largest"]
    },
    {
        "q": "Write a program to remove duplicates from a sorted array in-place.",
        "cat": "Coding", "sub": "Arrays", "d": "Beginner", "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Use the Two-Pointer Technique (Slow and Fast pointer). Fast pointer scans ahead; Slow pointer writes unique elements in-place.\n\n```python\ndef remove_duplicates(nums: list[int]) -> int:\n    if not nums:\n        return 0\n    slow = 0\n    for fast in range(1, len(nums)):\n        if nums[fast] != nums[slow]:\n            slow += 1\n            nums[slow] = nums[fast]\n    return slow + 1  # Length of unique prefix\n```\nTime Complexity: O(N). Space Complexity: O(1) in-place modification.",
        "kp": ["Two-pointer pattern: slow write index and fast scan index", "In-place modification without extra memory allocation", "Time O(N), Space O(1)"],
        "crit": ["Clean in-place implementation meeting O(1) auxiliary space constraint"],
        "cm": ["Using an auxiliary hash set which violates the in-place O(1) requirement"],
        "fu": ["What if each unique element is allowed to appear at most twice (Remove Duplicates II)?"],
        "tags": ["top-30", "coding", "arrays", "two-pointers", "remove-duplicates"]
    },
    {
        "q": "Write a program to find the duplicate element in an array of N+1 integers between 1 and N.",
        "cat": "Coding", "sub": "Arrays", "d": "Intermediate", "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Floyd's Tortoise and Hare (Cycle Detection Algorithm). Treat the array as a linked list where `nums[i]` is a pointer to index `nums[i]`.\n\n```python\ndef find_duplicate(nums: list[int]) -> int:\n    # Phase 1: Detect cycle\n    slow = nums[0]\n    fast = nums[0]\n    while True:\n        slow = nums[slow]\n        fast = nums[nums[fast]]\n        if slow == fast:\n            break\n    \n    # Phase 2: Find entrance to cycle\n    ptr1 = nums[0]\n    ptr2 = slow\n    while ptr1 != ptr2:\n        ptr1 = nums[ptr1]\n        ptr2 = nums[ptr2]\n    return ptr1\n```\nTime Complexity: O(N). Space Complexity: O(1) without modifying the original array.",
        "kp": ["Floyd's Cycle-Finding Algorithm runs in O(N) time and O(1) space", "Does not mutate the input array", "Interprets array indices and values as a linked list cycle"],
        "crit": ["Explaining why cycle detection works using pigeonhole principle", "Strict adherence to O(1) space and read-only array"],
        "cm": ["Modifying array signs or sorting when interviewer specifies array is read-only"],
        "fu": ["Why is there guaranteed to be a cycle in this array (Pigeonhole Principle)?"],
        "tags": ["top-30", "coding", "arrays", "cycle-detection", "duplicate-element"]
    },
    {
        "q": "Write a program to reverse an array in-place.",
        "cat": "Coding", "sub": "Arrays", "d": "Beginner", "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Use two pointers starting at opposite ends (left at 0, right at N-1). Swap elements and increment left, decrement right until they meet.\n\n```python\ndef reverse_array(arr: list[int]) -> None:\n    left, right = 0, len(arr) - 1\n    while left < right:\n        arr[left], arr[right] = arr[right], arr[left]\n        left += 1\n        right -= 1\n```\nTime Complexity: O(N). Space Complexity: O(1) in-place.",
        "kp": ["Two-pointer approach swapping opposite ends", "In-place modification without creating a new list", "Terminates when left >= right"],
        "crit": ["Clean swap logic and pointer advancement"],
        "cm": ["Using `arr[::-1]` which allocates a completely new array rather than reversing in-place"],
        "fu": ["How would you rotate an array by K positions using the reversal algorithm in O(N) time and O(1) space?"],
        "tags": ["top-30", "coding", "arrays", "reverse-array"]
    },
    {
        "q": "Write a program to find the missing number in an array of size N-1 containing numbers from 1 to N.",
        "cat": "Coding", "sub": "Arrays", "d": "Beginner", "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Two optimal methods: Sum Formula and Bitwise XOR.\n\n```python\ndef find_missing_sum(nums: list[int]) -> int:\n    n = len(nums) + 1\n    expected = n * (n + 1) // 2\n    return expected - sum(nums)\n\ndef find_missing_xor(nums: list[int]) -> int:\n    n = len(nums) + 1\n    res = 0\n    for i in range(1, n + 1):\n        res ^= i\n    for x in nums:\n        res ^= x\n    return res\n```\nTime Complexity: O(N). Space Complexity: O(1). XOR avoids integer overflow in fixed-width integer languages.",
        "kp": ["Sum formula `N*(N+1)//2 - sum(arr)`", "XOR bit manipulation cancels duplicate pairs and prevents overflow", "Time O(N), Space O(1)"],
        "crit": ["Explaining both math and bitwise solutions"],
        "cm": ["Sorting the array first (takes O(N log N) time unnecessarily)"],
        "fu": ["How would you find two missing numbers in an array in O(N) time and O(1) space?"],
        "tags": ["top-30", "coding", "arrays", "missing-number", "math"]
    },
    {
        "q": "Write a program to count the frequency of each element in an array.",
        "cat": "Coding", "sub": "Arrays", "d": "Beginner", "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Use a hash map (dictionary) to accumulate frequencies in a single pass.\n\n```python\ndef element_frequencies(arr: list[int]) -> dict[int, int]:\n    freq = {}\n    for num in arr:\n        freq[num] = freq.get(num, 0) + 1\n    return freq\n```\nTime Complexity: O(N) average time. Space Complexity: O(U) where U is number of unique elements.",
        "kp": ["Single pass linear accumulation using hash map", "Time O(N), Space O(U)", "dict.get(num, 0) + 1 handles missing keys cleanly"],
        "crit": ["Clean hash map logic without nested count() calls"],
        "cm": ["Calling `arr.count(x)` inside a loop which results in O(N^2) complexity"],
        "fu": ["How would you find the top K most frequent elements in an array (Heap / Bucket Sort)?"],
        "tags": ["top-30", "coding", "arrays", "frequency", "hash-map"]
    },
    {
        "q": "Write a program to calculate the sum of all elements in an array.",
        "cat": "Coding", "sub": "Arrays", "d": "Beginner", "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Iterate through elements adding each to an accumulator variable.\n\n```python\ndef array_sum(arr: list[int]) -> int:\n    total = 0\n    for num in arr:\n        total += num\n    return total\n```\nTime Complexity: O(N). Space Complexity: O(1).",
        "kp": ["Linear traversal with accumulator variable", "O(N) time and O(1) space", "Handles empty array returning 0"],
        "crit": ["Clean implementation and complexity analysis"],
        "cm": ["Ignoring potential integer overflow in languages like C/C++ (use 64-bit int)"],
        "fu": ["What is a Prefix Sum array and how does it answer range sum queries in O(1) time?"],
        "tags": ["top-30", "coding", "arrays", "sum"]
    },
    {
        "q": "Write a program to solve the Two Sum problem (find indices of two numbers that add up to a target).",
        "cat": "Coding", "sub": "Arrays", "d": "Beginner", "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "One-Pass Hash Map. For each element `num`, check if `target - num` already exists in the dictionary. If yes, return indices; otherwise store `num -> index`.\n\n```python\ndef two_sum(nums: list[int], target: int) -> list[int]:\n    seen = {}\n    for i, num in enumerate(nums):\n        complement = target - num\n        if complement in seen:\n            return [seen[complement], i]\n        seen[num] = i\n    return []\n```\nTime Complexity: O(N) single pass. Space Complexity: O(N) hash map.",
        "kp": ["One-pass hash map achieves O(N) time instead of O(N^2) brute force", "Key = complement value, Value = index", "Handles duplicate numbers properly"],
        "crit": ["Optimal O(N) solution with index tracking"],
        "cm": ["Using nested loops with O(N^2) complexity", "Re-using the same element index twice"],
        "fu": ["How would you solve Two Sum if the input array is already sorted in O(1) extra space (Two Pointers)?"],
        "tags": ["top-30", "coding", "arrays", "two-sum", "hash-map"]
    },

    # --- STRINGS (10) ---
    {
        "q": "Write a program to reverse a string.",
        "cat": "Coding", "sub": "Strings", "d": "Beginner", "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Convert to list of characters and swap from both ends, or use two pointers:\n\n```python\ndef reverse_string(s: str) -> str:\n    chars = list(s)\n    left, right = 0, len(chars) - 1\n    while left < right:\n        chars[left], chars[right] = chars[right], chars[left]\n        left += 1\n        right -= 1\n    return ''.join(chars)\n```\nTime Complexity: O(N). Space Complexity: O(N) (in Python strings are immutable). In C++, takes O(1) auxiliary space.",
        "kp": ["Two-pointer swapping pattern", "Time O(N)", "Awareness of string immutability in Python/Java requiring list/StringBuilder"],
        "crit": ["Clean implementation without relying solely on Python's `s[::-1]` slice"],
        "cm": ["Repeatedly concatenating strings in a loop (results in O(N^2) memory allocations)"],
        "fu": ["Why are strings immutable in Python and Java?"],
        "tags": ["top-30", "coding", "strings", "reverse-string"]
    },
    {
        "q": "Write a program to check if a string is a palindrome.",
        "cat": "Coding", "sub": "Strings", "d": "Beginner", "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Compare characters from both ends moving inward using two pointers. Skip non-alphanumeric characters and ignore case.\n\n```python\ndef is_palindrome(s: str) -> bool:\n    left, right = 0, len(s) - 1\n    while left < right:\n        while left < right and not s[left].isalnum():\n            left += 1\n        while left < right and not s[right].isalnum():\n            right -= 1\n        if s[left].lower() != s[right].lower():\n            return False\n        left += 1\n        right -= 1\n    return True\n```\nTime Complexity: O(N). Space Complexity: O(1) auxiliary space.",
        "kp": ["Two-pointer inward traversal", "Filter non-alphanumeric characters and normalize case", "O(N) time and O(1) space"],
        "crit": ["Handling spaces, punctuation, and mixed case"],
        "cm": ["Creating a reversed copy of the string (consumes O(N) extra space)"],
        "fu": ["What is the longest palindromic substring algorithm (Expand Around Center / Manacher's Algorithm)?"],
        "tags": ["top-30", "coding", "strings", "palindrome", "two-pointers"]
    },
    {
        "q": "Write a program to count vowels and consonants in a string.",
        "cat": "Coding", "sub": "Strings", "d": "Beginner", "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Iterate through characters, checking against a set of vowels and verifying alphabetic characters.\n\n```python\ndef count_vowels_and_consonants(s: str) -> tuple[int, int]:\n    vowels = set('aeiouAEIOU')\n    v_count = c_count = 0\n    for char in s:\n        if char.isalpha():\n            if char in vowels:\n                v_count += 1\n            else:\n                c_count += 1\n    return v_count, c_count\n```\nTime Complexity: O(N). Space Complexity: O(1) (vowels set has constant size 10).",
        "kp": ["Single pass traversal", "Set lookup for vowels runs in O(1) time", "Filter non-alphabetic characters (digits, spaces, punctuation)"],
        "crit": ["Proper case normalization and ignoring punctuation"],
        "cm": ["Counting whitespace and punctuation marks as consonants"],
        "fu": ["How would you remove all vowels from a string in-place?"],
        "tags": ["top-30", "coding", "strings", "vowels", "consonants"]
    },
    {
        "q": "Write a program to count total characters in a string without using built-in len().",
        "cat": "Coding", "sub": "Strings", "d": "Beginner", "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Iterate through the string with a counter variable.\n\n```python\ndef count_characters(s: str) -> int:\n    count = 0\n    for _ in s:\n        count += 1\n    return count\n```\nTime Complexity: O(N). Space Complexity: O(1).",
        "kp": ["Linear traversal incrementing counter", "O(N) time, O(1) space", "Works on any iterable"],
        "crit": ["Clean implementation avoiding len()"],
        "cm": ["Attempting to index until IndexError (unidiomatic and slow)"],
        "fu": ["How does Python's len() achieve O(1) time complexity internally (ob_size in CPython PyVarObject)?"],
        "tags": ["top-30", "coding", "strings", "character-count"]
    },
    {
        "q": "Write a program to count the frequency of each character in a string.",
        "cat": "Coding", "sub": "Strings", "d": "Beginner", "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Use a hash map or array of size 256 for ASCII.\n\n```python\ndef char_frequency(s: str) -> dict[str, int]:\n    freq = {}\n    for char in s:\n        freq[char] = freq.get(char, 0) + 1\n    return freq\n```\nTime Complexity: O(N). Space Complexity: O(K) where K is unique character count (<= 256 for ASCII).",
        "kp": ["Hash map single pass counting", "Time O(N), Space O(1) for bounded ASCII alphabet", "Preserves counts for all characters"],
        "crit": ["Optimal O(N) frequency counting"],
        "cm": ["Using `s.count(c)` inside a loop (results in O(N^2) complexity)"],
        "fu": ["How to sort characters by decreasing frequency (Bucket Sort / Heap)?"],
        "tags": ["top-30", "coding", "strings", "frequency"]
    },
    {
        "q": "Write a program to remove duplicate characters from a string.",
        "cat": "Coding", "sub": "Strings", "d": "Beginner", "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Maintain a hash set of seen characters while appending first occurrences to a list to preserve original order.\n\n```python\ndef remove_duplicate_chars(s: str) -> str:\n    seen = set()\n    result = []\n    for char in s:\n        if char not in seen:\n            seen.add(char)\n            result.append(char)\n    return ''.join(result)\n```\nTime Complexity: O(N). Space Complexity: O(K) where K is unique characters.",
        "kp": ["Hash set provides O(1) lookup to track seen characters", "List accumulator preserves original left-to-right ordering", "Time O(N), Space O(K)"],
        "crit": ["Preserves original string order"],
        "cm": ["Using `set(s)` directly (destroys the original character order)"],
        "fu": ["What if you must remove duplicate characters in O(1) extra space?"],
        "tags": ["top-30", "coding", "strings", "remove-duplicates"]
    },
    {
        "q": "Write a program to check whether two strings are anagrams of each other.",
        "cat": "Coding", "sub": "Strings", "d": "Beginner", "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Two strings are anagrams if they contain identical characters with identical frequencies.\n\n```python\nfrom collections import Counter\n\ndef is_anagram(s1: str, s2: str) -> bool:\n    if len(s1) != len(s2):\n        return False\n    return Counter(s1.lower()) == Counter(s2.lower())\n```\nTime Complexity: O(N). Space Complexity: O(1) for bounded alphabet.",
        "kp": ["Length check early exit O(1)", "Frequency map comparison runs in O(N) time", "Sorting takes O(N log N) time"],
        "crit": ["Handling case normalization and string length mismatch"],
        "cm": ["Assuming sorting is optimal (hash map is faster: O(N) vs O(N log N))"],
        "fu": ["How would you group an array of strings into anagram clusters (Group Anagrams)?"],
        "tags": ["top-30", "coding", "strings", "anagrams"]
    },
    {
        "q": "Write a program to reverse the words in a given string sentence.",
        "cat": "Coding", "sub": "Strings", "d": "Beginner", "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Split by whitespace, filter empty strings, and reverse the word tokens.\n\n```python\ndef reverse_words(sentence: str) -> str:\n    words = sentence.strip().split()\n    return ' '.join(reversed(words))\n```\nTime Complexity: O(N). Space Complexity: O(N). In languages with mutable strings like C++, reverse the entire string, then reverse each word in-place for O(1) extra space.",
        "kp": ["Tokenize words and reverse order", "Handles leading, trailing, and multiple consecutive spaces cleanly", "Time O(N), Space O(N)"],
        "crit": ["Handling multiple spaces between words"],
        "cm": ["Using basic split(' ') which leaves empty string tokens when multiple spaces exist"],
        "fu": ["How do you reverse words in-place in a character array with O(1) extra space?"],
        "tags": ["top-30", "coding", "strings", "reverse-words"]
    },
    {
        "q": "Write a program to find the first non-repeating character in a string.",
        "cat": "Coding", "sub": "Strings", "d": "Beginner", "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Two-pass algorithm: Pass 1 counts character frequencies; Pass 2 scans from left to right to return the first character with count == 1.\n\n```python\ndef first_non_repeating_char(s: str) -> str | None:\n    freq = {}\n    for c in s:\n        freq[c] = freq.get(c, 0) + 1\n    for c in s:\n        if freq[c] == 1:\n            return c\n    return None\n```\nTime Complexity: O(N). Space Complexity: O(1) for bounded alphabet.",
        "kp": ["Two-pass linear algorithm: count then scan", "Preserves original left-to-right order", "Time O(N), Space O(1)"],
        "crit": ["Optimal O(N) approach preserving order"],
        "cm": ["Using `s.count(c)` inside a loop (O(N^2) complexity)"],
        "fu": ["How to solve this for an infinite streaming input of characters (Queue + Frequency Map)?"],
        "tags": ["top-30", "coding", "strings", "first-non-repeating"]
    },
    {
        "q": "Write a program to find the longest word in a sentence.",
        "cat": "Coding", "sub": "Strings", "d": "Beginner", "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Split sentence into words and track the word with the maximum length.\n\n```python\nimport re\n\ndef longest_word(sentence: str) -> str:\n    # Strip punctuation and split into words\n    words = re.findall(r'\\b\\w+\\b', sentence)\n    if not words:\n        return ''\n    longest = words[0]\n    for word in words[1:]:\n        if len(word) > len(longest):\n            longest = word\n    return longest\n```\nTime Complexity: O(N). Space Complexity: O(N).",
        "kp": ["Strip punctuation before comparing word lengths", "Linear scan tracking max length", "Time O(N), Space O(N)"],
        "crit": ["Handling punctuation attached to words like 'hello, world!'"],
        "cm": ["Splitting purely on spaces without stripping trailing commas or periods"],
        "fu": ["What if two words have the exact same maximum length?"],
        "tags": ["top-30", "coding", "strings", "longest-word"]
    },

    # --- BASIC ALGORITHMS (10) ---
    {
        "q": "Write a program to generate the Fibonacci series up to N terms (Iterative and Recursive).",
        "cat": "Coding", "sub": "Basic Algorithms", "d": "Beginner", "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Iterative approach uses two variables (`a, b = 0, 1`) in O(N) time and O(1) space. Naive recursion is O(2^N); memoized recursion is O(N) time and O(N) space.\n\n```python\n# Iterative (Optimal O(N) time, O(1) space)\ndef fibonacci_iterative(n: int) -> list[int]:\n    if n <= 0:\n        return []\n    if n == 1:\n        return [0]\n    series = [0, 1]\n    for _ in range(2, n):\n        series.append(series[-1] + series[-2])\n    return series\n\n# Dynamic Programming Nth Fibonacci\ndef fib_dp(n: int) -> int:\n    if n <= 1:\n        return n\n    a, b = 0, 1\n    for _ in range(2, n + 1):\n        a, b = b, a + b\n    return b\n```\nTime Complexity: O(N). Space Complexity: O(1) auxiliary space.",
        "kp": ["Iterative DP runs in O(N) time and O(1) auxiliary space", "Naive recursion F(n-1) + F(n-2) takes exponential O(2^N) time", "Base cases: F(0)=0, F(1)=1"],
        "crit": ["Explaining why naive recursion is inefficient compared to iterative DP"],
        "cm": ["Using unmemoized recursion on large N (causes stack overflow and hangs)"],
        "fu": ["How can you compute the N-th Fibonacci number in O(log N) time using Matrix Exponentiation?"],
        "tags": ["top-30", "coding", "algorithms", "fibonacci", "dynamic-programming"]
    },
    {
        "q": "Write a program to calculate the factorial of a number (Iterative and Recursive).",
        "cat": "Coding", "sub": "Basic Algorithms", "d": "Beginner", "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Factorial of N (`N!`) is `N * (N-1) * ... * 1`. Base case: `0! = 1` and `1! = 1`.\n\n```python\n# Iterative (O(N) time, O(1) space)\ndef factorial_iterative(n: int) -> int:\n    if n < 0:\n        raise ValueError('Factorial is not defined for negative numbers')\n    res = 1\n    for i in range(2, n + 1):\n        res *= i\n    return res\n\n# Recursive (O(N) time, O(N) call stack space)\ndef factorial_recursive(n: int) -> int:\n    if n < 0:\n        raise ValueError('Negative numbers invalid')\n    if n <= 1:\n        return 1\n    return n * factorial_recursive(n - 1)\n```\nTime Complexity: O(N). Space Complexity: O(1) iterative vs O(N) recursive call stack.",
        "kp": ["Base cases: 0! = 1 and 1! = 1", "Iterative is preferred to avoid recursion call stack overhead", "Validate non-negative input"],
        "crit": ["Handling 0! = 1 and rejecting negative inputs"],
        "cm": ["Returning 0 for 0! (0! is mathematically 1)"],
        "fu": ["How would you calculate trailing zeros in N! in O(log N) time (Legendre's Formula: N//5 + N//25 + ...)?"] ,
        "tags": ["top-30", "coding", "algorithms", "factorial", "recursion"]
    },
    {
        "q": "Write a program to check whether a number is Prime.",
        "cat": "Coding", "sub": "Basic Algorithms", "d": "Beginner", "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "A prime number has exactly two distinct factors: 1 and itself. Numbers <= 1 are not prime. Test divisibility up to `sqrt(N)`.\n\n```python\nimport math\n\ndef is_prime(n: int) -> bool:\n    if n <= 1:\n        return False\n    if n <= 3:\n        return True\n    if n % 2 == 0 or n % 3 == 0:\n        return False\n    # Check 6k +/- 1 up to sqrt(n)\n    i = 5\n    while i * i <= n:\n        if n % i == 0 or n % (i + 2) == 0:\n            return False\n        i += 6\n    return True\n```\nTime Complexity: O(sqrt(N)). Space Complexity: O(1).",
        "kp": ["Factors repeat after sqrt(N), so checking up to sqrt(N) is sufficient", "Handle numbers <= 1 (not prime)", "6k +/- 1 optimization skips multiples of 2 and 3"],
        "crit": ["Optimized O(sqrt(N)) trial division instead of O(N)"],
        "cm": ["Checking all numbers up to N (O(N) brute force)", "Considering 1 as a prime number (1 is not prime)"],
        "fu": ["How does the Sieve of Eratosthenes generate all prime numbers up to N in O(N log log N) time?"],
        "tags": ["top-30", "coding", "algorithms", "prime-number", "math"]
    },
    {
        "q": "Write a program to check whether a number is an Armstrong number.",
        "cat": "Coding", "sub": "Basic Algorithms", "d": "Beginner", "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "An Armstrong number (Narcissistic number) is a number equal to the sum of its digits each raised to the power of the number of digits (e.g., `153 = 1^3 + 5^3 + 3^3 = 1 + 125 + 27 = 153`).\n\n```python\ndef is_armstrong(n: int) -> bool:\n    if n < 0:\n        return False\n    num_str = str(n)\n    power = len(num_str)\n    total = sum(int(digit) ** power for digit in num_str)\n    return total == n\n```\nTime Complexity: O(D) where D is number of digits (D = log10(N)). Space Complexity: O(1).",
        "kp": ["Calculate total number of digits D first", "Sum each digit raised to power D", "Time complexity O(log10(N))"],
        "crit": ["Clean digit extraction and power calculation"],
        "cm": ["Hardcoding power = 3 (fails for 4-digit Armstrong numbers like 1634 = 1^4 + 6^4 + 3^4 + 4^4)"],
        "fu": ["How would you extract digits mathematically using modulo `% 10` and division `// 10` without string conversion?"],
        "tags": ["top-30", "coding", "algorithms", "armstrong-number", "math"]
    },
    {
        "q": "Write a program to check whether a number is a Perfect number.",
        "cat": "Coding", "sub": "Basic Algorithms", "d": "Beginner", "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "A Perfect number is a positive integer equal to the sum of its proper positive divisors (excluding the number itself). Example: `6 = 1 + 2 + 3 = 6`, `28 = 1 + 2 + 4 + 7 + 14 = 28`.\n\n```python\ndef is_perfect_number(n: int) -> bool:\n    if n <= 1:\n        return False\n    div_sum = 1  # 1 is always a proper divisor\n    i = 2\n    while i * i <= n:\n        if n % i == 0:\n            div_sum += i\n            if i * i != n:  # Add paired divisor\n                div_sum += n // i\n        i += 1\n    return div_sum == n\n```\nTime Complexity: O(sqrt(N)). Space Complexity: O(1).",
        "kp": ["Sum proper divisors up to sqrt(N), adding paired divisor `N // i`", "Do not add `i` twice when `i * i == n`", "Time O(sqrt(N)), Space O(1)"],
        "crit": ["Optimized O(sqrt(N)) approach avoiding O(N) scan"],
        "cm": ["Adding the number itself to the sum of proper divisors"],
        "fu": ["What is the relationship between Mersenne primes and even perfect numbers (Euclid-Euler Theorem)?"],
        "tags": ["top-30", "coding", "algorithms", "perfect-number", "math"]
    },
    {
        "q": "Write a program to find the Greatest Common Divisor (GCD / HCF) of two numbers using the Euclidean Algorithm.",
        "cat": "Coding", "sub": "Basic Algorithms", "d": "Beginner", "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Euclidean Algorithm: `GCD(a, b) = GCD(b, a % b)`. Continue until remainder is 0; the non-zero divisor is the GCD.\n\n```python\ndef gcd(a: int, b: int) -> int:\n    while b != 0:\n        a, b = b, a % b\n    return abs(a)\n```\nTime Complexity: O(log(min(a, b))) (Lamé's Theorem). Space Complexity: O(1).",
        "kp": ["Euclidean algorithm uses modulo: `while b: a, b = b, a % b`", "Time complexity O(log(min(A, B)))", "Works regardless of which number is larger"],
        "crit": ["Clean implementation of Euclidean algorithm"],
        "cm": ["Using linear decrement `while i > 0` which takes O(min(A, B)) time instead of logarithmic"],
        "fu": ["What is the Extended Euclidean Algorithm and how is it used in modular inverse cryptography?"],
        "tags": ["top-30", "coding", "algorithms", "gcd", "math"]
    },
    {
        "q": "Write a program to find the Least Common Multiple (LCM) of two numbers.",
        "cat": "Coding", "sub": "Basic Algorithms", "d": "Beginner", "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Mathematical relationship: `a * b = GCD(a, b) * LCM(a, b)`. Therefore, `LCM(a, b) = (a * b) // GCD(a, b)`.\n\n```python\ndef gcd(a: int, b: int) -> int:\n    while b != 0:\n        a, b = b, a % b\n    return abs(a)\n\ndef lcm(a: int, b: int) -> int:\n    if a == 0 or b == 0:\n        return 0\n    return abs(a * b) // gcd(a, b)\n```\nTime Complexity: O(log(min(a, b))). Space Complexity: O(1).",
        "kp": ["Formula: `(a * b) // gcd(a, b)`", "Avoid integer overflow by computing `(a // gcd(a, b)) * b`", "Handle 0 input returning 0"],
        "crit": ["Efficient calculation using GCD relationship"],
        "cm": ["Brute force incrementing `lcm += max(a, b)` which is extremely slow on large coprimes"],
        "fu": ["How do you find the LCM of an array of N numbers?"],
        "tags": ["top-30", "coding", "algorithms", "lcm", "math"]
    },
    {
        "q": "Write a program to implement Binary Search on a sorted array.",
        "cat": "Coding", "sub": "Basic Algorithms", "d": "Beginner", "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Binary Search repeatedly divides a sorted search space in half. Compare target with middle element `mid`. If target == arr[mid], return mid; if target < arr[mid], search left half; else search right half.\n\n```python\ndef binary_search(arr: list[int], target: int) -> int:\n    left, right = 0, len(arr) - 1\n    while left <= right:\n        mid = left + (right - left) // 2  # Prevents integer overflow\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1  # Target not found\n```\nTime Complexity: O(log N). Space Complexity: O(1) iterative.",
        "kp": ["Requires array to be SORTED beforehand", "Halves search space each iteration: O(log N) time", "Calculate `mid = left + (right - left) // 2` to prevent overflow in languages with fixed integer limits"],
        "crit": ["Correct loop boundary condition `left <= right` and mid calculation"],
        "cm": ["Using `(left + right) // 2` in C++/Java which can cause integer overflow when sum exceeds 2^31 - 1", "Applying binary search on unsorted arrays"],
        "fu": ["What are Lower Bound and Upper Bound binary searches (bisect_left and bisect_right)?", "How to search in a rotated sorted array in O(log N) time?"],
        "tags": ["top-30", "coding", "algorithms", "binary-search"]
    },
    {
        "q": "Write a program to implement Linear Search on an array.",
        "cat": "Coding", "sub": "Basic Algorithms", "d": "Beginner", "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Sequentially inspect each element from index 0 to N-1 until target is found or array ends.\n\n```python\ndef linear_search(arr: list[int], target: int) -> int:\n    for i in range(len(arr)):\n        if arr[i] == target:\n            return i\n    return -1\n```\nTime Complexity: O(N) worst and average case, O(1) best case. Space Complexity: O(1). Works on both sorted and unsorted collections.",
        "kp": ["Checks each element sequentially", "Works on unsorted data without preprocessing", "Time O(N), Space O(1)"],
        "crit": ["Clean implementation returning index or -1"],
        "cm": ["Assuming linear search requires sorted data"],
        "fu": ["When is linear search preferred over binary search (small N < 30, linked lists, unsorted streams)?"],
        "tags": ["top-30", "coding", "algorithms", "linear-search"]
    },
    {
        "q": "Compare common Sorting Algorithms (Bubble Sort, Insertion Sort, Merge Sort, Quick Sort) and implement Merge Sort.",
        "cat": "Coding", "sub": "Basic Algorithms", "d": "Intermediate", "type": "coding",
        "roles": ["Software Development Engineer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Comparison:\n- Bubble Sort: O(N^2) time, O(1) space. Stable. Repeatedly swaps adjacent out-of-order elements.\n- Insertion Sort: O(N^2) time, O(1) space (O(N) best case on nearly sorted data). Stable.\n- Merge Sort: O(N log N) time in all cases, O(N) auxiliary space. Stable. Divide-and-conquer.\n- Quick Sort: O(N log N) average time, O(N^2) worst case, O(log N) space. Unstable in-place.\n\nMerge Sort Implementation (Divide and Conquer):\n```python\ndef merge_sort(arr: list[int]) -> list[int]:\n    if len(arr) <= 1:\n        return arr\n    mid = len(arr) // 2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n    return merge(left, right)\n\ndef merge(left: list[int], right: list[int]) -> list[int]:\n    result = []\n    i = j = 0\n    while i < len(left) and j < len(right):\n        if left[i] <= right[j]:  # <= ensures stability\n            result.append(left[i])\n            i += 1\n        else:\n            result.append(right[j])\n            j += 1\n    result.extend(left[i:])\n    result.extend(right[j:])\n    return result\n```\nTime Complexity: O(N log N) in best, average, and worst cases. Space Complexity: O(N).",
        "kp": ["Merge Sort guarantees O(N log N) worst-case time", "Divide and conquer: split in half, sort recursively, merge two sorted halves", "Stable sort: preserves relative order of equal elements", "Requires O(N) extra memory space"],
        "crit": ["Clear complexity comparison across sorting algorithms", "Clean recursive Merge Sort implementation with stable merge logic"],
        "cm": ["Confusing Merge Sort O(N) space with Quick Sort O(log N) space", "Thinking Quick Sort guarantees O(N log N) worst-case time"],
        "fu": ["What is Timsort (used in Python and Java) and how does it combine Merge Sort and Insertion Sort?", "What makes an algorithm 'stable'?"],
        "tags": ["top-30", "coding", "algorithms", "sorting", "merge-sort"]
    },

    # =========================================================================
    # 3. OPERATING SYSTEMS (OS) SECTION
    # =========================================================================
    {
        "q": "What is a Process in Operating Systems? Explain its components and memory layout.",
        "cat": "Operating Systems", "sub": "Process Management", "d": "Beginner", "type": "technical",
        "roles": ["Software Development Engineer", "Backend Developer", "Systems Engineer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "A Process is a program in execution. While a program is a passive entity stored on disk (e.g., an executable binary file), a process is an active entity loaded into RAM with its own dedicated address space, execution state, and system resources.\n\nProcess Memory Layout (from low to high memory):\n1) Text / Code Segment: Contains the compiled machine instructions (read-only to prevent accidental modification).\n2) Data Segment:\n   - Initialized Data Segment: Global and static variables explicitly initialized by developer.\n   - BSS Segment (Uninitialized Data): Global and static variables initialized to zero by default.\n3) Heap Segment: Dynamically allocated memory at runtime (e.g., `malloc()` in C, `new` in Java/C++, Python objects). Grows upwards toward higher memory addresses.\n4) Stack Segment: Stores function call frames, local variables, return addresses, and parameter registers. Grows downwards toward lower memory addresses.\n\nProcess Control Block (PCB):\nThe OS kernel represents each process via a data structure called the PCB containing: Process ID (PID), Process State (New, Ready, Running, Waiting, Terminated), Program Counter (PC), CPU Registers, Scheduling Info, Memory Limits, and Open File Descriptors.",
        "kp": [
            "Program is passive code on disk; Process is active instance running in memory",
            "4 Memory segments: Text (code), Data (globals/statics), Heap (dynamic runtime), Stack (call frames/locals)",
            "PCB (Process Control Block) tracks PID, registers, program counter, and execution state",
            "Processes run in isolated address spaces protected by hardware memory bounds"
        ],
        "crit": ["Accurate explanation of memory layout (Text, Data, Heap, Stack)", "Clear understanding of the PCB structure"],
        "cm": ["Confusing Stack memory (automatic local allocation) with Heap memory (dynamic manual allocation)", "Thinking two processes can directly read each other's memory without IPC"],
        "fu": ["What happens when the Stack and Heap collide (Stack Overflow / Out of Memory)?", "What are the 5 states of a process lifecycle?"],
        "tags": ["master-bank", "os", "process", "pcb", "memory-layout", "top-30"]
    },
    {
        "q": "What is a Thread? Explain user-level threads versus kernel-level threads.",
        "cat": "Operating Systems", "sub": "Threads & Concurrency", "d": "Beginner", "type": "technical",
        "roles": ["Software Development Engineer", "Backend Developer", "Systems Engineer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "A Thread is the smallest, basic unit of CPU execution (often called a 'Lightweight Process'). Multiple threads exist within the context of a single parent process, sharing its address space, code segment, data segment, and open files, while maintaining their own private thread state:\n\nPrivate to Each Thread:\n- Thread ID (TID)\n- Program Counter (PC tracking instruction execution)\n- Register Set (working CPU variables)\n- Private Call Stack (local variables and function activation frames)\n\nShared Across All Threads in Process:\n- Code / Text segment\n- Data segment (global variables)\n- Heap memory (dynamically allocated objects)\n- OS resources (open files, network sockets, signals)\n\nUser-Level vs Kernel-Level Threads:\n1) User-Level Threads (ULT):\n- Managed entirely by a user-space runtime thread library without kernel awareness.\n- Fast context switching (no mode switch to kernel mode required).\n- Major drawback: If one thread makes a blocking system call (e.g., synchronous disk I/O), the entire process and all its threads are blocked by the OS.\n\n2) Kernel-Level Threads (KLT):\n- Created, scheduled, and managed directly by the OS kernel scheduler.\n- True parallelism: different threads of the same process can run concurrently on multiple physical CPU cores.\n- Blocking one thread does not block others.\n- Higher context switch overhead (requires user-to-kernel mode switch).",
        "kp": [
            "Smallest unit of CPU execution within a process; shares heap/code/data, keeps private stack/registers",
            "User-level threads: fast user-space switching, but blocking one blocks all",
            "Kernel-level threads: scheduled by OS across multiple CPU cores, true multicore parallelism",
            "Lightweight: creating and switching threads is much faster than processes"
        ],
        "crit": ["Clear distinction of what is shared vs what is private per thread", "Accurate comparison between User-Level and Kernel-Level threads"],
        "cm": ["Assuming threads share call stacks (each thread MUST have its own independent stack)", "Believing user-level threads can achieve multicore CPU parallelism"],
        "fu": ["What is the Python GIL (Global Interpreter Lock) and how does it affect multithreading in CPython?", "What are Green Threads / Goroutines / Virtual Threads?"],
        "tags": ["master-bank", "os", "threads", "concurrency", "ult-klt", "top-30"]
    },
    {
        "q": "What is the difference between a Process and a Thread (Process vs Thread)?",
        "cat": "Operating Systems", "sub": "Processes vs Threads", "d": "Beginner", "type": "technical",
        "roles": ["Software Development Engineer", "Backend Developer", "Full-Stack Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "1) Definition:\n- Process: An independent executing program with its own private virtual address space.\n- Thread: A lightweight execution path within a process; shares memory with peer threads.\n\n2) Memory Isolation:\n- Process: Completely isolated. Process A cannot access Process B's memory without explicit IPC (Inter-Process Communication).\n- Thread: Shared address space. All threads in a process share the heap, globals, and file descriptors.\n\n3) Creation & Destruction Cost:\n- Process: Heavyweight. Requires allocating address space, page tables, file handles, and PCB.\n- Thread: Lightweight. Requires allocating only a thread control block (TCB), registers, and stack.\n\n4) Context Switching Overhead:\n- Process: High. Flushes CPU cache, invalidates TLB (Translation Lookaside Buffer), and switches memory mapping.\n- Thread: Low. CPU cache and TLB remain valid since virtual memory address space does not change.\n\n5) Communication:\n- Process: Requires IPC (Pipes, Message Queues, Shared Memory, Sockets).\n- Thread: Direct memory access (reading/writing shared variables; requires mutex/locks to prevent race conditions).\n\n6) Crash Impact:\n- Process: A crash in one process does not affect other processes.\n- Thread: A crash (e.g., segmentation fault) in one thread terminates the entire parent process.",
        "kp": [
            "Process = heavyweight, isolated memory, expensive context switch, crash isolation",
            "Thread = lightweight, shared memory, fast context switch, shared fate on crash",
            "Processes communicate via IPC; threads communicate directly via shared memory with locks"
        ],
        "crit": ["Comprehensive comparison across memory, creation cost, context switching, IPC, and crash impact", "Understanding TLB invalidation in process context switching"],
        "cm": ["Saying threads are just smaller processes without explaining shared address space", "Claiming thread communication requires IPC"],
        "fu": ["Why does process context switching flush the TLB, but thread context switching does not?", "When would an engineer choose multiprocessing over multithreading?"],
        "tags": ["master-bank", "os", "process-vs-thread", "concurrency", "top-30"]
    },
    {
        "q": "What is Multithreading? What are its advantages and common pitfalls?",
        "cat": "Operating Systems", "sub": "Concurrency & Multithreading", "d": "Intermediate", "type": "technical",
        "roles": ["Software Development Engineer", "Backend Developer", "Systems Engineer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Multithreading is the capability of a CPU (or a single process) to execute multiple threads concurrently or in parallel:\n\nAdvantages:\n1) Responsiveness: In GUI/Web applications, a background thread can perform slow disk/network I/O without freezing the main user interface thread.\n2) Resource Sharing & Efficiency: Threads share memory naturally, eliminating expensive IPC mechanisms.\n3) Economy: Creating and context switching threads is 10x-100x cheaper than processes.\n4) Multicore Utilization: Enables true hardware parallelism by executing separate threads across distinct CPU cores.\n\nCommon Pitfalls & Challenges:\n1) Race Conditions: Occurs when multiple threads concurrently read and write shared data without synchronization, producing unpredictable corrupted states.\n2) Deadlocks: Occurs when two or more threads are permanently blocked, each holding a lock that the other needs.\n3) Starvation: A thread is perpetually denied CPU access because higher-priority threads dominate resources.\n4) Thread Overhead & Thrashing: Spawning too many threads causes the CPU to spend more time context switching than executing useful application instructions.\n5) Synchronization Overhead: Overusing locks (mutexes) serializes code, destroying the concurrency benefit.",
        "kp": [
            "Enables responsiveness, efficient resource sharing, and multicore parallel execution",
            "Race conditions occur when unsynchronized threads mutate shared state",
            "Pitfalls: deadlocks, race conditions, starvation, and context-switching overhead",
            "Use thread pools and thread-safe data structures to manage concurrency"
        ],
        "crit": ["Clear trade-off analysis between concurrency gains vs synchronization complexity", "Accurate definitions of race condition and deadlock"],
        "cm": ["Assuming adding more threads always makes an application run faster", "Ignoring race conditions on shared memory mutations"],
        "fu": ["What is the difference between Concurrency and Parallelism?", "How does a Thread Pool prevent thread creation overhead?"],
        "tags": ["master-bank", "os", "multithreading", "race-conditions", "concurrency", "top-30"]
    },
    {
        "q": "What is Context Switching in an Operating System? Why is it considered an overhead?",
        "cat": "Operating Systems", "sub": "CPU Scheduling & Execution", "d": "Intermediate", "type": "technical",
        "roles": ["Software Development Engineer", "Backend Developer", "Systems Engineer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Context Switching is the procedure performed by the OS kernel scheduler to save the current execution state ('context') of a running process or thread, and restore the state of a previously paused process/thread so that its execution can resume.\n\nWhat Is Saved and Restored:\n1) Program Counter (PC): The memory address of the next instruction to execute.\n2) CPU Registers: General-purpose registers, stack pointer, accumulator, condition flags.\n3) Memory Management State: Page tables, segment pointers, and virtual memory mappings.\n4) Process Status: In the PCB (Process Control Block) or TCB (Thread Control Block).\n\nWhy It Is Pure Overhead:\n1) Zero Useful Work Done: While the CPU is saving registers, executing the dispatcher, and restoring registers, no user application logic executes.\n2) Cache Invalidation (Cold Cache): The CPU hardware L1/L2/L3 caches hold data and instructions belonging to the previous process. The new process experiences a flood of cache misses, stalling the CPU until its working set is reloaded.\n3) TLB (Translation Lookaside Buffer) Flush: In a full process switch, the TLB must be flushed to avoid memory cross-contamination, causing expensive page table traversals.\n4) Frequency: Modern preemptive kernels context switch hundreds of times per second; if time slices are too small, CPU thrashing occurs.",
        "kp": [
            "Saves state (registers, PC, stack pointer) to PCB/TCB and restores next task's state",
            "Pure overhead: CPU executes zero application code during the switch",
            "Causes hardware cache pollution (L1/L2 cache misses) and TLB flushes",
            "Thread context switch is faster because virtual memory and TLB mappings are preserved"
        ],
        "crit": ["Accurate list of saved registers and state", "Clear explanation of hardware cache and TLB invalidation overhead"],
        "cm": ["Thinking context switching performs application computations", "Assuming thread switches flush page tables"],
        "fu": ["What hardware mechanisms exist to speed up context switching (e.g. multiple register sets)?", "What triggers a context switch (interrupts, system calls, time-slice expiry)?"],
        "tags": ["master-bank", "os", "context-switching", "pcb", "tlb", "cpu-overhead", "top-30"]
    },
    {
        "q": "What is a Deadlock in an Operating System? How can it be prevented?",
        "cat": "Operating Systems", "sub": "Synchronization & Deadlocks", "d": "Intermediate", "type": "technical",
        "roles": ["Software Development Engineer", "Backend Developer", "Systems Engineer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "A Deadlock is an execution state where a set of processes are permanently blocked because each process holds a resource that another process needs, and is waiting for a resource that another process holds. No process can proceed, allocate resources, or terminate.\n\nClassic Example (Two Threads, Two Locks):\n- Thread 1 locks Resource A, attempts to acquire Resource B.\n- Concurrently, Thread 2 locks Resource B, attempts to acquire Resource A.\n- Result: Both threads wait indefinitely.\n\nDeadlock Prevention (Invalidate at least ONE of the 4 Coffman conditions):\n1) Eliminate Mutual Exclusion: Make resources shareable where possible (e.g., read-only files, lock-free data structures).\n2) Eliminate Hold and Wait: Require a process to request and receive ALL required resources at once before execution begins; if one resource is unavailable, it holds none.\n3) Eliminate No Preemption: If a process holding resources is denied an additional resource, it must forcibly release (preempt) all its currently held resources and retry later.\n4) Eliminate Circular Wait (Most Practical Standard): Impose a strict global numerical ordering on all resources (e.g., Lock 1 < Lock 2 < Lock 3). Enforce that every process must acquire resources strictly in ascending numerical order.",
        "kp": [
            "Deadlock: set of processes permanently blocked waiting for resources held by each other",
            "Prevented by breaking at least one of the 4 Coffman conditions",
            "Resource Ordering is the most practical engineering prevention strategy (acquire locks in fixed order)",
            "Deadlock Avoidance uses algorithms like Banker's Algorithm to verify safe states before granting resources"
        ],
        "crit": ["Clear, concrete example of deadlock", "Systematic explanation of prevention techniques targeting each Coffman condition"],
        "cm": ["Confusing Deadlock Prevention (designing system so deadlocks are mathematically impossible) with Deadlock Detection and Recovery", "Failing to explain Resource Ordering"],
        "fu": ["What is the difference between Deadlock Prevention and Deadlock Avoidance (Banker's Algorithm)?", "What is the Dining Philosophers Problem and how does it illustrate deadlock?"],
        "tags": ["master-bank", "os", "deadlock", "coffman-conditions", "concurrency", "top-30"]
    },
    {
        "q": "What are the 4 Coffman Conditions required for a Deadlock to occur?",
        "cat": "Operating Systems", "sub": "Synchronization & Deadlocks", "d": "Intermediate", "type": "technical",
        "roles": ["Software Development Engineer", "Backend Developer", "Systems Engineer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "In 1971, Edward Coffman Jr. proved that a deadlock can arise IF AND ONLY IF all four of the following conditions hold simultaneously in a system:\n\n1) Mutual Exclusion:\n- At least one resource must be non-shareable. Only one process can use the resource at any given time.\n- If another process requests that resource, it must wait until the resource is released.\n\n2) Hold and Wait:\n- A process must currently be holding at least one resource and simultaneously waiting to acquire additional resources that are currently held by other active processes.\n\n3) No Preemption:\n- Resources cannot be forcibly taken away from a process while it is using them.\n- A resource can only be released voluntarily by the process holding it after completing its task.\n\n4) Circular Wait:\n- There must exist a closed chain of processes {P0, P1, ..., Pn} such that P0 is waiting for a resource held by P1, P1 is waiting for a resource held by P2, ..., and Pn is waiting for a resource held by P0.\n\nEngineering Takeaway: If you design a system that guarantees even ONE of these four conditions cannot hold, deadlocks become mathematically impossible.",
        "kp": [
            "1. Mutual Exclusion: resources cannot be shared simultaneously",
            "2. Hold and Wait: holding resources while requesting more",
            "3. No Preemption: resources cannot be forcibly reclaimed",
            "4. Circular Wait: closed loop of processes waiting for each other",
            "All 4 conditions must hold simultaneously for a deadlock to exist"
        ],
        "crit": ["Precise naming and explanation of all 4 Coffman conditions", "Clear understanding that breaking any single condition prevents deadlocks"],
        "cm": ["Listing Starvation or Livelock as one of the 4 conditions (they are related concepts, not Coffman conditions)", "Missing Circular Wait"],
        "fu": ["What is a Resource Allocation Graph (RAG) and how do cycles in it indicate deadlocks?", "What is Livelock and how does it differ from Deadlock?"],
        "tags": ["master-bank", "os", "deadlock", "coffman-conditions", "top-30"]
    },
    {
        "q": "What is CPU Scheduling in an Operating System? Explain preemptive versus non-preemptive scheduling.",
        "cat": "Operating Systems", "sub": "CPU Scheduling", "d": "Beginner", "type": "technical",
        "roles": ["Software Development Engineer", "Backend Developer", "Systems Engineer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "CPU Scheduling is the process by which the OS short-term scheduler (dispatcher) selects an executable process from the Ready Queue to allocate CPU execution time, maximizing CPU utilization and system responsiveness.\n\nKey Scheduling Metrics:\n- CPU Utilization: Percentage of time CPU is doing useful work (target: 40% - 90%).\n- Throughput: Number of processes completed per unit time.\n- Turnaround Time: Total time from process submission to completion.\n- Waiting Time: Total time a process spends waiting in the Ready Queue.\n- Response Time: Time from submission to first output response.\n\nPreemptive vs Non-Preemptive Scheduling:\n1) Preemptive Scheduling:\n- The OS kernel can forcibly interrupt (preempt) a currently running process before its burst finishes (e.g., when a higher-priority process arrives, or when a timer interrupt fires at the end of a time slice).\n- The running process is moved back to the Ready Queue.\n- Examples: Round Robin (RR), Shortest Remaining Time First (SRTF), Priority (Preemptive).\n- Pros: High responsiveness, prevents CPU starvation by long tasks. Cons: Context switch overhead and concurrency lock protection.\n\n2) Non-Preemptive Scheduling:\n- Once the CPU is allocated to a process, the process retains control until it voluntarily terminates or blocks on I/O.\n- Examples: First-Come First-Served (FCFS), Shortest Job First (SJF Non-preemptive).\n- Pros: Simple, minimal context switch overhead. Cons: Long tasks cause convoy effect, starving shorter interactive processes.",
        "kp": [
            "CPU Scheduling decides which ready process gets CPU allocation",
            "Preemptive: OS can forcibly interrupt running process (Round Robin, SRTF)",
            "Non-preemptive: process runs until voluntary termination or I/O block (FCFS, SJF)",
            "Evaluation metrics: Turnaround time, Waiting time, Response time, Throughput"
        ],
        "crit": ["Clear distinction between preemptive interruption vs non-preemptive voluntary surrender", "Accurate explanation of scheduling metrics"],
        "cm": ["Thinking non-preemptive processes can be interrupted by timer interrupts", "Confusing turnaround time with waiting time"],
        "fu": ["What is the Convoy Effect in CPU scheduling?", "What is Multi-Level Feedback Queue (MLFQ) scheduling?"],
        "tags": ["master-bank", "os", "cpu-scheduling", "preemption", "throughput", "top-30"]
    },
    {
        "q": "Explain the First-Come, First-Served (FCFS) CPU Scheduling algorithm and the Convoy Effect.",
        "cat": "Operating Systems", "sub": "CPU Scheduling Algorithms", "d": "Beginner", "type": "technical",
        "roles": ["Software Development Engineer", "Backend Developer", "Systems Engineer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "First-Come, First-Served (FCFS) is the simplest, non-preemptive CPU scheduling algorithm. Processes are assigned the CPU strictly in the order they arrive in the Ready Queue (managed via a FIFO queue).\n\nCharacteristics:\n- Non-preemptive: A process holds the CPU until its entire CPU burst completes.\n- Simple to implement: Enqueue incoming processes to a FIFO queue.\n- Unpredictable Waiting Time: Average waiting time is heavily dependent on the order of process arrival bursts.\n\nThe Convoy Effect:\nOccurs when a long, CPU-bound process arrives first, followed by several short, I/O-bound processes. The short processes must wait in the ready queue for the long CPU burst to finish. While the CPU-bound task executes, all I/O devices sit idle. When the CPU task finally finishes and blocks on I/O, all short processes rush through their CPU bursts quickly and block on I/O, leaving the CPU idle. This results in poor CPU and device utilization and severely inflated average waiting time.",
        "kp": [
            "Non-preemptive FIFO queue allocation",
            "Simple implementation, but suffers from high average waiting time",
            "Convoy Effect: short processes queue behind a massive CPU-bound task, stalling throughput"
        ],
        "crit": ["Clear, accurate description of FCFS queue mechanics", "Coherent explanation of the Convoy Effect and its impact on system utilization"],
        "cm": ["Assuming FCFS is preemptive", "Thinking FCFS provides optimal average waiting times"],
        "fu": ["How does Shortest Job First (SJF) solve the convoy effect problem of FCFS?"],
        "tags": ["master-bank", "os", "fcfs", "convoy-effect", "cpu-scheduling"]
    },
    {
        "q": "Explain Shortest Job First (SJF) and Shortest Remaining Time First (SRTF) Scheduling.",
        "cat": "Operating Systems", "sub": "CPU Scheduling Algorithms", "d": "Intermediate", "type": "technical",
        "roles": ["Software Development Engineer", "Backend Developer", "Systems Engineer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Shortest Job First (SJF) associates with each process the length of its next CPU burst. When the CPU becomes available, it is assigned to the process with the smallest CPU burst:\n\n1) Non-Preemptive SJF:\n- Once a process gets the CPU, it runs to completion.\n- Mathematically Optimal: SJF is proven to yield the minimal average waiting time among all scheduling algorithms.\n\n2) Preemptive SJF (Shortest Remaining Time First - SRTF):\n- If a new process arrives with a remaining CPU burst shorter than the currently running process's remaining time, the running process is preempted and returned to the ready queue.\n\nMajor Drawbacks:\n1) Starvation: Long processes can starve indefinitely if a continuous stream of short processes keeps arriving.\n2) Unpredictable Burst Times: In general-purpose OS kernels, it is impossible to know the exact length of a process's future CPU burst in advance (approximated via Exponential Smoothing: `tau_{n+1} = alpha * t_n + (1 - alpha) * tau_n`).",
        "kp": [
            "Selects process with shortest CPU burst time; mathematically minimizes average waiting time",
            "SRTF is the preemptive variant (preempts if incoming task has shorter remaining burst)",
            "Drawbacks: Starvation of long processes, and difficulty predicting future CPU bursts in practice"
        ],
        "crit": ["Proof that SJF minimizes average waiting time", "Clear distinction between non-preemptive SJF and preemptive SRTF", "Awareness of starvation and burst estimation limitations"],
        "cm": ["Claiming commercial operating systems use pure SJF (real OSs cannot know burst times in advance)"],
        "fu": ["How does Aging prevent starvation in priority and SJF scheduling?"],
        "tags": ["master-bank", "os", "sjf", "srtf", "cpu-scheduling", "starvation"]
    },
    {
        "q": "Explain Round Robin (RR) CPU Scheduling. How does time quantum selection impact performance?",
        "cat": "Operating Systems", "sub": "CPU Scheduling Algorithms", "d": "Intermediate", "type": "technical",
        "roles": ["Software Development Engineer", "Backend Developer", "Systems Engineer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Round Robin (RR) is a preemptive scheduling algorithm designed specifically for time-sharing and interactive multi-user operating systems:\n\nAlgorithm Mechanics:\n1) The ready queue is treated as a circular FIFO queue.\n2) A small unit of CPU time called a Time Quantum (or Time Slice, typically 10 to 100 milliseconds) is defined.\n3) The CPU scheduler allocates the CPU to the first process for up to one time quantum.\n4) If the process completes or blocks within the quantum, it releases the CPU voluntarily.\n5) If the process's burst exceeds the quantum, a timer interrupt fires. The process is preempted, its context saved, and it is placed at the tail of the ready queue. The CPU is dispatched to the next process.\n\nImpact of Time Quantum (Q) Selection:\n- Quantum is Extremely Large (Q -> infinity): Round Robin degenerates into First-Come First-Served (FCFS), leading to the Convoy Effect and poor interactive response time.\n- Quantum is Extremely Small (Q -> 0): Causes excessive context switching overhead. The CPU spends most of its clock cycles saving and restoring registers rather than executing application code (thrashing).\n- Rule of Thumb: The time quantum should be chosen such that approximately 80% of CPU bursts are shorter than the quantum, while keeping context-switching time under 1% of the quantum.",
        "kp": [
            "Preemptive time-sharing algorithm using circular queue and fixed time quantum (10-100ms)",
            "Guarantees fairness: no process waits more than (N-1) * Q time units",
            "Too large quantum -> degrades into FCFS (poor response time)",
            "Too small quantum -> excessive context-switching overhead and CPU thrashing"
        ],
        "crit": ["Clear trade-off analysis of time quantum size", "Fairness and starvation-free guarantees of Round Robin"],
        "cm": ["Assuming Round Robin produces the minimal average waiting time (SJF does, not RR)"],
        "fu": ["What is Completely Fair Scheduler (CFS) used in Linux kernels and how does it use virtual runtime (vruntime)?"],
        "tags": ["master-bank", "os", "round-robin", "time-quantum", "cpu-scheduling", "top-30"]
    },
    {
        "q": "What is Paging in Memory Management? Explain Page Tables and the Translation Lookaside Buffer (TLB).",
        "cat": "Operating Systems", "sub": "Memory Management & Paging", "d": "Intermediate", "type": "technical",
        "roles": ["Software Development Engineer", "Backend Developer", "Systems Engineer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Paging is a non-contiguous memory management scheme that eliminates external fragmentation by decoupling logical (virtual) memory from physical physical memory (RAM):\n\nKey Concepts:\n1) Pages & Frames:\n- Physical RAM is divided into fixed-size blocks called Frames (typically 4KB).\n- Logical Address Space of a process is divided into equal-sized blocks called Pages (4KB).\n\n2) Address Translation:\n- A CPU-generated logical address consists of: Page Number (p) and Page Offset (d).\n- The Memory Management Unit (MMU) uses `p` as an index into the process's Page Table to find the corresponding physical Frame Number (f).\n- Physical Address = (Frame Number f * Frame Size) + Offset d.\n\n3) Translation Lookaside Buffer (TLB):\n- Accessing the page table in RAM adds memory lookup latency (doubling memory access time).\n- The TLB is a high-speed associative hardware cache inside the CPU that stores recent `Page -> Frame` translations.\n- TLB Hit: Translation found in hardware in ~1 clock cycle.\n- TLB Miss: MMU reads page table from RAM, updates TLB, and resumes (takes ~50-100ns).\n\n4) Advantages & Disadvantages:\n- Pros: Completely eliminates external fragmentation; pages can be loaded anywhere non-contiguously in physical RAM.\n- Cons: Suffers from Internal Fragmentation (if the last page of a process requires only 100 bytes, the remaining 3996 bytes in the 4KB frame are wasted); page table memory overhead.",
        "kp": [
            "Physical memory = Frames; Logical memory = Pages (both fixed size, typically 4KB)",
            "Page Table translates Page Number (p) to physical Frame Number (f)",
            "TLB (Translation Lookaside Buffer) is a CPU hardware cache that accelerates page translations",
            "Eliminates external fragmentation; minor internal fragmentation on last page"
        ],
        "crit": ["Accurate mathematical breakdown of logical to physical address translation using offset", "Understanding TLB hit ratio and its impact on effective memory access time"],
        "cm": ["Confusing Internal Fragmentation (within fixed 4KB page) with External Fragmentation", "Thinking pages and frames have different sizes (they MUST be identical)"],
        "fu": ["What is a Multi-Level Page Table and why is it necessary for 64-bit address spaces?", "What is an Inverted Page Table?"],
        "tags": ["master-bank", "os", "paging", "page-tables", "tlb", "memory-management", "top-30"]
    },
    {
        "q": "What is Segmentation in Operating Systems? How does it differ from Paging?",
        "cat": "Operating Systems", "sub": "Memory Management", "d": "Intermediate", "type": "technical",
        "roles": ["Software Development Engineer", "Backend Developer", "Systems Engineer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Segmentation is a memory management scheme that divides a program's logical address space into variable-sized logical units reflecting the programmer's view of software (e.g., Code segment, Global data segment, Heap segment, Stack segment, Subroutines).\n\nLogical Address in Segmentation:\nConsists of a pair: `<Segment Number (s), Offset (d)>`.\nThe Segment Table maps the segment number to a Base Address (physical starting memory address) and Limit (length of the segment). If `Offset >= Limit`, a trap/segmentation fault is raised by the MMU.\n\nPaging vs Segmentation Comparison:\n1) Block Size: Paging uses fixed-size blocks (e.g., 4KB); Segmentation uses variable-sized blocks corresponding to program modules.\n2) Programmer Visibility: Paging is invisible to the programmer (managed transparently by hardware and OS); Segmentation reflects logical user-defined modules.\n3) Fragmentation: Paging suffers from internal fragmentation, but eliminates external fragmentation; Segmentation suffers from external fragmentation (free memory holes between segments).\n4) Address Space: Paging uses a single 1D linear address (`p + d`); Segmentation uses a 2D address (`segment_number + offset`).\n\nModern Hybrid Architecture: Modern OSs (Linux, Windows x86) combine both: Segmented Paging. Logical segments are subdivided into fixed-size pages, combining the logical modularity of segmentation with the zero-external-fragmentation benefits of paging.",
        "kp": [
            "Segmentation divides memory into variable-sized logical units (Code, Stack, Heap, Data)",
            "Segment Table contains Base address and Limit length to prevent boundary violations",
            "Paging = fixed-size, invisible, internal fragmentation; Segmentation = variable-size, visible, external fragmentation",
            "Modern x86 systems combine both into Segmented Paging"
        ],
        "crit": ["Clear comparison table across block size, visibility, and fragmentation types", "Accurate explanation of Segment Base and Limit registers"],
        "cm": ["Believing Paging causes external fragmentation", "Thinking Segmentation divides memory into fixed 4KB blocks"],
        "fu": ["What is a Segmentation Fault and what causes the hardware MMU to trigger it?", "How does compaction resolve external fragmentation in segmentation?"],
        "tags": ["master-bank", "os", "segmentation", "paging", "memory-management"]
    },
    {
        "q": "Explain Virtual Memory, Demand Paging, and Page Faults in Operating Systems.",
        "cat": "Operating Systems", "sub": "Virtual Memory", "d": "Intermediate", "type": "technical",
        "roles": ["Software Development Engineer", "Backend Developer", "Systems Engineer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Virtual Memory is an abstraction provided by the OS and hardware MMU that gives each process the illusion of having a vast, contiguous address space (e.g., 128TB in 64-bit systems), often vastly exceeding the physical RAM available.\n\nDemand Paging ('Lazy Loading'):\nInstead of loading the entire 2GB program into RAM when launched, pages are loaded into physical frames only when referenced by CPU instructions.\n\nPage Fault Handling Sequence:\n1) CPU references a virtual address whose page table entry has the Valid/Invalid bit set to `0` (Invalid / Not in RAM).\n2) The MMU traps to the OS kernel: a Page Fault Interrupt is generated.\n3) The OS pauses the process and locates the missing page in secondary storage (Swap Space / Pagefile on SSD/Disk).\n4) The OS finds a free physical frame in RAM. (If no frame is free, a Page Replacement Algorithm like LRU evicts a victim page; if dirty, writes to disk).\n5) The OS reads the requested page from disk into the allocated physical frame.\n6) The OS updates the process's page table entry with the new frame number and sets valid bit to `1`.\n7) The OS resumes the interrupted instruction seamlessly as if the page was always in RAM.\n\nThrashing: If a system does not have enough physical RAM to hold the working sets of all active processes, the OS spends virtually 100% of its time swapping pages in and out of disk rather than executing instructions.",
        "kp": [
            "Virtual memory gives processes the illusion of large contiguous address space independent of physical RAM size",
            "Demand Paging loads pages into physical RAM only upon reference",
            "Page Fault: CPU references page not currently in RAM, triggering OS kernel to load it from disk",
            "Thrashing: excessive page swapping that collapses CPU throughput"
        ],
        "crit": ["Accurate, step-by-step description of the 7-step page fault handling sequence", "Clear definition of Thrashing and working set models"],
        "cm": ["Assuming a page fault is a fatal application crash (page faults are standard OS lazy-loading mechanisms)", "Ignoring the dirty bit during page replacement"],
        "fu": ["What is the Least Recently Used (LRU) page replacement algorithm?", "What is Belady's Anomaly in FIFO page replacement?"],
        "tags": ["master-bank", "os", "virtual-memory", "demand-paging", "page-fault", "thrashing", "top-30"]
    },
    {
        "q": "What is the difference between RAM and ROM?",
        "cat": "Operating Systems", "sub": "Hardware & Memory Architecture", "d": "Beginner", "type": "technical",
        "roles": ["Software Development Engineer", "Support Engineer", "Hardware / IoT Engineer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "RAM (Random Access Memory) and ROM (Read-Only Memory) are primary memory technologies with fundamentally different volatility, operations, and architectural roles:\n\n1) RAM (Random Access Memory):\n- Volatility: Volatile memory. Requires continuous electrical power to maintain data; all data is lost instantly when power is turned off or computer reboots.\n- Operations: Read and Write capability at ultra-high speeds (nanoseconds).\n- Purpose: Serves as the primary working memory holding the active OS kernel, running program processes, open documents, and dynamic allocations.\n- Types: DRAM (Dynamic RAM, used for main system RAM, requires periodic refresh capacitors) and SRAM (Static RAM, faster, used for CPU L1/L2/L3 caches).\n\n2) ROM (Read-Only Memory):\n- Volatility: Non-volatile memory. Retains data permanently even when the system is completely powered down.\n- Operations: Primarily Read-only during normal operation; writing requires special flashing procedures.\n- Purpose: Stores permanent, immutable firmware instructions necessary to bootstrap the hardware upon power-on (BIOS / UEFI, firmware microcode, bootloader).\n- Types: PROM, EPROM, EEPROM (Electrically Erasable PROM, used in modern flash BIOS).",
        "kp": [
            "RAM: Volatile (loses data on power loss), high-speed Read/Write, stores active OS and running programs (DRAM/SRAM)",
            "ROM: Non-volatile (permanent data retention), Read-only, stores BIOS/UEFI bootstrap firmware (EEPROM/Flash)",
            "RAM is temporary working space; ROM is permanent bootstrap instruction storage"
        ],
        "crit": ["Clear, accurate comparison across volatility, operations, speed, and functional purpose"],
        "cm": ["Confusing ROM with secondary storage like SSDs/Hard Disks", "Thinking RAM retains data after system restart"],
        "fu": ["What is the difference between SRAM and DRAM in terms of speed and physical construction?", "What is the bootstrap loader and how does BIOS hand over execution to the OS kernel?"],
        "tags": ["master-bank", "os", "hardware", "ram", "rom", "memory"]
    },
    {
        "q": "What is the difference between Stack Memory and Heap Memory?",
        "cat": "Operating Systems", "sub": "Memory Management & Execution", "d": "Beginner", "type": "technical",
        "roles": ["Software Development Engineer", "Backend Developer", "Python Developer", "Java Developer"],
        "stages": ["Technical Screening", "Technical"],
        "ans": "Both Stack and Heap are regions within a process's virtual memory address space, but operate under completely different allocation paradigms:\n\n1) Stack Memory:\n- Allocation: Automatic allocation and deallocation by the CPU hardware as functions are called and return (LIFO - Last In, First Out).\n- Contents: Stores function call frames, local primitive variables, parameter arguments, and return memory addresses.\n- Speed: Extremely fast. Allocation merely increments or decrements the CPU Stack Pointer register.\n- Size: Fixed, relatively small size (typically 1MB to 8MB per thread). Exceeding it causes a `StackOverflowError` (e.g., infinite recursion).\n- Thread Safety: Private to each individual thread; no synchronization locks needed.\n\n2) Heap Memory:\n- Allocation: Manual or dynamic runtime allocation via language runtime / allocator (`malloc()`, `new`, object instantiation).\n- Contents: Dynamically sized objects, arrays, and complex data structures whose lifetime extends beyond the scope of a single function.\n- Deallocation: Must be manually freed (C/C++ `free()`, `delete`) or automatically collected by a Garbage Collector (Java, Python, Go). Failure to release causes Memory Leaks.\n- Speed: Slower. Requires searching free memory lists, handling fragmentation, and thread synchronization.\n- Size: Large, limited only by physical RAM and virtual memory space. Exceeding it causes an `OutOfMemoryError`.\n- Thread Safety: Shared across all threads in the process; requires mutexes or synchronized locks to prevent race conditions.",
        "kp": [
            "Stack: Automatic LIFO, fast pointer manipulation, stores locals/call frames, thread-private, small fixed size (StackOverflow)",
            "Heap: Dynamic runtime allocation, slower, stores complex objects, thread-shared, large size (OutOfMemory / Memory Leaks)",
            "Stack deallocates automatically on function return; Heap requires manual free or Garbage Collector"
        ],
        "crit": ["Systematic comparison across allocation mechanics, speed, lifetime, scope, and error types", "Understanding thread privacy on Stack vs shared access on Heap"],
        "cm": ["Believing heap memory deallocates automatically when a function finishes execution", "Confusing the Stack memory segment with the Stack Abstract Data Type (ADT)"],
        "fu": ["What is a Memory Leak and how do tools like Valgrind detect unreferenced heap memory?", "What is Escape Analysis in JIT compilers that allows heap objects to be allocated on the stack?"],
        "tags": ["master-bank", "os", "stack-vs-heap", "memory-management", "top-30"]
    }
]


def run():
    with SessionLocal() as db:
        existing_rows = db.scalars(select(Question)).all()
        hash_to_question = {row.question_hash: row for row in existing_rows}
        id_to_question = {row.id: row for row in existing_rows}

        created = 0
        updated = 0

        for item in CURATED_QUESTIONS:
            q_text = item["q"]
            h = question_fingerprint(q_text)
            tags = list(item.get("tags", []))

            if h in hash_to_question:
                row = hash_to_question[h]
                merged_tags = list(dict.fromkeys(list(row.tags or []) + tags))
                row.tags = merged_tags
                row.reference_answer = item["ans"]
                row.key_points = item["kp"]
                row.evaluation_criteria = item["crit"]
                row.common_mistakes = item["cm"]
                row.follow_up_questions = item["fu"]
                row.subcategory = item["sub"]
                row.difficulty = item["d"]
                row.category = item["cat"]
                row.question_type = item["type"]
                updated += 1
                log.info(f"Updated existing question: {row.id} - {q_text[:40]}")
            else:
                cat_slug = item["cat"].lower().replace("&", "").replace(",", "").replace(" ", "-")[:4]
                sub_count = sum(1 for qid in id_to_question if qid.startswith(f"cur-{cat_slug}"))
                new_id = f"cur-{cat_slug}-{sub_count + 1:03d}"

                while new_id in id_to_question:
                    sub_count += 1
                    new_id = f"cur-{cat_slug}-{sub_count + 1:03d}"

                new_row = Question(
                    id=new_id,
                    question=q_text,
                    question_hash=h,
                    category=item["cat"],
                    subcategory=item["sub"],
                    difficulty=item["d"],
                    question_type=item["type"],
                    target_roles=item["roles"],
                    interview_stage=item["stages"],
                    reference_answer=item["ans"],
                    key_points=item["kp"],
                    evaluation_criteria=item["crit"],
                    common_mistakes=item["cm"],
                    follow_up_questions=item["fu"],
                    tags=tags,
                    is_active=True,
                )
                db.add(new_row)
                id_to_question[new_id] = new_row
                hash_to_question[h] = new_row
                created += 1
                log.info(f"Created new question: {new_id} - {q_text[:40]}")

        db.commit()
        print(f"Custom Curated Seeding Completed! Created: {created}, Updated: {updated}")


if __name__ == "__main__":
    run()
