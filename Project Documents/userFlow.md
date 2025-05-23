# Pokémon Catcher – User Flow Document

## Overview

This document describes how users will navigate and interact with the Pokémon Catcher web application. It includes all major user interactions: signing up, logging in, searching for Pokémon, saving favorites, and viewing personalized data.

---

## 1. Landing Page (`/`)

### Description:
The homepage introduces the app and provides navigation options.

### Actions:
- Click “Search” to go to the Pokémon search page
- Click “Login” or “Sign Up” to authenticate
- If already logged in, click “Favorites” to view saved Pokémon
- Optionally display a featured Pokémon or tips

---

## 2. Signup Page (`/signup`)

### Description:
Allows new users to create an account.

### Form Inputs:
- Username
- Email
- Password (min length validation)

### Flow:
- User submits form
- Server hashes the password with bcrypt
- Creates a new user in the database
- Redirects to login or directly logs them in and redirects to homepage

---

## 3. Login Page (`/login`)

### Description:
Existing users log in with their credentials.

### Form Inputs:
- Email or Username
- Password

### Flow:
- User submits login form
- Credentials are validated against database
- On success, user is logged in via Flask session
- Redirects to homepage or previous page
- On failure, shows error message

---

## 4. Search Page (`/search`)

### Description:
Main interaction page where users search for Pokémon.

### Features:
- Search input field
- AJAX or form-based search submission
- Results pulled from PokéAPI via Pokebase
- Displays: name, sprite, type(s)

### Logged-In Users:
- Can click “Add to Favorites” next to Pokémon result
- Saves Pokémon name to `favorites` table with associated user ID

### Not Logged-In:
- Clicking "Add to Favorites" redirects to login page with a message

---

## 5. Favorites Page (`/favorites`)

### Description:
Personal dashboard showing Pokémon the user has favorited.

### Features:
- Displays list of favorited Pokémon (name, image, type)
- “Remove” button to delete from favorites
- Redirects to login if the user is not authenticated

---

## 6. Logout (`/logout`)

### Description:
Logs the user out and ends session.

### Flow:
- Flask session is cleared
- Redirects to homepage

---

## Optional Flow: Caching or Error States

### If PokéAPI is unreachable:
- Show a friendly error message
- Optionally fallback to local cache (if `pokemon` table is populated)

---

## User Scenarios

### 🧑 New User
1. Visits homepage
2. Clicks “Sign Up”
3. Completes registration
4. Redirected to homepage
5. Searches for a Pokémon
6. Clicks “Add to Favorites”
7. Pokémon appears in Favorites page

### 🔁 Returning User
1. Visits homepage
2. Clicks “Login”
3. Enters credentials
4. Searches or goes directly to Favorites
5. Removes or adds more Pokémon

### 🔒 Logged-Out User Tries to Favorite
1. Visits `/search`
2. Searches for Pokémon
3. Clicks “Add to Favorites”
4. Redirected to `/login` with message: “Please log in to save favorites.”

---

## Navigation Menu (Persistent)

- **Home**
- **Search**
- **Favorites** (if logged in)
- **Login / Sign Up** (if logged out)
- **Logout** (if logged in)

---

## Summary

This user flow ensures:
- A smooth onboarding process
- Clear access to core functionality (searching + saving)
- Protection of user-specific data
- Flexibility for future features like team-building, filtering, and profile customization
