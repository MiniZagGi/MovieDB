CREATE TABLE `Director` (
  `DirectorID` int NOT NULL AUTO_INCREMENT,
  `FirstName` varchar(40),
  `LastName` varchar(40),
  `BirthYear` year,
  PRIMARY KEY (`DirectorID`)
);

CREATE TABLE `Movie` (
  `MovieID` int NOT NULL AUTO_INCREMENT,
  `Title` varchar(50) NOT NULL,
  `ReleaseYear` year NOT NULL,
  PRIMARY KEY (`MovieID`)
);

CREATE TABLE `Movie_Director` (
  `Movie_MovieID` int NOT NULL,
  `Director_DirectorID` int NOT NULL,
  PRIMARY KEY (`Movie_MovieID`, `Director_DirectorID`),
  FOREIGN KEY (`Director_DirectorID`) REFERENCES `Director`(`DirectorID`),
  FOREIGN KEY (`Movie_MovieID`) REFERENCES `Movie`(`MovieID`)
);

CREATE TABLE `MediaType` (
  `MediaTypeID` int NOT NULL AUTO_INCREMENT,
  `Type` varchar(20) NOT NULL,
  PRIMARY KEY (`MediaTypeID`)
);

CREATE TABLE `Movie_MediaType` (
  `Movie_MovieID` int NOT NULL,
  `MediaType_MediaTypeID` int NOT NULL,
  `IsBackedUp` BOOLEAN NOT NULL DEFAULT FALSE,
  `IsOwned` BOOLEAN NOT NULL DEFAULT TRUE,
  `OwnedSince` DATETIME DEFAULT NULL,
  `ThrownOutOn` DATETIME DEFAULT NULL,
  PRIMARY KEY (`Movie_MovieID`, `MediaType_MediaTypeID`),
  FOREIGN KEY (`Movie_MovieID`) REFERENCES `Movie`(`MovieID`),
  FOREIGN KEY (`MediaType_MediaTypeID`) REFERENCES `MediaType`(`MediaTypeID`)
);

