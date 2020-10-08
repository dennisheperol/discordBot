create TABLE poop_balance (
    id BIGINT NOT NULL UNIQUE PRIMARY KEY,
    balance BIGINT NOT NULL
);

create TABLE scavenge_time (
    id BIGINT NOT NULL UNIQUE PRIMARY KEY,
    time DOUBLE PRECISION NOT NULL
)