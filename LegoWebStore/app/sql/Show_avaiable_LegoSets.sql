#Shows how many kinds of pieses is out of stock for a LegoSet.
#If the LegoSet is not on the list then it has all its pieces in stock.
#Call the procedure using:
#CALL What_LegoSet_Is_Out_Of_Stock;

DELIMITER %%

DROP PROCEDURE IF EXISTS What_LegoSet_Is_Out_Of_Stock%%

CREATE PROCEDURE What_LegoSet_Is_Out_Of_Stock()
BEGIN
	SELECT LegoSet.`Name`, count(LegoSet.`Name`) AS How_Many_Kinds_Of_Piece_Are_Out_Of_Stock
	FROM LegoSet
	INNER JOIN LegoSetContent ON LegoSet.ID = LegoSetContent.LegoSet
	INNER JOIN LegoBrick ON LegoSetContent.LegoBrick = LegoBrick.ID
	INNER JOIN StorageLocation ON LegoBrick.StorageLocation = StorageLocation.ID
	WHERE (StorageLocation.Quantity <= LegoSetContent.Quantity)
	GROUP BY LegoSet.`Name`, LegoSet.Price
	ORDER BY LegoSet.`Name`;
END%%

DELIMITER ;