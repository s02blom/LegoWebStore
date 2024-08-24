# Description
We are intending to develop a possible database similar to what would be needed if you were a 
Lego manufacturing facility or storage location. Lego does not usually sell in piece by piece but in different building kits, intended to be assembled by the end user. This means that we, as the provider need to assemble all the different pieces of the many different kits before shipping them to the customer. That means that we need to have an exact count of every piece and know exactly what the different kits require. 

## ER Models
See figure 1
![Figure 1](./figures/Lego.png)

## SQL Queries

### Admin page

On the admin page we display a lot of differet data. We are for example displaying all the orders that has been placed on the Lego Web Store. To get all the orders and it's related relevant data, we use this select statement: 
```
SELECT `Order`.id, `Order`.TotalSum, `Order`.Customer, ShippingAdress.StreetAdress, ShippingAdress.PostCode, ShippingAdress.City, `Order`.OrderDate, `Order`.ShippingDate, `Order`.ArrivalDate
    FROM `Order`
    CROSS JOIN ShippingAdress ON `Order`.ShippingAdress = ShippingAdress.id
```
With this statement we get the Order ID, Total Sum, Customer ID, Shipping Adress, Post Code, City, Order Date, Shipping Date and Arrival Date for every order. Of course it would have been easier to solely display all the data that's available in the `Order` table and nothing else. But then we would be missing some valuble and relavant information for the orders. That's why we also want to get some data from the related `ShippingAdress` table. We want the `StreetAdress`, `PostCode` and the `City` from the `ShippingAdress` table. To correctly align the two tables; `Order` and `ShippingAdress`, we use `CROSS JOIN` on the shipping adress id, which is a value that both tables contains (`Order.ShippingAdress` for the `Order` table, and `ShippingAdress.id` for the `ShippingAdress` table). 

Aside from that select statement above, we also have a query that looks like this, on both the front page and admin page:  
```
SELECT * from LegoSet WHERE CheckAvailability(LegoSet.id) = True;
```
This statement is used to displays all the available Lego sets at that moment. We use almost the same query for displaying all the unavailable Lego sets; but instead of `CheckAvailability(LegoSet.id) = True`, the unavailable Lego sets is displayed using `CheckAvailability(LegoSet.id) = False` insted. `CheckAvailability` is a function we created ourselves, because we needed a way to check whether our LegoSets were available for purchase or not.

### CheckAvailability
```
DROP FUNCTION IF EXISTS CheckAvailability;

CREATE FUNCTION CheckAvailability (legoSetId INT)
RETURNS BOOLEAN DETERMINISTIC
BEGIN
	DECLARE available BOOLEAN DEFAULT TRUE;
    DECLARE lSet, LBrick, requiredLegoBricks, availableLegoBricks INT;
    DECLARE done INT DEFAULT FALSE;
    DECLARE cursorSetContent CURSOR FOR SELECT * FROM LegoSetContent WHERE LegoSet = legoSetId;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cursorSetContent;
    
    LegoBricksLoop: LOOP
        FETCH cursorSetContent into lSet, LBrick, requiredLegoBricks;
        IF done THEN
            LEAVE LegoBricksLoop;
        END IF;

        SELECT StorageLocation.Quantity INTO availableLegoBricks
            FROM LegoBrick
            CROSS JOIN StorageLocation ON LegoBrick.StorageLocation = StorageLocation.ID
            WHERE LegoBrick.id = LBrick;
        IF availableLegoBricks < requiredLegoBricks THEN
            SET available = FALSE;
            SET done = True;
        END IF;
    END LOOP;
    CLOSE cursorSetContent;
    RETURN available;
END
```
`CheckAvailability` first started out as a procedure that Sofia created. But after trying to use the procedure for the front page, we realised that we had to make it into a function insted. So Ninni translated it into a function, which is the function you see above.

`CheckAvailability` takes one Lego Set Id as input, and returns a boolean. The function returns True if that Lego Set has all the Lego pieces it needs in stock, in other words, it's available for purchase. Otherwise the function will return False, meaning that there are not enough piece instock for that Lego set.

Because our system uses several tables that are connected to eachother, we need to go deeper when we want to reach for example the in stock quantity of a specific Lego brick. In order to be able to do that in our function we had to declare a cursor that we could use. The cursor selects everything from `LegoSetContent` that has the same Lego set id as the input for the fucntion. Then we use a loop to go through all the different Legobricks needed for that Lego set. In the begining of each loop we fetch all the information about one Lego brick. After the fetch statement we check to see if we went through all the content in the cursor, using our variable `done`, which we declared in the begining of the function. We leave the loop when we have no more content to go though. Our variable `done` also helps us from recieving error massages.

