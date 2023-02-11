# Database

This document describes the database present on dealer.

### Tables

```mermaid
erDiagram

clients {
	UUID uuid "UUID PRIMARY KEY"
	TIMESTAMP creation "TIMESTAMP NOT NULL DEFAUL CURRENT_TIMESTAMP"
	TIMESTAMP modification "TIMESTAMP NOT NULL DEFAUL CURRENT_TIMESTAMP"
	TIMESTAMP deletion "TIMESTAMP NOT NULL DEFAUL CURRENT_TIMESTAMP"
	TEXT phone "TEXT NOT NULL CHECK phone LIKE '\+\d{10}'"
	BOOL confirmed "BOOL NOT NULL DEFAULT FALSE"
	BLOB image_bytes "BLOB"
	TEXT names "TEXT NOT NULL"
	TEXT username "TEXT NOT NULL UNIQUE"
	TEXT password_salt "TEXT NOT NULL"
	TEXT password_hash "TEXT NOT NULL"
}
stores {
	UUID uuid "UUID PRIMARY KEY"
	TIMESTAMP creation "TIMESTAMP NOT NULL DEFAUL CURRENT_TIMESTAMP"
	TIMESTAMP modification "TIMESTAMP NOT NULL DEFAUL CURRENT_TIMESTAMP"
	TIMESTAMP deletion "TIMESTAMP NOT NULL DEFAUL CURRENT_TIMESTAMP"
	TEXT phone "TEXT NOT NULL CHECK phone LIKE '\+\d{10}'"
	BOOL confirmed "BOOL NOT NULL DEFAULT FALSE"
	BLOB image_bytes "BLOB"
	TEXT name "TEXT NOT NULL"
	DOUBLE rating "DOUBLE NOT NULL DEFAULT 0.0"
	TEXT address "TEXT NOT NULL"
	TEXT username "TEXT NOT NULL UNIQUE"
	TEXT password_salt "TEXT NOT NULL"
	TEXT password_hash "TEXT NOT NULL"
}
```

```mermaid
erDiagram
ratings {
	TIMESTAMP creation "TIMESTAMP NOT NULL DEFAUL CURRENT_TIMESTAMP"
	TIMESTAMP modification "TIMESTAMP NOT NULL DEFAUL CURRENT_TIMESTAMP"
	TIMESTAMP deletion "TIMESTAMP NOT NULL DEFAUL CURRENT_TIMESTAMP"
	UUID client_uuid "UUID NOT NULL FOREIGN KEY REFERENCES clients uuid"
	UUID store_uuid "UUID NOT NULL FOREIGN KEY REFERENCES stores uuid"
	DOUBLE rating "DOUBLE NOT NULL DEFAULT 0.0"
}

packs {
	UUID uuid "UUID PRIMARY KEY"
	TIMESTAMP creation "TIMESTAMP NOT NULL DEFAUL CURRENT_TIMESTAMP"
	TIMESTAMP modification "TIMESTAMP NOT NULL DEFAUL CURRENT_TIMESTAMP"
	TIMESTAMP deletion "TIMESTAMP NOT NULL DEFAUL CURRENT_TIMESTAMP"
	BLOB image "BLOB"
	UUID owner "UUID NOT NULL FOREIGN KEY REFERENCES stores uuid"
	INT stock "INT NOT NULL DEFAULT 0 CHECK stock >= 0"
	INT price "INT NOT NULL CHECK price >= 0"
	TEXT name "TEXT NOT NULL"
	PACK_TYPE pack_type "PACK_TYPE NOT NULL"
	TEXT description "TEXT NOT NULL"
}
```

```mermaid
erDiagram

orders {
	UUID uuid "UUID PRIMARY KEY"
	TIMESTAMP creation "TIMESTAMP NOT NULL DEFAUL CURRENT_TIMESTAMP"
	TIMESTAMP modification "TIMESTAMP NOT NULL DEFAUL CURRENT_TIMESTAMP"
	TIMESTAMP deletion "TIMESTAMP NOT NULL DEFAUL CURRENT_TIMESTAMP"
	UUID buyer "UUID NOT NULL FOREIGN KEY REFERENCES clients uuid"
	UUID store "UUID NOT NULL FOREIGN KEY REFERENCES stores uuid"
	UUID pack "UUID NOT NULL FOREIGN KEY REFERENCES packs uuid"
	STATUS status "STATUS NOT NULL"
	INT payed_price "INT NOT NULL CHECK payed_price >= 0"
}
```

### Relations

#### Order system

```mermaid
erDiagram

clients ||--o{ orders : "Can read / create / cancel"
stores ||--o{ orders : "Can read / cancel"
stores ||--o{ packs : "Can read / create / update / delete"
orders ||--o{ packs : "Contain"
```

#### Rating system

```mermaid
erDiagram

clients ||--o{ ratings : "Has"
stores ||--o{ ratings : "Has"
```

## Cache

Dealer uses any `redis` like cache to store user sessions in the format `random_key:user_uuid`