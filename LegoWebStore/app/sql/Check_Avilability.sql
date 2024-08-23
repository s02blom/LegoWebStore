DROP PROCEDURE IF EXISTS CheckAvilability;

CREATE PROCEDURE CheckAvilability (IN legoSetId INT, OUT avilable BOOLEAN)
BEGIN
    DECLARE lSet, LBrick, requiredLegoBricks, avilableLegoBricks INT;
    DECLARE done INT DEFAULT FALSE;
    DECLARE cursorSetContent CURSOR FOR SELECT * FROM LegoSetContent WHERE LegoSet = legoSetId;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    SET avilable = TRUE;
    OPEN cursorSetContent;
    
    LegoBricksLoop: LOOP
        FETCH cursorSetContent into lSet, LBrick, requiredLegoBricks;
        IF done THEN
            LEAVE LegoBricksLoop;
        END IF;

        SELECT StorageLocation.Quantity INTO avilableLegoBricks
            FROM LegoBrick
            CROSS JOIN StorageLocation ON LegoBrick.StorageLocation = StorageLocation.ID
            WHERE LegoBrick.id = LBrick;
        IF avilableLegoBricks < requiredLegoBricks THEN
            SET avilable = FALSE;
            SET done = True;
        END IF;
    END LOOP;
    CLOSE cursorSetContent;
END