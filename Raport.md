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
| Sofia Blom | Add trigger for totalling the sum in Order table | 2024-07-17 |
| Sofia Blom | Frontpage form working with database |2024-08-07|
| Sofia Blom | Add tables to Admin page | 2024-08-19 |
| Sofia Blom | Add forms to Admin page | 2027-08-19 |
| Sofia Blom | Trigger for removing lego bricks when ordering lego sets | 2024-08-22 |
| Sofia Blom & Ninni Salomonsson | Function for checking whether we have enought Lego Bricks to make that Lego Set | 2024-08-23 |

## Other

### Github access
The repository can be found [here](https://github.com/s02blom/LegoWebStore/). 