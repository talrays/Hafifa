# Data Engineering Onboarding & Learning Plan

Welcome to Optimus! This repository is designed to guide you through a set of topics and exercises to get you up to speed with essential concepts and tools. Each section contains learning material, links to external resources, and practical exercises. The goal is for you to complete this onboarding program within a specific timeline while also engaging with the hands-on exercises.

---

## Submitting Your Exercises

1. Fork this repository to your own GitHub account.
2. Clone your fork locally:  
   `git clone <your-fork-url>`
3. Work on the exercises in their respective folders.
4. Work on a separate branch for each exercise.
5. When you're ready, create a pull request for an exercise and inform your superior for a CR.
6. The pull request should be to your forked repository.

---

## Questions and Support

If you have any questions or need support, feel free to reach out to your supervisor.

Happy learning!🤍

---

## Table of Contents
- [Data Engineering Onboarding \& Learning Plan](#data-engineering-onboarding--learning-plan)
  - [Submitting Your Exercises](#submitting-your-exercises)
  - [Questions and Support](#questions-and-support)
  - [Table of Contents](#table-of-contents)
  - [1. Git](#1-git)
  - [2. Clean Code](#2-clean-code)
  - [3. Web Scraping](#3-web-scraping)
  - [4. Threading and MultiProcessing](#4-threading-and-multiprocessing)
  - [5. Databases](#5-databases)
  - [6. SQL](#6-sql)
  - [7. Building API](#7-building-api)
  - [8. Testing](#8-testing)
  - [9. Useful Python Libraries](#9-useful-python-libraries)
  - [10. Advanced Python](#10-advanced-python)
  - [11. Rolling Exercise](#11-rolling-exercise)
  - [12. Data Engineering](#12-data-engineering)
  - [13. Kafka🩷](#13-kafka)
  - [14. Streaming](#14-streaming)
  - [15. Splunk](#15-splunk)
  - [16. Data Warehouse \\ Data Lake](#16-data-warehouse--data-lake)
  - [17. Trino](#17-trino)
  - [18. Airflow](#18-airflow)
   
---

## 1. Git

### Duration: 1 Day

**Learning Material**:  
- Interactive Git learning: [Learn Git Branching](https://learngitbranching.js.org/)

**Notes**:  
- **Do not** cover the following topics:
  - Main: "Advanced Topics"
  - Remote: "To Origin And Beyond -- Advanced Git Remotes!"

---

## 2. Clean Code

### Duration: 1 Day

**Reference Material**:  
- [Clean Code Python](https://github.com/zedr/clean-code-python)  
This github page includes Python best practices to write clean and maintainable code.

**Exercise**:  
- In the `clean_code/` folder in this project, you will find a `main.py` file that requires refactoring. Apply the principles described in the reference material to improve the code quality.

---

## 3. Web Scraping

### Duration: 1 Day

**Exercise**:  
In the `web_scraping/` folder, there is an exercise with instructions to perform web scraping on a websites.

---

## 4. Threading and MultiProcessing

### Duration: 2 Days

**Learning Material**:  
- [Practical Guide to Asyncio, Threading & Multiprocessing](https://itnext.io/practical-guide-to-async-threading-multiprocessing-958e57d7bbb8)
- [Multiprocessing VS Threading VS AsyncIO in Python](https://leimao.github.io/blog/Python-Concurrency-High-Level/)

**Exercise**:  
There is an exercise in the `threading_multiprocessing/` folder where you'll need to implement a multi-threaded solution to process data efficiently. Follow the instructions provided in the folder.

---

## 5. Databases

### Duration: 1 Day

**Learning Material**:

#### 5.1. PostgreSQL
A tutorial on postgreSQL (We know you've learnt it already, but go over it quickly)
- [Postgresql Tutorial](https://www.w3schools.com/postgresql/postgresql_exercises.php)

#### 5.2. MongoDB
- [Mongo Interactive Tutorial](https://www.mongodb.com/docs/manual/tutorial/getting-started/)
- [Excersice](https://www.w3resource.com/mongodb-exercises/) - do 5 random exercises 

#### 5.3. S3
Quick overview about s3
- [S3 Guide](https://youtu.be/tfU0JEZjcsg?si=ch-W6mPULHn79Ars)

#### 5.4. Redis
Introduction to Redis and learning the syntax
- [Redis Introduction](https://youtu.be/G1rOthIU-uo?si=jhEWzfj59GZrHBg7)
- [Redis Beginers' Guide](https://daily.dev/blog/redis-basics-for-new-developers)

---

## 6. SQL

### Duration: 5 hours

- [SQL Challenge](https://mystery.knightlab.com/)
- [More SQL](https://leetdata.ai/problems) - do 5 problems in each difficulty 

---

## 7. Building API

### Duration: 0.5 Day

**Learning Material**:

#### 7.1. FastAPI
- [FastAPI Explanation](https://youtu.be/iWS9ogMPOI0?si=HPv_xetY7HGfOxPK)
- [FastAPI Syntax Guide](https://fastapi.tiangolo.com/tutorial/first-steps/)

**Notes**:  
- **Only** cover the following topics:
  - From "First Steps" to "Request Body"
  - "Handling Errors"
  - "Debugging"

#### 7.2. SQLAlchemy
- [SQLAlchemy Documentation](https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_introduction.htm)

---

## 8. Testing

### Duration: 0.5 Days

**Learning Material**:
- [Beginers' Guide to Python Testing](https://medium.com/@sachinsoni600517/unit-testing-in-python-a-comprehensive-guide-for-beginners-985eec71bb4d)
- [Pytest Documentation](https://docs.pytest.org/en/stable/)
- [Mocking in Python](https://medium.com/@moraneus/the-art-of-mocking-in-python-a-comprehensive-guide-8b619529458f)

---

## 9. Useful Python Libraries

### Duration: 1 Day

- [NumPy Cheat Sheet](https://www.dataquest.io/cheat-sheet/numpy-cheat-sheet/)
- [NumPy Exercises](https://www.w3schools.com/python/numpy/default.asp)
- [Pandas Tutorial](https://www.w3schools.com/python/pandas/default.asp)

---

## 10. Advanced Python

### Duration: 7 hours

 - [Generators](https://realpython.com/introduction-to-python-generators/)
 - [Decorators](https://realpython.com/primer-on-python-decorators/)
 - [Context Manager](https://realpython.com/python-with-statement/)
 - [Iterators](https://www.geeksforgeeks.org/python/iterators-in-python/)
 - [Profiling](https://www.geeksforgeeks.org/python/memory-profiling-in-python-using-memory_profiler/)
 - [Garbage Collection](https://www.geeksforgeeks.org/python/garbage-collection-python/)
 - [Memory Management](https://www.geeksforgeeks.org/python/memory-management-in-python/)
 - [Tips](https://www.geeksforgeeks.org/python/optimization-tips-python-code/)

---

## 11. Rolling Exercise

### Duration: 5 Days

There is an exercise in the `rolling_exercise/` folder where you'll need to build an API. Follow the instructions provided in the folder.

---
# Before the next section please do the Newbies training - DevOps section in the TS
---

## 12. Data Engineering

### Duration: 1 Hour

**DE Explanation**

- [DE Introduction](https://docs.google.com/document/d/1ZOsylqaWftkHFjnqHi_d3As8c_ifI8EOHQZhfscUdGo/edit?tab=t.0#heading=h.udg0q6xlt4mv)
- [DE Introduction Video](https://www.youtube.com/watch?v=qWru-b6m030)
If you feel that you don't understand it enough, you are more than welcome to read more about it.

---

## 13. Kafka🩷

### Duration: 4 hours

- [Kafka Introduction](https://www.youtube.com/watch?v=Ch5VhJzaoaI&t=284s)
- [Get To Know the Terms](https://kafka.apache.org/intro#)
- [Zookeeper](https://docs.conduktor.io/learn/fundamentals/zookeeper)
- [Clean Up Policies](https://medium.com/apache-kafka-from-zero-to-hero/apache-kafka-guide-20-log-cleanup-policies-e739cdc91bd8)
- [Segments](https://docs.conduktor.io/learn/advanced/topics/internals-segments-indexes)
- [KRaft](https://docs.conduktor.io/learn/fundamentals/kraft-mode)

---

## 14. Streaming

### Duration: 3 Hours

- [What is streaming](https://www.oreilly.com/radar/the-world-beyond-batch-streaming-101/)
- [RocksDB](https://getstream.io/blog/rocksdb-fundamentals/)
- [CDC](https://luminousmen.com/post/change-data-capture)
- [Kafka Streams option 1](https://www.instaclustr.com/blog/kafka-streams-guide/) - optional
- [Kafka Streams option 2](https://www.baeldung.com/java-kafka-streams) - optional
- [Kafka Streams official tutorial](https://kafka.apache.org/documentation/streams/) - optional
- [What is Faust](https://medium.com/data-science/stream-processing-with-python-kafka-faust-a11740d0910c) - optional
- [Official Docs Faust](https://faust.readthedocs.io/en/latest/) - optional

Kafka Streams is the most popular library for streaming developing. However Kafka Streams a java library.
There is an implementation of Kafka Streams in python named Faust. And yet Faust does not have all the abilities of Kafka Streams and it is not as production ready as Kafka Streams. 
  
---

## 15. Splunk

### Duration: 1 Hour

- [Splunk Introduction and Cheat Sheet](https://www.stationx.net/splunk-cheat-sheet/)
- [Basic Splunk Searching](https://www.youtube.com/watch?v=GWl-TuAAF-k&t=102s)
- [Creating a Splunk Dashboard](https://www.youtube.com/watch?v=uQUAvY5M3RU)

---

## 16. Data Warehouse \ Data Lake

### Duration: 2 Days

### OLAP VS OLTP
- [OLAP vs OLTP](https://youtu.be/iw-5kFzIdgY?si=do71e86y3TqNCbxQ)
- [More on OLAP vs OLTP](https://www.geeksforgeeks.org/dbms/difference-between-olap-and-oltp-in-dbms/)
- [Databases vs Datawarehouses vs Datalakes](https://youtu.be/-bSkREem8dM?si=CfTmfdbV9wja5BWS)
- [More On Data Lake VS Warehouse](https://luminousmen.com/post/data-lake-vs-data-warehouse/#data-warehouse/)
- [Data lakehouse](https://arxiv.org/abs/2310.08697v1) - optional

### File Formats
- [Big Data File Formats](https://www.upsolver.com/blog/the-file-format-fundamentals-of-big-data)
- [Avro File Format](https://sqream.com/blog/a-detailed-introduction-to-the-avro-data-format/)
- [ORC File Format](https://www.youtube.com/watch?v=IX5ElplseUY)
- [Why Parquet](https://luminousmen.substack.com/p/why-parquet-is-the-go-to-format-for?utm_source=cross-post&publication_id=1936637&post_id=163835393&utm_campaign=1930705&isFreemail=true&r=57ujs9&triedRedirect=true)
- [Parquet File](https://youtu.be/1j8SdS7s_NY?si=HOXHepdPRATRnjNm)
- [Schema Evolution](https://www.linkedin.com/pulse/schema-evolution-avro-orc-parquet-detailed-approach-aniket-kulkarni-z7zpf/)

### Open Table Formats
- [Hive Introduction](https://youtu.be/cMziv1iYt28?si=chzEEPKILW-2Ovow)
- [Iceberg Introduction](https://youtu.be/TsmhRZElPvM?si=V8tvEUZhRCEIlq8G)
- [How Iceberg Stores Data](https://youtu.be/xfAYLAFCLvM?si=mgZocoUYGFJo9CKp)
- [Another intro to iceberg](https://vutr.substack.com/p/i-spent-8-hours-learning-apache-iceberg)
- [Streaming with iceberg](https://www.ryft.io/blog/streaming-with-apache-iceberg-the-operational-problems-at-scale)
- [Detailed talk on iceberg](https://www.youtube.com/watch?v=kJaD0WuQ1Bg) - optional

### Data Partitioning
- [More on Partitioning](https://vutr.substack.com/p/partitioning-and-clustering?utm_source=post-email-title&publication_id=1930705&post_id=166732941&utm_campaign=email-post-title&isFreemail=true&r=57ujs9&triedRedirect=true&utm_medium=email)
- [How not to partition data](https://luminousmen.substack.com/p/how-not-to-partition-data-in-s3-and)


### Other
- [Apache Arrow](https://youtu.be/R4BIXbfKBtk?si=-HrXgui3LkQA61Om)

---

## 17. Trino

### Duration: 0.5 Hour

- [Trino Introduction](https://www.youtube.com/watch?v=SKNJObdGCsY)
- [Trino Concepts](https://trino.io/docs/current/overview/concepts.html)

---

## 18. Airflow

### Duration: 4 hours

- [All About Airflow](https://medium.com/@sumitmudliar/beginners-guide-to-apache-airflow-4827c3f4bfe4)
- [Practical Overview Of Airflow UI](https://youtube.com/playlist?list=PLcoE64orFoVsyzbvfgiY5iNKo30fJ4IWm&si=ZiouDEBaXTZCMRNA)
  
