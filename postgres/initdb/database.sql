CREATE TABLE mtech (
    unique_id CHAR(36) NOT NULL UNIQUE PRIMARY KEY,
    created TIMESTAMP(6) NOT NULL,
    ip_address INET NOT NULL,
    http_method VARCHAR(7) NOT NULL,
    request_uri VARCHAR(255) NOT NULL,
    http_code SMALLINT NOT NULL
);

INSERT INTO mtech (unique_id, created, ip_address, http_method, request_uri, http_code)
VALUES
    ('3f47ce6f-4a37-4bb9-97b0-79af7c864cd4', '2023-12-13 15:56:56.548809', '192.168.10.25', 'GET', 'https://example.org/', '200'),
    ('fa789ff1-01b5-4174-9072-bfe8cfd0b249', '2023-10-04 22:11:01.005454', '192.168.1.2', 'GET', 'http://example.net', '301'),
    ('1d301f61-d63a-46d9-bdb8-63004d0504af', '2022-12-13 15:56:56.926504', '192.168.100.25', 'GET', 'http://example.com', '400'),
    ('e4286fe6-7094-4a55-8377-4373d78322e2', '2023-12-15 15:56:56.408066', '192.168.10.251', 'POST', 'https://cloud.example.com', '201');
