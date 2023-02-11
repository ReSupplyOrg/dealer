\c dealer;

-- Tables
-- - Clients
CREATE TABLE IF NOT EXISTS clients
(
    uuid          UUID        NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    creation      TIMESTAMP   NOT NULL             DEFAULT CURRENT_TIMESTAMP,
    modification  TIMESTAMP   NOT NULL             DEFAULT CURRENT_TIMESTAMP,
    deletion      TIMESTAMP,
    phone         TEXT UNIQUE NOT NULL,
    confirmed     BOOLEAN     NOT NULL             DEFAULT FALSE,
    image_bytes   BYTEA,
    names         TEXT        NOT NULL,
    username      TEXT UNIQUE NOT NULL,
    password_salt TEXT        NOT NULL,
    password_hash TEXT        NOT NULL,
    CONSTRAINT clients_valid_phone CHECK (phone ~ '^[0-9]+$')
);
-- -- Update trigger
CREATE TRIGGER clients_update
    BEFORE UPDATE
    ON clients
    FOR EACH ROW
EXECUTE PROCEDURE update_modification();

-- -- Register procedure
CREATE OR REPLACE PROCEDURE clients_register(
    phone_v TEXT, names_v TEXT, username_v TEXT, password_v TEXT
)
    LANGUAGE 'plpgsql' AS
$$
DECLARE
    salt_v                  TEXT;
    DECLARE password_hash_v TEXT;
BEGIN
    salt_v = gen_salt('md5');
    password_hash_v = crypt(password_v, salt_v);
    INSERT INTO clients (phone, names, username, password_salt, password_hash)
    VALUES (phone_v, names_v, username_v, salt_v, password_hash_v);
END
$$;

-- -- Login function
CREATE OR REPLACE FUNCTION clients_login(
    username_v TEXT, passw_v TEXT
)
    RETURNS UUID AS
$$
BEGIN
    RETURN (SELECT uuid
            FROM clients
            WHERE username = username_v
              AND deletion IS NULL
              AND crypt(passw_v, password_salt) = password_hash
            LIMIT 1);
END;
$$ LANGUAGE 'plpgsql';

-- -- Update procedures

CREATE OR REPLACE PROCEDURE clients_update_phone(
    uuid_v UUID, phone_v TEXT
)
    LANGUAGE 'plpgsql' AS
$$
BEGIN
    UPDATE clients
    SET phone     = phone_v,
        confirmed = FALSE
    WHERE uuid = uuid_v;
END
$$;
CREATE OR REPLACE PROCEDURE clients_confirm(
    uuid_v UUID
)
    LANGUAGE 'plpgsql' AS
$$
BEGIN
    UPDATE clients
    SET confirmed = TRUE
    WHERE uuid = uuid_v;
END
$$;
CREATE OR REPLACE PROCEDURE clients_update_image(
    uuid_v UUID, image_v BYTEA
)
    LANGUAGE 'plpgsql' AS
$$
BEGIN
    UPDATE clients
    SET image_bytes = image_v
    WHERE uuid = uuid_v;
END
$$;
CREATE OR REPLACE PROCEDURE clients_update_names(
    uuid_v UUID, names_v TEXT
)
    LANGUAGE 'plpgsql' AS
$$
BEGIN
    UPDATE clients
    SET names = names_v
    WHERE uuid = uuid_v;
END
$$;
CREATE OR REPLACE PROCEDURE clients_update_password(
    uuid_v UUID, password_v TEXT
)
    LANGUAGE 'plpgsql' AS
$$
DECLARE
    salt_v TEXT;
BEGIN
    salt_v = gen_salt('md5');
    UPDATE clients
    SET password_salt = salt_v,
        password_hash = crypt(password_v, salt_v)
    WHERE uuid = uuid_v;
END
$$;