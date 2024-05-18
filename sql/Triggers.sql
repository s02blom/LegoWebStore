DROP TRIGGER IF EXISTS SumOrder;

DELIMITER ??
CREATE TRIGGER SumOrder BEFORE INSERT ON OrderContent
FOR EACH ROW 
BEGIN    
    DECLARE sum, price INT;
    SET sum = SELECT totalSum FROM `Order` WHERE New.Order = `Order`.ID;
    SET price = SELECT Price FROM LegoSet  WHERE New.LegoSet = LegoSet.ID;
    SET @totalSum = sum + price * New.Quantity;
END ??

DELIMITER ;
