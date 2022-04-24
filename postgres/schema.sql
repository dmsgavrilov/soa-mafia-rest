CREATE TABLE IF NOT EXISTS users (
    id serial PRIMARY KEY,
    nickname varchar(32) NOT NULL,
    img_url varchar(256),
    sex varchar(1) NOT NULL,
    email varchar(64) NOT NULL UNIQUE,
    password varchar NOT NULL,
    is_superuser boolean NOT NULL
);

CREATE TABLE IF NOT EXISTS games (
    id serial PRIMARY KEY,
    status varchar,
    start_date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    end_date TIMESTAMP WITHOUT TIME ZONE NOT NULL
);

CREATE TABLE IF NOT EXISTS users_games  (
    id serial PRIMARY KEY,
    user_id INT NOT NULL,
    game_id INT NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE,
    UNIQUE (user_id, game_id)
);
