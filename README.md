# Mini Spotify Clone

## Description

Mini Spotify Clone is a music streaming web application built with Django that integrates with Spotify's API to display top artists, tracks, and audio details. It offers user authentication, music search functionality, and track playback with audio previews.

## Features

- **User Authentication**
  - Secure login and registration
  - User session management

- **Spotify API Integration**
  - Retrieve and display top artists and tracks
  - Search for tracks
  - Display track details, including preview audio and duration

- **User Interface**
  - Dynamic rendering with Django templates
  - Responsive design

## Technologies Used

- Django
- Spotify API
- HTML, CSS, JavaScript
- Requests
- dotenv

## Setup Instructions

1. Clone the repository:
    ```sh
    git clone https://github.com/kahenyamercy/mini_spotify.git
    cd mini_spotify
    ```

2. Create and activate a virtual environment:
    ```sh
    python3 -m venv myenv
    source myenv/bin/activate
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    - Create a `.env` file in the project root directory.
    - Add your Spotify API credentials:
        ```
        CLIENT_ID=your_spotify_client_id
        CLIENT_SECRET=your_spotify_client_secret
        ```

5. Run the development server:
    ```sh
    python manage.py runserver
    ```

6. Access the application in your browser at `http://localhost:8000`.

## Usage

- **Home Page**: Displays top artists and tracks.
- **Search**: Allows users to search for tracks.
- **Track Details**: Displays detailed information about a track, including a preview audio.
- **User Profile**: Displays user-specific information and top tracks for a selected artist.

## Code Overview

### `views.py`
- Handles the core logic for retrieving data from the Spotify API and rendering it in the templates.

### `templates/`
- Contains the HTML templates for rendering the web pages.

### `urls.py`
- Defines the URL routes for the application.

### `models.py`
- (Optional) Define any database models if needed.

## Demo

Check out the live demo [here](https://www.loom.com/share/7c4e8baf25dd4d60966d9498400720d2?sid=527c731e-e591-45e4-8180-22367de9e260).

## Repository

The source code is available on GitHub: [mini_spotify](https://github.com/kahenyamercy/mini_spotify)

## License

This project is licensed under the MIT License.

---

**Contributing**

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes.

**Contact**

For any questions or suggestions, feel free to contact me at [kahenyamercy5@gmail.com].

---

Thank you for checking out my project!
