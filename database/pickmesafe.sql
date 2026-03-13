-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 16, 2024 at 09:50 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `pickmesafe`
--

-- --------------------------------------------------------

--
-- Table structure for table `pm_driver`
--

CREATE TABLE `pm_driver` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `address` varchar(40) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(30) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `date_join` varchar(20) NOT NULL,
  `profile` varchar(100) NOT NULL,
  `veh_no` varchar(20) NOT NULL,
  `owner_username` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pm_driver`
--

INSERT INTO `pm_driver` (`id`, `name`, `address`, `mobile`, `email`, `username`, `password`, `date_join`, `profile`, `veh_no`, `owner_username`) VALUES
(1, 'ramu raja p', '12, new str', 8838468320, 'huwaidom@gmail.com', 'admin', '1234', '07-04-2024', 'c1.jpg', 'TN 38 BR 3036', 'logo');

-- --------------------------------------------------------

--
-- Table structure for table `pm_rto`
--

CREATE TABLE `pm_rto` (
  `id` int(5) NOT NULL,
  `username` varchar(10) NOT NULL,
  `password` varchar(10) NOT NULL,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pm_rto`
--

INSERT INTO `pm_rto` (`id`, `username`, `password`) VALUES
(1, 'admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `pm_travel`
--

CREATE TABLE `pm_travel` (
  `id` int(11) NOT NULL,
  `veh_no` varchar(25) NOT NULL,
  `oname` varchar(30) NOT NULL,
  `omobile` bigint(20) NOT NULL,
  `oaddress` varchar(30) NOT NULL,
  `veh_type` varchar(30) NOT NULL,
  `veh_name` varchar(30) NOT NULL,
  `dname` varchar(30) NOT NULL,
  `dmobile` bigint(20) NOT NULL,
  `daddress` varchar(30) NOT NULL,
  `gmobile` bigint(20) NOT NULL,
  `gname` varchar(30) NOT NULL,
  `user` varchar(30) NOT NULL,
  `uaddress` varchar(30) NOT NULL,
  `umobile` bigint(20) NOT NULL,
  `username` varchar(30) NOT NULL,
  `reg_join` varchar(20) NOT NULL,
  `status` int(5) NOT NULL,
  `latitude` varchar(20) NOT NULL,
  `longitude` varchar(20) NOT NULL,
  `source` varchar(30) NOT NULL,
  `destination` varchar(30) NOT NULL,
  `owner_username` varchar(20) NOT NULL,
  `feedback` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pm_travel`
--

INSERT INTO `pm_travel` (`id`, `veh_no`, `oname`, `omobile`, `oaddress`, `veh_type`, `veh_name`, `dname`, `dmobile`, `daddress`, `gmobile`, `gname`, `user`, `uaddress`, `umobile`, `username`, `reg_join`, `status`, `latitude`, `longitude`, `source`, `destination`, `owner_username`, `feedback`) VALUES
(1, 'TN 38 BR 3036', 'Vasu', 8838468320, '34, karur', 'Car', 'Swift', 'admin', 8838468320, '12, new str', 8838468320, 'Example', 'Ravi', '56, karur', 8838468320, 'ravi', '13-04-2024', 2, '11.0142', '76.9941', 'Maduurai', 'Trichy', 'logo', 'Super service');

-- --------------------------------------------------------

--
-- Table structure for table `pm_user`
--

CREATE TABLE `pm_user` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `address` varchar(40) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(30) NOT NULL,
  `gu_name` varchar(20) NOT NULL,
  `gu_mobile` bigint(20) NOT NULL,
  `profile` varchar(100) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `date_join` date NOT NULL,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pm_user`
--

INSERT INTO `pm_user` (`id`, `name`, `address`, `mobile`, `email`, `gu_name`, `gu_mobile`, `profile`, `username`, `password`, `date_join`) VALUES
(1, 'Ravi', '56, karur', 8838468320, 'kalirajan3079@gmail.com', 'Example', 8838468320, '', 'ravi', '1234', '0000-00-00');

-- --------------------------------------------------------

--
-- Table structure for table `pm_vehicle`
--

CREATE TABLE `pm_vehicle` (
  `id` int(11) NOT NULL,
  `veh_no` varchar(20) NOT NULL,
  `reg_mobile` bigint(20) NOT NULL,
  `reg_name` varchar(20) NOT NULL,
  `reg_address` varchar(100) NOT NULL,
  `veh_type` varchar(20) NOT NULL,
  `veh_name` varchar(20) NOT NULL,
  `veh_color` varchar(20) NOT NULL,
  `fuel_type` varchar(10) NOT NULL,
  `chassis_no` varchar(30) NOT NULL,
  `seats` int(10) NOT NULL,
  `reg_join` date NOT NULL,
  `image` varchar(100) NOT NULL,
  `images` varchar(100) NOT NULL,
  `proof` varchar(100) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pm_vehicle`
--

INSERT INTO `pm_vehicle` (`id`, `veh_no`, `reg_mobile`, `reg_name`, `reg_address`, `veh_type`, `veh_name`, `veh_color`, `fuel_type`, `chassis_no`, `seats`, `reg_join`, `image`, `images`, `proof`, `username`, `password`) VALUES
(1, 'TN 38 BR 3036', 8838468320, 'Vasu', '34, karur', 'Car', 'Swift', 'Red', 'Diesel', '24679YU2316DF', 3, '2024-02-27', '50950667-9541-4a86-a227-4e8db1969507_download.jpg', 'b4759679-fe2e-483e-a012-5834c82c1f0a_c1.jpg', 'a8b8dc8a-9567-4e5d-9726-c61efba11d43_1.jpg', 'logo', '1234'),
(2, 'TN G6 S 5656,', 8148956634, 'Harish', '78,west str, Tirunelveli', 'Auto', 'Maruthi', 'Yellow', 'Petrol', '34KS1772SLK75', 4, '2024-02-17', 'pexels-tim-samuel-5834937.jpg', 'face1.jpg', 'a8b8dc8a-9567-4e5d-9726-c61efba11d43_1.jpg', 'raja', '1234'),
(3, 'awe 74 AH 6561', 8148956634, 'Ponraj', '56, washington road, Tuticorin', 'Car', 'Ford', 'Gray', 'Diesel', '67788DJD262FG1', 4, '2024-02-24', 'pexels-huu-huynh-18915664.jpg', 'face2.jpg', 'a8b8dc8a-9567-4e5d-9726-c61efba11d43_1.jpg', 'raja', '1234'),
(4, 'IN 47 X aoe', 8148956634, 'John', '78,west str, Chennai', 'Car', 'Tata suv-800', 'Black', 'Petrol', '34KS1772SLK89G', 4, '2024-02-25', 'pexels-tim-samuel-5835053.jpg', 'face3.jpg', 'a8b8dc8a-9567-4e5d-9726-c61efba11d43_1.jpg', 'vasu', '1234'),
(5, '“DLZCAF4943', 8148956634, 'Ganesh', '67, h.r nagar, karur', 'Car', 'Yamaha- razon', 'Blue', 'Diesel', '67788DJD262S545', 4, '2024-02-29', 'pexels-tim-samuel-5835291.jpg', 'face4.jpg', 'a8b8dc8a-9567-4e5d-9726-c61efba11d43_1.jpg', 'sam', '1234'),
(6, '-DL7CO 1939!', 8148956634, 'Lokesh', '9, fathima nagar, Trichy', 'Van', 'Marcopolo', 'White', 'Diesel', '56DS1772SLK75', 9, '2024-02-28', 'pexels-axp-photography-18729244.jpg', 'face5.jpg', 'a8b8dc8a-9567-4e5d-9726-c61efba11d43_1.jpg', 'Harsh', '1234'),
(7, '“21 BH 0001 AA', 8148956634, 'Mani', '90, ngo colony, Theni', 'Car', 'Ford-15', 'Navy blue', 'Diesel', '67YU8DJD262FG1', 4, '2024-02-26', 'pexels-mart-lmj-2563994.jpg', 'face6.jpg', '', 'test', '1234'),
(8, '=X KOSMD 4923)', 8148956634, 'Dhana', '9, Kamaraj nagar, Trichy', 'Car', 'Tiago-ev', 'Black', 'E-vehicle', '34KS1772SLK75', 6, '2024-02-23', 'pexels-ps-photography-67183.jpg', 'face7.jpg', '', 'yazhl', '123456'),
(9, 'we KAIS” eo 0001', 8148956634, 'John', '67, Bashir street, kanyakumari', 'Van', 'Maxi cab', 'black', 'Diesel', '67YU8DJD262FG1', 4, '2024-02-04', 'pexels-alexandros-chatzidimos-3652766.jpg', 'face8.jpg', '', 'kavi', '12345'),
(10, 'NGP 3944', 8148956634, 'Kailesh', '81, nehru nagar', 'Auto', 'Maruthi', 'Black', 'E-vehicle', '34KS1772SLUY56', 3, '2024-02-24', 'pexels-ricky-esquivel-1662160.jpg', 'face9.jpg', '', 'jo', '12345');
