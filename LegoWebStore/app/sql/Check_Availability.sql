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