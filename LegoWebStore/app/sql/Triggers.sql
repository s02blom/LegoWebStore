DROP TRIGGER IF EXISTS SumOrder;

DELIMITER ??
CREATE TRIGGER SumOrder BEFORE INSERT ON OrderContent
FOR EACH ROW 
BEGIN    
    DECLARE sum, price INT;
    SELECT totalSum INTO sum FROM `Order` WHERE New.`Order` = `Order`.ID;
    SELECT Price INTO price FROM LegoSet  WHERE New.LegoSet = LegoSet.ID;
    UPDATE OrderContent set totalSum = sum + price * new.Quantity
    WHERE `Order`.ID = New.`Order`;
    
END ??

DELIMITER ;