In the loop we have a select statement that joins the LegoBrick table and the StorageLocation table, and pair them up using cross join on the StorageLoctaion ID which both tables contains. The select statement gets the quantity of that specific LegoBrick we are interested in, and inserts that value into the variable `availableLegoBricks`. The variable `availableLegoBricks` is how many pieces there are in stock of this specific Legobrick. We use this variable to check towards the number of pieces we need; `requiredLegoBricks`. If we don't have enough pieces in stock, we set the variable `available` to false and the variable `done` to done. This will break the loop. But if we do have enough pieces, the loop continues.

### RemoveLegoBricks
```
DROP TRIGGER IF EXISTS RemoveLegoBricks;

CREATE TRIGGER RemoveLegoBricks BEFORE INSERT ON OrderContent
FOR EACH ROW
BEGIN
    DECLARE storageID, brickQuantity INT;
    DECLARE lSet, lBrick, lQuant INT;
    DECLARE done INT DEFAULT FALSE;
    DECLARE cursorSetContent CURSOR FOR SELECT * FROM LegoSetContent WHERE LegoSet = New.LegoSet;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    

    OPEN cursorSetContent;

    loopy: LOOP
      FETCH cursorSetContent into lSet, lBrick, lQuant;
      IF done THEN
        LEAVE loopy;
      END IF;
      SELECT StorageLocation INTO storageID FROM LegoBrick WHERE ID = lBrick;
      SELECT Quantity into brickQuantity FROM StorageLocation WHERE ID = storageID;
      UPDATE StorageLocation
        SET Quantity = brickQuantity - lQuant*New.Quantity
        WHERE StorageLocation.id = storageID;
    END LOOP;
    CLOSE cursorSetContent;
END
```
We have two triggers that activates before we insert data in the OrderContent table. `RemoveLegoBricks` is one of them. This trigger updates the available quantity of each Lego brick that was needed for an order. In other words, removes the quantity of Lego pieces from the storage that an order required. Similar to the `CheckAvailability` function, `RemoveLegoBricks` also uses a cursor to fetch data deeper in our tables, and also a variable `done` that helps us break the loop when we are done.

In the loop we insert the `StorageLocation`, for the Lego Brick that we are checking right now, into the variable `storageID`. Then we insert the old quantity value, for our specific Lego brick, into the variable `brickQuantity`.

After that we update the `Quantity` in `StorageLocation`, by taking the old value of available Lego pieces and subtract with the needed value of a specific Lego brick, `lQuant`, for the order, and multiplies by how many LegoSets were ordered `New.Quantity`. This value is now set as the new available quiantity of the Lego brick.

### SumOrder
```
DROP TRIGGER IF EXISTS SumOrder;

CREATE TRIGGER SumOrder BEFORE INSERT ON OrderContent
FOR EACH ROW 
BEGIN    
    DECLARE oldValue, pricePerKit INT;
    SELECT totalSum INTO oldValue FROM `Order` WHERE New.`Order` = `Order`.ID;
    SELECT Price INTO pricePerKit FROM LegoSet  WHERE New.LegoSet = LegoSet.ID;
    UPDATE `Order`
		SET TotalSum = oldValue + pricePerKit * new.Quantity
		WHERE `Order`.ID = New.`Order`;
    
END
```
`SumOrder` is the second trigger that is activated before we insert data in the `OrderContent` table. This trigger updates the total price for the order we are interested in rigth now. This trigger first get the old total price for the order and inserts that value into the variable `oldValue`. Then we get the `Price` for the LegoSet we are working with right now and insert that value into the variable `pricePerKit`. Then finally we update the total order price, `TotalSum` for our order, with: the `oldValue`, which is the acumulated sum from previous LegoSets total prices (alternatively zero, for when this is the first LegoSets in the order), and add the price for that LegoSet, `pricePerKit`, multiplied by the number of LegoSets the order wanted.

## Changelog

| Name| Change Description| Date|
|:----|:------------------|:----|
| Sofia Blom | Setup devcontainer for Python and SQL development | 2024-04-09 |
| Sofia Blom | First attempt at a ER-diagram for the project | 2024-04-12 |
| Sofia Blom | Got flask to display an html template | 2024-05-09 |
| Sofia Blom & Ninni Salomonsson | Created sql files for createing and populating tables | 2024-05-15 |
| Sofia Blom | Frontpage form working with database |2024-08-07|

## Other

### Github access
The repository can be found [here](https://github.com/s02blom/LegoWebStore/). 