-- handling business logic for preventing shipment state from sent to cancelled

CREATE OR REPLACE FUNCTION prevent_shipment_cancel_after_sent()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.shipment_state = 'sent' AND NEW.shipment_state = 'cancelled' THEN
        RAISE EXCEPTION 'Shipment has been sent - cannot cancel.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER prevent_cancel_after_sent
BEFORE UPDATE ON shipment
FOR EACH ROW EXECUTE FUNCTION prevent_shipment_cancel_after_sent();