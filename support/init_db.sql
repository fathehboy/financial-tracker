-- Create database
CREATE DATABASE trackerdb;

\c trackerdb

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    salt VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    failed_attempts INT DEFAULT 0,
    locked_until TIMESTAMP
);

-- Insert default user (replace password_hash and salt later)
INSERT INTO users (username, email, password_hash, salt)
VALUES (
    'fatheh',
    'fatheh.alif@gmail.com',
    '$2b$12$z7cj137BwVHzU2ujsEL6qu',
    '$2b$12$z7cj137BwVHzU2ujsEL6qulQkgSs8tgDxq/Lp4E1yE1XtId9Vu.eW'
);