# Ticketing
Server-Clinet ticketing program

# PreRequirements
python 2.7
mysql

# Requirements
Tornado

Torndb

MySQL-Python

# Install

## Step1 : Create "ticketing" database in MySQL

Connect to MySQL as a superuser:

```shell
$ mysql -u root -p
```
    
Create a database named "ticketing":
    
```shell
mysql> CREATE DATABASE ticketing;
```
    
Create a user named "tick" with password "tick":
    
```shell
mysql> CREATE USER 'tick'@'localhost' IDENTIFIED BY 'tick';
```
and exit MySQL:

```shell
mysql> exit
```

## Step2 : Import "ticketing" database and grant premissions to "tick" user:

Import db.sql by running this command:

```shell
$ mysql -u root -p ticketing < PATHTOFILE/db.sql
```
Start MySQL as super user and run this command:

```shell
mysql> GRANT ALL PRIVILEGES ON ticketing.* TO 'tick'@'localhost';
```

## Step3: Run server and client code:

Start server by running this command:

```shell
$ python PATHTOFILE/server.py
```

In another terminal start client:

```shell
$ python PATHTOFILE/client.py
```

## Preview:

### Part 1:
![GET GIF](http://up.vbiran.ir/uploads/8998155568203426603_part1.gif)

### Part 2:
![GET GIF](http://up.vbiran.ir/uploads/35590155568202735501_part2.gif)
