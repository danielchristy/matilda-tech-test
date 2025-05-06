-- handling updated_at timestamps for ship_order and shipment

CREATE OR REPLACE FUNCTION update_ship_order_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER ship_order_updated_at
BEFORE UPDATE ON ship_order
FOR EACH ROW EXECUTE FUNCTION update_ship_order_timestamp();


CREATE OR REPLACE FUNCTION update_shipment_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER shipment_updated_at
BEFORE UPDATE ON shipment
FOR EACH ROW EXECUTE FUNCTION update_shipment_timestamp();