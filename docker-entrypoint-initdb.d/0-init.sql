\c dealer;

-- Dependencies

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- -- On Update trigger
CREATE OR REPLACE FUNCTION update_modification()
    RETURNS TRIGGER AS
$$
BEGIN
    NEW.modification = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';