# Description
We are intending to develop a possible database similar to what would be needed if you were a 
Lego manufacturing facility or storage location. Lego does not usually sell in piece by piece but 
in different building kits, intended to be assembled by the end user. This means that we, as the 
provider need to assemble all the different pieces of the many different kits before shipping them 
to the customer. That means that we need to have an exact count of every piece and know 
exactly what the different kits require. 

## ER Models
See figure 1
There is several things we can take away from the description of the buissness we are modeling. 

Firstly is desciption of the Lego Set's and Lego Bricks. Several different Lego Bricks make up the one Lego Set and Lego Brick are themselves never sold. We chose to model the Lego Set and the Lego Bricks as seen in the [ER-diagram](#er---diagram). It is rare that a Lego Set only contains one of a single type of Lego Brick, so to properly model the relationship we need to add a quantity. To more closely model reality we also made the Storage Location table. One noteworthy choice was made here, to store the quantity of Lego Bricks that were avilable in storage in the Storage Location table. It seperates the different tables into two different categories, Lego Brick which deals in hypothetical descriptins of a Lego Brick and Storage Location who has lots of information about the real world such as where it's located and how much is in it. 

Secondly is that we are in fact some kind of business, and there for we need to keep track of what we sell, to whom a where to ship the goods. To that end we need one table to keep track of the orders and another to know who the customer is. In this chase we decide that we were not an end retailer, but rather some middle man, meaning our hypothetical customers were other businesses. The Orders has to contain Lego Sets as that is the only thiing we sell. 

As we can see from the quantifiers in the [ER-diagram](#er---diagram) most of the tables has a many to one or a many to many relation to one another. This means that we will have to create several helping tables to keep track. Detailed in the [Schema](#schema), we can see Lego Set Content and Order content primarily are here to help. This comes with the bonus that we can add the attribute quantity as detailed in the Lego Brick - Lego Set relation and added in the Order - Lego Set relation to better store data and model reality. The somewhat unexpected addition here is the Shipping Adress entity. An address has a lot of different parts to them and are often very different in different countries. If this were a propper business we would have to do a lot of work with the adress to figure out the best shipping routes and times and then it sould be benificial to have it as a seperate data structure. 

### ER - diagram
![Figure 1](./figures/ER-diagram.png)


### Schema
![Figure 2](./figures/Schema.png)


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