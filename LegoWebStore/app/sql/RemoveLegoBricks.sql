DROP TRIGGER IF EXISTS RemoveLegoBricks;

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