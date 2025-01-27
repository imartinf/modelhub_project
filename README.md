# Model Hub

![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![Gradio](https://img.shields.io/badge/Gradio-3.0.0-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3.36.0-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Model Hub** is a robust and user-friendly tool designed to manage, clone, and organize machine learning models efficiently. Leveraging the power of Python, Gradio, and SQLite, Model Hub provides a seamless interface for users to handle models from various sources, ensuring they are securely stored and easily accessible within a shared directory.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Permissions Handling](#permissions-handling)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **Clone Git Repositories:** Easily clone machine learning model repositories directly into a shared directory.
- **Copy Local Models:** Seamlessly copy local model directories to the shared storage with proper permissions.
- **Database Management:** Utilize SQLite to keep track of all models, their sources, paths, and metadata.
- **User-Friendly Interface:** Gradio-based web interface for intuitive interaction and management.
- **Secure Permissions:** Ensure that copied models have read-only permissions to maintain integrity.

## Technologies

- **Python 3.10:** The core programming language used for developing the application.
- **Gradio:** Provides a simple yet powerful web interface for interacting with the tool.
- **SQLite:** Lightweight, file-based database for managing model records.
- **Git:** Facilitates cloning of model repositories from platforms like GitHub.
- **Systemd:** Manages the application as a service for seamless deployment and uptime.

## Project Structure
```plaintext
modelhub_project/
├── modelhub_core/
│   ├── __init__.py
│   ├── config.py            # Configuration settings (paths, etc.)
│   ├── db_manager.py        # SQLite database interactions
│   └── modelhub_logic.py    # Core functionalities: clone, copy, protect
├── modelhub_app/
│   ├── __init__.py
│   └── main_app.py          # Gradio-based web interface
├── tests/
│   └── test_modelhub.py     # Automated tests using Pytest
├── .venv/                   # Python virtual environment
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
```

## Installation

Follow these steps to set up **Model Hub** on your local machine or server.

### Prerequisites

- **Python 3.10+** installed. You can download it from [Python's official website](https://www.python.org/downloads/).
- **Git** installed. Install it via your package manager or from [Git's official website](https://git-scm.com/downloads).
- **Systemd** for managing the application as a service (common in most Linux distributions).

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/<your_username>/modelhub_app.git
   cd modelhub_app
   ```

2. **Set Up a Virtual Environment**

   It’s recommended to use a virtual environment to manage dependencies.

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Initialize the Database**

   Ensure that the SQLite database is set up correctly.

   ```bash
   python -m modelhub_core.db_manager
   ```

## Configuration

Model Hub uses a configuration file to manage paths and other settings. By default, configurations are defined in modelhub_core/config.py. You can modify this file or use environment variables for customization.

### Configuration Options

- **Database Path**

  ```python
  DEFAULT_DB_PATH = "/var/modelhub/modelhub.db"
  DB_PATH = os.getenv("MODELHUB_DB_PATH", DEFAULT_DB_PATH)
  ```

- **Shared Directory**

  ```python
  DEFAULT_SHARED_DIR = "/autofs/thau00a/shared_models"
  SHARED_DIR = os.getenv("MODELHUB_SHARED_DIR", DEFAULT_SHARED_DIR)
  ```

### Environment Variables

You can override default settings by defining the following environment variables:

- **MODELHUB_DB_PATH:** Path to the SQLite database.
- **MODELHUB_SHARED_DIR:** Path to the shared directory where models are stored.

Example:

```bash
export MODELHUB_DB_PATH="/path/to/your/modelhub.db"
export MODELHUB_SHARED_DIR="/path/to/shared_models"
```

## Usage

Launch the application using the following command:

```bash
python -m modelhub_app.main_app
```

Alternatively, if you’ve set up Systemd as described in the Deployment section, the service will manage the application for you.

### Accessing the Interface

Once the application is running, open your web browser and navigate to:

```
http://<server_ip>:7860
```

Replace `<server_ip>` with the IP address of your server.

### Features in the Interface

1. **Clone from Git**
   - Enter the Git repository URL.
   - Click “Download Model” to clone and register the model.
2. **Copy Local Model**
   - Specify the local path of the model directory.
   - Optionally, provide a custom name.
   - Click “Copy Local Model” to copy and register the model.
3. **List Models**
   - View all registered models along with their details.

## Permissions Handling

To ensure Model Hub operates smoothly without sudo, users need to adjust directory permissions where models are stored.

### Adjusting Permissions

Users should set appropriate permissions for the shared directory to allow read and write access as needed.

Example:

```bash
# Change ownership to the user running Model Hub
sudo chown -R <username>:<group> /path/to/shared_models

# Set read and execute permissions
chmod -R 755 /path/to/shared_models
```

Note: Replace `<username>` and `<group>` with the appropriate user and group names.

## Testing

Model Hub includes automated tests to ensure functionality remains intact during development.

### Running Tests

1. **Activate the Virtual Environment**

   ```bash
   source .venv/bin/activate
   ```

2. **Install Testing Dependencies**

   Ensure pytest is installed.

   ```bash
   pip install pytest
   ```

3. **Execute Tests**

   ```bash
   pytest tests/test_modelhub.py -v
   ```

   This command runs the test suite with verbose output, providing detailed information about each test case.

### Test Cases

- **Clone New Model:** Tests cloning a new Git repository.
- **Clone Existing Model:** Ensures cloning an already registered repository is handled gracefully.
- **Copy Local Model:** Verifies copying a local directory works as expected.
- **List Models:** Confirms that all models are listed correctly in the database.

## Contributing

Contributions are welcome! To maintain quality and consistency, please follow the guidelines below.

### How to Contribute

1. **Fork the Repository**

   Click the “Fork” button at the top-right corner of the repository page to create a personal copy.

2. **Clone Your Fork**

   ```bash
   git clone https://github.com/<your_username>/modelhub_app.git
   cd modelhub_app
   ```

3. **Create a New Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Your Changes**

   Implement your feature or fix bugs.

5. **Commit Your Changes**

   ```bash
   git commit -m "Add feature: your feature description"
   ```

6. **Push to Your Fork**

   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**

   Navigate to the original repository and submit a pull request detailing your changes.

### Code Style

- Follow PEP 8 guidelines for Python code.
- Write clear and concise commit messages.
- Ensure all tests pass before submitting a pull request.

### Reporting Issues

If you encounter any issues or bugs, please open an issue in the repository with detailed information.

## License

This project is licensed under the MIT License.

## Contact

For any questions, suggestions, or support, please contact:

- **Name:** Your Name
- **Email:** your.email@example.com
- **GitHub:** @your_username

Thank you for using Model Hub! We hope it enhances your workflow and helps manage your machine learning models efficiently.

