\c dealer;

CREATE OR REPLACE FUNCTION protect_order()
    RETURNS TRIGGER AS
$$
BEGIN
    IF (OLD.status != 'pending' AND OLD.status != NEW.status) THEN
        RAISE EXCEPTION 'cannot operate orders more than once';
    END IF;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Tables
-- - orders
CREATE TYPE ORDER_STATUS AS ENUM ('pending', 'canceled', 'completed');
CREATE TABLE IF NOT EXISTS orders
(
    uuid         UUID         NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    creation     TIMESTAMP    NOT NULL             DEFAULT CURRENT_TIMESTAMP,
    modification TIMESTAMP    NOT NULL             DEFAULT CURRENT_TIMESTAMP,
    deletion     TIMESTAMP,
    buyer        UUID         NOT NULL,
    store        UUID         NOT NULL,
    pack         UUID         NOT NULL,
    status       ORDER_STATUS NOT NULL             DEFAULT 'pending',
    code         UUID         NOT NULL             DEFAULT uuid_generate_v4(),
    payed_price  INT          NOT NULL CHECK (payed_price >= 0),
    CONSTRAINT fk_orders_clients FOREIGN KEY (buyer) REFERENCES clients (uuid) ON DELETE CASCADE,
    CONSTRAINT fk_orders_stores FOREIGN KEY (store) REFERENCES stores (uuid) ON DELETE CASCADE,
    CONSTRAINT fk_orders_packs FOREIGN KEY (pack) REFERENCES packs (uuid) ON DELETE CASCADE
);
-- -- Update trigger
CREATE TRIGGER orders_update
    BEFORE UPDATE
    ON orders
    FOR EACH ROW
EXECUTE PROCEDURE update_modification();
CREATE TRIGGER orders_protect_trigger
    BEFORE UPDATE
    ON orders
    FOR EACH ROW
EXECUTE PROCEDURE protect_order();

-- -- Create order procedure
CREATE OR REPLACE PROCEDURE clients_create_order(
    client_uuid_v UUID, pack_uuid_v UUID
)
    LANGUAGE 'plpgsql' AS
$$
DECLARE
    store_uuid_v  UUID;
    DECLARE
    payed_price_v INT;
BEGIN
    store_uuid_v = (SELECT owner FROM packs WHERE uuid = store_uuid_v LIMIT 1);
    payed_price_v = (SELECT price FROM packs WHERE uuid = store_uuid_v LIMIT 1);
    UPDATE packs
    SET stock = stock - 1
    WHERE uuid = pack_uuid_v;
    INSERT INTO orders (buyer, store, pack, payed_price)
    VALUES (client_uuid_v, store_uuid_v, pack_uuid_v, payed_price_v);
END
$$;

-- -- Cancel order procedures
CREATE OR REPLACE PROCEDURE clients_cancel_order(
    client_uuid UUID, order_uuid UUID
)
    LANGUAGE 'plpgsql' AS
$$
BEGIN
    UPDATE orders
    SET status = 'canceled'
    WHERE buyer = client_uuid
      AND uuid = order_uuid;
END
$$;
CREATE OR REPLACE PROCEDURE stores_cancel_order(
    stores_uuid UUID, order_uuid UUID
)
    LANGUAGE 'plpgsql' AS
$$
BEGIN
    UPDATE orders
    SET status = 'canceled'
    WHERE store = stores_uuid
      AND uuid = order_uuid;
END
$$;

CREATE OR REPLACE PROCEDURE stores_complete_order(
    stores_uuid UUID, order_uuid UUID, code_v UUID
)
    LANGUAGE 'plpgsql' AS
$$
BEGIN
    UPDATE orders
    SET status = 'completed'
    WHERE store = stores_uuid
      AND uuid = order_uuid
      AND code = code_v;
END
$$;
