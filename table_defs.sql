
PRAGMA foreign_keys = ON;

Create TABLE IF NOT EXISTS main.rl_insider_item
(
    item_name         VARCHAR(50) NOT NULL,
    item_url_name     VARCHAR(50) NOT NULL,
    item_rarity       VARCHAR(50) NOT NULL,
    item_type         VARCHAR(50) NOT NULL,
    item_is_paintable BOOLEAN     NOT NULL,
    item_id           INTEGER,

    PRIMARY KEY (item_id)
);

CREATE TABLE IF NOT EXISTS rl_insider_prices
(
    item_id         INTEGER,
    item_color      VARCHAR(50) NOT NULL,
    item_price_low  INTEGER,
    item_price_high INTEGER,

    PRIMARY KEY (item_id, item_color),
    FOREIGN KEY (item_id) REFERENCES rl_insider_item (item_id) ON DELETE CASCADE
);

-- rlg

CREATE TABLE IF NOT EXISTS rl_garage_trade
(
    rlg_name          VARCHAR(50),
    platform          VARCHAR(50),
    platform_username VARCHAR(50),
    platform_link     VARCHAR(100),
    time              DATETIME,
    note              VARCHAR(150),
    trade_id          INTEGER,

    PRIMARY KEY (trade_id)
);

CREATE TABLE IF NOT EXISTS rl_garage_trade_contents
(
    trade_id            INTEGER,
    has_item_name       VARCHAR(50) NOT NULL,
    has_item_quantity   INTEGER     NOT NULL,
    has_item_rarity     VARCHAR(50) NOT NULL,
    has_item_color      VARCHAR(50) NOT NULL,

    wants_item_name     VARCHAR(50) NOT NULL,
    wants_item_quantity INTEGER     NOT NULL,
    wants_item_rarity   VARCHAR(50) NOT NULL,
    wants_item_color    VARCHAR(50) NOT NULL,

    content_ID          INTEGER,

    PRIMARY KEY (content_ID),
    FOREIGN KEY (trade_id) REFERENCES rl_garage_trade (trade_id) ON DELETE CASCADE,
    UNIQUE (has_item_name, has_item_quantity, has_item_rarity, has_item_color, wants_item_name, wants_item_quantity,
            wants_item_rarity, wants_item_color) ON CONFLICT IGNORE
);

-- queries

SELECT t.has_item_name                                  AS 'Item to sell',
       t.has_item_color                                 AS 'Item color',
       t.wants_item_quantity                            AS 'Credits wanted',
       rip.item_price_low                               AS 'Price low',
       rip.item_price_high                              AS 'Price high',
       t.wants_item_quantity * 1.0 / rip.item_price_low AS 'Factor',
       i.item_type,
       rgt.note,
       rgt.rlg_name,
       i.item_rarity,
       t.has_item_rarity
FROM rl_garage_trade_contents t
         INNER JOIN rl_insider_item i
                    ON i.item_name LIKE t.has_item_name
--                         AND i.item_rarity = t.has_item_rarity
         INNER JOIN rl_insider_prices rip
                    ON i.item_id = rip.item_id
                        AND rip.item_color LIKE t.has_item_color
         INNER JOIN rl_garage_trade rgt on t.trade_id = rgt.trade_id
WHERE t.wants_item_name LIKE 'Credits'
  AND Factor BETWEEN 0.3 AND 0.8
  AND t.wants_item_quantity > 1000
ORDER BY Factor;
