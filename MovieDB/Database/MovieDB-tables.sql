CREATE TABLE `Movie` (
  `MovieID` int NOT NULL AUTO_INCREMENT,
  `DirectorID` int NOT NULL,
  `Title` varchar(50) NOT NULL,
  `ReleaseYear` year NOT NULL,
  PRIMARY KEY (`MovieID`)
);

CREATE TABLE `Director` (
  `DirectorID` int NOT NULL AUTO_INCREMENT,
  `FirstName` varchar(40) NOT NULL,
  `LastName` varchar(40) NOT NULL,
  PRIMARY KEY (`DirectorID`)
);

CREATE TABLE `Movie_Director` (
  `Movie_MovieID` int NOT NULL,
  `Director_DirectorID` int NOT NULL,
  PRIMARY KEY (`Movie_MovieID`, `Director_DirectorID`),
  FOREIGN KEY (`Movie_MovieID`) REFERENCES `Movie`(`MovieID`),
  FOREIGN KEY (`Director_DirectorID`) REFERENCES `Director`(`DirectorID`)
);