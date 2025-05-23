# Capstone Project Proposal: Pokémon Catcher

## 1. Tech Stack

For this project, I will be using the **Python + Flask** stack for the backend, with a simple HTML/CSS/JavaScript frontend powered by Jinja templates. The database will be PostgreSQL, and I will use SQLAlchemy as the ORM.

- **Backend:** Python with Flask
- **Frontend:** HTML, CSS, JavaScript (Jinja2 templating)
- **Database:** PostgreSQL
- **Authentication & Security:** bcrypt (password hashing), Flask-Login (session management)
- **External API:** [Pokebase](https://github.com/PokeAPI/pokebase) wrapper for the PokéAPI

Since Flask requires the creation of a custom API, I will also build an internal API to handle user and favorites data.

---

## 2. Project Focus

The app will focus **primarily on frontend interactivity**, allowing users to search for and favorite Pokémon. The backend will handle user authentication, secure session management, and saving favorite Pokémon to a user-specific list, making it a meaningful full-stack project.

---

## 3. Platform

The initial version will be a **responsive web app** served via Flask. It will be accessible on both desktop and mobile browsers, with future potential for expansion into a PWA.

---

## 4. Project Goal

The goal is to build an interactive, user-friendly app for Pokémon fans. Users will be able to:

- Search for Pokémon by name
- View Pokémon details pulled from the PokéAPI
- Create an account and log in
- Save favorite Pokémon to their profile

---

## 5. Target Users

Target users include:

- Casual Pokémon fans
- Students or users interested in collecting or browsing Pokémon
- Anyone who wants a simple, customizable Pokédex experience

---

## 6. Data Handling & Collection

### External Data
- Pokémon data will be pulled from the PokéAPI using the Pokebase wrapper.

### Internal Data
User data will be stored in a PostgreSQL database using SQLAlchemy.

### Database Schema

#### Users
- `id` (PK)  
- `username`  
- `email`  
- `hashed_password`  
- `created_at`

#### Favorites
- `id` (PK)  
- `user_id` (FK)  
- `pokemon_name`  
- `saved_at`

#### (Optional) Pokemon
- `id` (PK)  
- `name`  
- `type`  
- `sprite_url`

---

### Potential Issues
- **API Rate Limiting:** May require caching of popular Pokémon to reduce requests to PokéAPI.
- **Security:** Passwords will be hashed using bcrypt; secure session management via Flask-Login.
- **Custom API:** Must ensure consistency and validation across internal API endpoints.

---

## Functionality Overview

- User signup and login
- Secure session-based authentication
- Search bar for Pokémon lookup
- Display Pokémon data using PokeAPI
- Add Pokémon to favorites (if logged in)
- View “My Favorites” page
- Base navigation: Home, Search, Favorites, Login/Signup

---

## User Flow

1. User visits the homepage
2. Can search for a Pokémon by name
3. If logged in, can add Pokémon to favorites
4. Can register or log in to manage favorites
5. Can view their personal favorites list
6. Can log out securely

---

## Stretch Goals / Beyond CRUD

- RESTful internal API (e.g., `/api/favorites`, `/api/user`)
- AJAX-based search suggestions
- Cache top 100 Pokémon locally
- Filter favorites by type or generation
- Dark mode toggle
- Shareable favorites page
- PWA/offline support

---

## Summary

**Pokémon Catcher** will be a clean, interactive, and secure web app that allows users to search, browse, and favorite Pokémon using the PokéAPI. It demonstrates practical full-stack development with Flask, including custom API routes, session handling, and third-party API integration — all within a fun, familiar theme.
