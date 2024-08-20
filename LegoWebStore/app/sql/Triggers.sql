DROP TRIGGER IF EXISTS SumOrder, RemoveLegoBricks;

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

CREATE TRIGGER RemoveLegoBricks BEFORE INSERT ON OrderContent
FOR EACH ROW
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE cursorSetContent FOR SELECT * FROM LegoSetContent WHERE LegoSet = New.LegoSet;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    DECLARE storageID, brickQuantity INT;
    DECLARE lSet, lBrick, lQuant INT;

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