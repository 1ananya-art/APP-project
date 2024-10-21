-- Create the hotel management database
CREATE DATABASE hotel_management;

-- Use the hotel management database
USE hotel_management;

-- Create a table for storing customer information
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    room_number INT NOT NULL,
    check_in_date DATE
);

-- Create a table for storing room information
CREATE TABLE rooms (
    room_number INT PRIMARY KEY,
    is_occupied BOOLEAN DEFAULT FALSE
);
