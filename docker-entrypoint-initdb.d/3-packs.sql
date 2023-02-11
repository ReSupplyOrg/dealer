\c dealer;

-- Tables
-- - packs
CREATE TYPE PACK_TYPE AS ENUM ('fast-food', 'dessert', 'random');
CREATE TABLE IF NOT EXISTS packs
(
    uuid         UUID      NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    creation     TIMESTAMP NOT NULL             DEFAULT CURRENT_TIMESTAMP,
    modification TIMESTAMP NOT NULL             DEFAULT CURRENT_TIMESTAMP,
    deletion     TIMESTAMP,
    image_bytes  BYTEA,
    name         TEXT      NOT NULL,
    description  TEXT      NOT NULL,
    owner        UUID      NOT NULL,
    stock        INT       NOT NULL             DEFAULT 0 CHECK (stock >= 0),
    price        INT       NOT NULL CHECK (price >= 0),
    pack_type    PACK_TYPE NOT NULL,
    CONSTRAINT fk_packs_stores FOREIGN KEY (owner) REFERENCES stores (uuid) ON DELETE CASCADE,
    CONSTRAINT unique_pack_per_store UNIQUE (owner, name)
);
-- -- Update trigger
CREATE TRIGGER packs_update
    BEFORE UPDATE
    ON packs
    FOR EACH ROW
EXECUTE PROCEDURE update_modification();

-- -- Create pack procedure
CREATE OR REPLACE PROCEDURE stores_create_packs(
    store_uuid_v UUID, name_v TEXT, description_v TEXT, stock_v INT, price_v INT, pack_type_v PACK_TYPE
)
    LANGUAGE 'plpgsql' AS
$$
BEGIN
    INSERT INTO packs (name, description, owner, stock, price, pack_type)
    VALUES (name_v, description_v, store_uuid_v, stock_v, price_v, pack_type_v);
END
$$;

-- -- Delete pack procedure
CREATE OR REPLACE PROCEDURE stores_delete_pack(
    store_uuid_v UUID, pack_uuid UUID
)
    LANGUAGE 'plpgsql' AS
$$
BEGIN
    UPDATE packs
    SET deletion = NOW()
    WHERE owner = store_uuid_v
      AND uuid = pack_uuid;
END
$$;

-- -- Update procedures

CREATE OR REPLACE PROCEDURE packs_update_image(
    uuid_v UUID, image_v BYTEA
)
    LANGUAGE 'plpgsql' AS
$$
BEGIN
    UPDATE packs
    SET image_bytes = image_v
    WHERE uuid = uuid_v;
END
$$;
CREATE OR REPLACE PROCEDURE packs_update_name(
    uuid_v UUID, name_v TEXT
)
    LANGUAGE 'plpgsql' AS
$$
BEGIN
    UPDATE packs
    SET name = name_v
    WHERE uuid = uuid_v;
END
$$;
CREATE OR REPLACE PROCEDURE packs_update_description(
    uuid_v UUID, description_v TEXT
)
    LANGUAGE 'plpgsql' AS
$$
BEGIN
    UPDATE packs
    SET description = description_v
    WHERE uuid = uuid_v;
END
$$;
CREATE OR REPLACE PROCEDURE packs_update_price(
    uuid_v UUID, price_v INT
)
    LANGUAGE 'plpgsql' AS
$$
BEGIN
    UPDATE packs
    SET price = price_v
    WHERE uuid = uuid_v;
END
$$;
CREATE OR REPLACE PROCEDURE packs_update_stock(
    uuid_v UUID, stock_v TEXT
)
    LANGUAGE 'plpgsql' AS
$$
BEGIN
    UPDATE packs
    SET stock = stock_v
    WHERE uuid = uuid_v;
END
$$;