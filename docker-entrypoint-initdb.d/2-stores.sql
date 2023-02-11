\c dealer;

CREATE OR REPLACE FUNCTION rating_change()
    RETURNS TRIGGER AS
$$
DECLARE
    avg_rating DOUBLE PRECISION;
BEGIN
    avg_rating = AVG(
                (SELECT rating FROM ratings WHERE store_uuid = NEW.store_uuid)
        );
    UPDATE stores
    SET rating = avg_rating
    WHERE stores.uuid = NEW.store_uuid;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Tables
-- - stores
CREATE TABLE IF NOT EXISTS stores
(
    uuid          UUID             NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    creation      TIMESTAMP        NOT NULL             DEFAULT CURRENT_TIMESTAMP,
    modification  TIMESTAMP        NOT NULL             DEFAULT CURRENT_TIMESTAMP,
    deletion      TIMESTAMP,
    phone         TEXT UNIQUE      NOT NULL,
    confirmed     BOOLEAN          NOT NULL             DEFAULT FALSE,
    image_bytes   BYTEA,
    name          TEXT             NOT NULL,
    rating        DOUBLE PRECISION NOT NULL             DEFAULT 0 CHECK ( rating >= 0),
    address       TEXT             NOT NULL,
    username      TEXT UNIQUE      NOT NULL,
    password_salt TEXT             NOT NULL,
    password_hash TEXT             NOT NULL,
    CONSTRAINT stores_valid_phone CHECK (phone ~ '^[0-9]+$')
);
CREATE TABLE IF NOT EXISTS ratings
(
    creation     TIMESTAMP        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modification TIMESTAMP        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deletion     TIMESTAMP,
    client_uuid  UUID             NOT NULL,
    store_uuid   UUID             NOT NULL,
    rating       DOUBLE PRECISION NOT NULL DEFAULT 0 CHECK ( rating >= 0),
    CONSTRAINT unique_ratings_entry UNIQUE (client_uuid, store_uuid),
    CONSTRAINT fk_ratings_clients FOREIGN KEY (client_uuid) REFERENCES clients (uuid) ON DELETE CASCADE,
    CONSTRAINT fk_ratings_stores FOREIGN KEY (store_uuid) REFERENCES stores (uuid) ON DELETE CASCADE
);
-- -- Update trigger
CREATE TRIGGER stores_update
    BEFORE UPDATE
    ON stores
    FOR EACH ROW
EXECUTE PROCEDURE update_modification();
CREATE TRIGGER ratings_update
    BEFORE UPDATE
    ON ratings
    FOR EACH ROW
EXECUTE PROCEDURE update_modification();
-- -- Ratings triggers
CREATE TRIGGER refresh_ratings_value_update
    AFTER UPDATE
    ON ratings
    FOR EACH ROW
EXECUTE PROCEDURE rating_change();
CREATE TRIGGER refresh_ratings_value_insert
    AFTER INSERT
    ON ratings
    FOR EACH ROW
EXECUTE PROCEDURE rating_change();

-- -- Register procedure
CREATE OR REPLACE PROCEDURE stores_register(
    phone_v TEXT, name_v TEXT, address_v TEXT, username_v TEXT, password_v TEXT
)
    LANGUAGE 'plpgsql' AS
$$
DECLARE
    salt_v                  TEXT;
    DECLARE password_hash_v TEXT;
BEGIN
    salt_v = gen_salt('md5');
    password_hash_v = crypt(password_v, salt_v);
    INSERT INTO stores (phone, name, address, username, password_salt, password_hash)
    VALUES (phone_v, name_v, address_v, username_v, salt_v, password_hash_v);
END
$$;

-- -- Login function
CREATE OR REPLACE FUNCTION stores_login(
    username_v TEXT, passw_v TEXT
)
    RETURNS UUID AS
$$
BEGIN
    RETURN (SELECT uuid
            FROM stores
            WHERE username = username_v
              AND deletion IS NULL
              AND crypt(passw_v, password_salt) = password_hash
            LIMIT 1);
END;
$$ LANGUAGE 'plpgsql';

-- -- Rating procedure
CREATE OR REPLACE PROCEDURE rate_store(
    client_uuid_v UUID, store_uuid_v UUID, rating_v DOUBLE PRECISION
)
    LANGUAGE 'plpgsql' AS
$$
BEGIN
    INSERT INTO ratings (client_uuid, store_uuid, rating)
    VALUES (client_uuid_v, store_uuid_v, rating_v)
    ON CONFLICT ON CONSTRAINT unique_ratings_entry DO UPDATE SET rating = rating_v;
END
$$;

-- -- Update procedures

CREATE OR REPLACE PROCEDURE stores_update_phone(
    uuid_v UUID, phone_v TEXT
)
    LANGUAGE 'plpgsql' AS
$$
BEGIN
    UPDATE stores
    SET phone     = phone_v,
        confirmed = FALSE
    WHERE uuid = uuid_v;
END
$$;
CREATE OR REPLACE PROCEDURE stores_confirm(
    uuid_v UUID
)
    LANGUAGE 'plpgsql' AS
$$
BEGIN
    UPDATE stores
    SET confirmed = TRUE
    WHERE uuid = uuid_v;
END
$$;
CREATE OR REPLACE PROCEDURE stores_update_image(
    uuid_v UUID, image_v BYTEA
)
    LANGUAGE 'plpgsql' AS
$$
BEGIN
    UPDATE stores
    SET image_bytes = image_v
    WHERE uuid = uuid_v;
END
$$;
CREATE OR REPLACE PROCEDURE stores_update_name(
    uuid_v UUID, name_v TEXT
)
    LANGUAGE 'plpgsql' AS
$$
BEGIN
    UPDATE stores
    SET name = name_v
    WHERE uuid = uuid_v;
END
$$;
CREATE OR REPLACE PROCEDURE stores_update_address(
    uuid_v UUID, address_v TEXT
)
    LANGUAGE 'plpgsql' AS
$$
BEGIN
    UPDATE stores
    SET address = address_v
    WHERE uuid = uuid_v;
END
$$;
CREATE OR REPLACE PROCEDURE stores_update_password(
    uuid_v UUID, old_password_v TEXT, new_password_v TEXT
)
    LANGUAGE 'plpgsql' AS
$$
DECLARE
    salt_v TEXT;
BEGIN
    salt_v = gen_salt('md5');
    UPDATE stores
    SET password_salt = salt_v,
        password_hash = crypt(new_password_v, salt_v)
    WHERE uuid = uuid_v
      AND password_hash = crypt(old_password_v, password_salt);
END
$$;