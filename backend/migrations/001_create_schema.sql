CREATE TYPE order_state AS ENUM ('new', 'in_process', 'sent', 'cancelled');

CREATE TABLE IF NOT EXISTS employee (
    employee_id SERIAL PRIMARY KEY,
    username VARCHAR(25) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS shipping_company (
    ship_company_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS client (
    client_id SERIAL PRIMARY KEY,
    ship_company_id INT NOT NULL REFERENCES shipping_company(ship_company_id) ON DELETE CASCADE,
    client_name VARCHAR(255) NOT NULL,
    client_address TEXT NOT NULL,
    client_contact_info TEXT NOT NULL,
    client_billing_info TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ship_order (
    ship_order_id SERIAL PRIMARY KEY,
    client_id INT NOT NULL REFERENCES client(client_id) ON DELETE CASCADE,
    ship_order_state order_state NOT NULL,
    ship_order_date DATE,
    expected_shipments INT NOT NULL,
    completed_shipments INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS shipment (
    shipment_id SERIAL PRIMARY KEY,
    ship_order_id INT NOT NULL REFERENCES ship_order(ship_order_id) ON DELETE CASCADE,
    shipment_state order_state NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS item (
    item_id SERIAL PRIMARY KEY,
    sku VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    item_metadata JSONB
);

CREATE TABLE IF NOT EXISTS ship_order_item (
    ship_order_id INT NOT NULL,
    item_id INT NOT NULL,
    order_quantity INT NOT NULL,
    PRIMARY KEY (ship_order_id, item_id),
    FOREIGN KEY (ship_order_id) REFERENCES ship_order(ship_order_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES item(item_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS shipment_item (
    shipment_id INT NOT NULL,
    item_id INT NOT NULL,
    order_quantity INT NOT NULL,
    PRIMARY KEY (shipment_id, item_id),
    FOREIGN KEY (shipment_id) REFERENCES shipment(shipment_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES item(item_id) ON DELETE CASCADE
);

