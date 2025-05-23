# Pokémon Catcher – Schema Design Document

## Overview

This schema supports a web application where users can search for Pokémon via the PokéAPI and save their favorites after signing up and logging in. The schema supports user authentication, many-to-many relationships (via favorites), and optional Pokémon caching.

---

## Tables

### 1. `users`

Stores account and authentication data for each user.

| Field           | Type      | Constraints                      | Description                        |
|----------------|-----------|----------------------------------|------------------------------------|
| id             | INTEGER   | PRIMARY KEY, SERIAL              | Unique identifier for each user    |
| username       | TEXT      | NOT NULL, UNIQUE                 | Display name of the user           |
| email          | TEXT      | NOT NULL, UNIQUE                 | Used for account login             |
| hashed_password| TEXT      | NOT NULL                         | Hashed password using bcrypt       |
| created_at     | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP        | Timestamp of account creation      |

---

### 2. `favorites`

Stores a record for each favorited Pokémon by a user. This supports a many-to-many relationship between `users` and Pokémon (via name or ID).

| Field        | Type      | Constraints                      | Description                           |
|-------------|-----------|----------------------------------|---------------------------------------|
| id          | INTEGER   | PRIMARY KEY, SERIAL              | Unique favorite record ID             |
| user_id     | INTEGER   | FOREIGN KEY → users(id), NOT NULL| The user who favorited the Pokémon    |
| pokemon_name| TEXT      | NOT NULL                         | Name of the Pokémon favorited         |
| saved_at    | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP        | When the Pokémon was favorited        |

> **Note:** This does not enforce uniqueness of the `pokemon_name` itself — a user can favorite any number of Pokémon, and multiple users can favorite the same one.

---

### 3. (Optional) `pokemon`

Used for local caching of popular Pokémon to improve performance or provide offline fallback.

| Field      | Type    | Constraints           | Description                        |
|-----------|---------|-----------------------|------------------------------------|
| id        | INTEGER | PRIMARY KEY, SERIAL   | Internal Pokémon ID                |
| name      | TEXT    | NOT NULL, UNIQUE      | Pokémon name                       |
| sprite_url| TEXT    |                       | URL of the Pokémon sprite image    |
| type      | TEXT[]  |                       | Array of Pokémon type(s)           |

> This table is optional and can be used if rate limits from the external API become an issue or if you want to prefetch common Pokémon data.

---

## Entity Relationship Diagram (ERD)

