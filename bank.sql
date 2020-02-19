-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 27, 2020 at 04:04 PM
-- Server version: 10.1.37-MariaDB
-- PHP Version: 7.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bank`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin_reg`
--

CREATE TABLE `admin_reg` (
  `ID` int(100) NOT NULL,
  `fname` varchar(40) NOT NULL,
  `lname` varchar(40) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `email` varchar(50) NOT NULL,
  `contact` varchar(15) NOT NULL,
  `password` varchar(265) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin_reg`
--

INSERT INTO `admin_reg` (`ID`, `fname`, `lname`, `gender`, `email`, `contact`, `password`) VALUES
(1, 'venkat', 'kishore', 'male', 'venkat.kishore@bank.com', '9538618698', 'bank'),
(2, 'admin', 'b', 'male', 'admin@admin.com', '123456789', 'pbkdf2:sha256:150000$agjhlqa7$9ef5fe4c6acea7a0b71b89f41ad3386b1f7b7e3ea5253340ea360dd450884140');

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `ID` int(11) NOT NULL,
  `from_add` varchar(100) NOT NULL,
  `to_add` varchar(100) NOT NULL,
  `date` varchar(50) NOT NULL,
  `amount` int(11) NOT NULL,
  `email` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `transactions`
--

INSERT INTO `transactions` (`ID`, `from_add`, `to_add`, `date`, `amount`, `email`) VALUES
(1, 'venkat', 'nani', '2020-01-27', 2, 'venkat.kishore610@gmail.com'),
(2, 'venkat', 'nani', '2020-01-27', 2, 'venkat.kishore610@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `user_reg`
--

CREATE TABLE `user_reg` (
  `ID` int(100) NOT NULL,
  `fname` varchar(40) NOT NULL,
  `lname` varchar(40) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `email` varchar(50) NOT NULL,
  `contact` varchar(15) NOT NULL,
  `password` varchar(265) NOT NULL,
  `reg_date` varchar(20) NOT NULL,
  `balance` int(11) NOT NULL,
  `closed_date` varchar(20) NOT NULL,
  `status` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user_reg`
--

INSERT INTO `user_reg` (`ID`, `fname`, `lname`, `gender`, `email`, `contact`, `password`, `reg_date`, `balance`, `closed_date`, `status`) VALUES
(1, 'venkat', 'kishore', 'male', 'venkat.kishore610@gmail.com', '7382181612', 'pbkdf2:sha256:150000$frnljj1p$2ebda410b78176b743124dda0dfa9030f58586c1ba424d9f747eb1cf6c1bf10a', '2020-01-25', 170, '2020-01-27', 'Activate'),
(2, 'nani', 'b', 'male', 'nani@gmail.com', '966199739', 'pbkdf2:sha256:150000$YJFp2DlD$68942c9baf9bf45a21bd317f1980b31f8406c007ca67a7f95a4422acaff31279', '2020-01-26', 84, '', 'Activate');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin_reg`
--
ALTER TABLE `admin_reg`
  ADD UNIQUE KEY `ID` (`ID`);

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD UNIQUE KEY `ID` (`ID`);

--
-- Indexes for table `user_reg`
--
ALTER TABLE `user_reg`
  ADD UNIQUE KEY `ID` (`ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin_reg`
--
ALTER TABLE `admin_reg`
  MODIFY `ID` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `user_reg`
--
ALTER TABLE `user_reg`
  MODIFY `ID` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
