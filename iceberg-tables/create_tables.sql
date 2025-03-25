CREATE TABLE dta_csv (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    value NUMERIC
);

CREATE TABLE dta_json (
    id SERIAL PRIMARY KEY,
    metadata JSONB
);