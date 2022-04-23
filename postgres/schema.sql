CREATE TABLE IF NOT EXISTS users (
    id serial PRIMARY KEY,
    nickname varchar(32) NOT NULL,
    img_url varchar(256),
    sex varchar(1) NOT NULL,
    email varchar(64) NOT NULL,
    password varchar NOT NULL,
    is_superuser boolean NOT NULL
);

CREATE TABLE IF NOT EXISTS games (
    id serial PRIMARY KEY,
    status varchar,
    start_date TIMESTAMP WITHOUT TIME ZONE,
    end_date TIMESTAMP WITHOUT TIME ZONE
);

CREATE TABLE IF NOT EXISTS users_games  (
    user_id INT NOT NULL,
    game_id INT NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (game_id) REFERENCES games(id),
    UNIQUE (user_id, game_id)
);
