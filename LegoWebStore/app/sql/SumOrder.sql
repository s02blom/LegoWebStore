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