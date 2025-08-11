-- Insert Admin User
INSERT INTO users (first_name, last_name, email, password, role_id)
VALUES ('System', 'Admin', 'admin@example.com', 'hashed_admin_password', 1);

-- Insert Instructor User
INSERT INTO users (first_name, last_name, email, password, role_id)
VALUES ('Jane', 'Doe', 'jane.doe@example.com', 'hashed_password', 2);


-- Insert Student User
INSERT INTO users (first_name, last_name, email, password, role_id)
VALUES ('John', 'Smith', 'john.smith@example.com', 'hashed_password', 3);
