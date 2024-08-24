# Description
We are intending to develop a possible database similar to what would be needed if you were a 
Lego manufacturing facility or storage location. Lego does not usually sell in piece by piece but 
in different building kits, intended to be assembled by the end user. This means that we, as the 
provider need to assemble all the different pieces of the many different kits before shipping them 
to the customer. That means that we need to have an exact count of every piece and know 
exactly what the different kits require. 

## ER Models
See figure 1
![Figure 1](./figures/Lego.png)

## SQL Queries

## Changelog

| Name| Change Description| Date|
|:----|:------------------|:----|
| Sofia Blom | Setup devcontainer for Python and SQL development | 2024-04-09 |
| Sofia Blom | First attempt at a ER-diagram for the project | 2024-04-12 |
| Sofia Blom | Got flask to display an html template | 2024-05-09 |
| Sofia Blom & Ninni Salomonsson | Created sql files for createing and populating tables | 2024-05-15 |
| Sofia Blom | Frontpage form working with database |2024-08-07|

## Other
There are several things to take note of here. Firstly is that the application has no security what so ever. Secondly is that all the input fields have no limits on the html end meaning that the user could input any number or any length of string and it would be passed on to the python code. This of course means that we can input zero or negative numbers, somewhat breaking things. If we ever are unable to complete a SQL command that contains user given information we print an error in the console and perform a rollback on the transaction. It is still possible to order a negative amount of Lego Sets. This could be interprited as a return order, and it is handeled correctly by the triggers. To ensure that a user is only able to input correctly formated information would involve more html and python and would not contribute towards the functionality of the database. Because of this it was deemed out of scope for this assignment. 

### Github access
The repository can be found [here](https://github.com/s02blom/LegoWebStore/). 