# Elite Search

A lightweight search engine built with Python and Flask. It indexes plain-text documents, ranks matches using a basic TF-IDF-inspired scoring approach, and serves a simple web interface for searching and uploading text files.

## Features

- Search across `.txt` files in a `documents/` directory
- Basic ranking based on term frequency and document frequency
- Highlighted snippets in the search results
- Upload document files through the browser
- Simple, polished UI with search and theme toggle

## Project structure

```text
.
├── project2.py        # Flask app and search engine implementation
├── requirements.txt   # Python dependencies (currently empty)
├── Procfile            # Heroku-style process definition
├── documents/         # Folder containing searchable text files
└── README.md          # Project overview and setup instructions
```

## Requirements

- Python 3.x
- Flask

## Setup

1. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

2. Install Flask:

```bash
pip install flask
```

3. Create a `documents/` directory and add text files to it:

```bash
mkdir -p documents
```

4. Run the app:

```bash
python project2.py
```

5. Open the app in your browser:

```text
http://localhost:5000
```

## Usage

### Search for content

- Enter a query in the search bar and click "Search".
- Matching documents are ranked and displayed with highlighted snippets.

### Upload documents

- Use the upload section on the homepage.
- Select a `.txt` file and click "Upload Now".
- The uploaded file is indexed immediately in memory.

## Notes

- The app stores indexed documents in memory, so uploaded files are not persisted across restarts.
- The app expects the `documents/` folder to exist and contain searchable `.txt` files.
- `requirements.txt` is intentionally left empty; you may want to populate it with project dependencies before deployment.

## Example deployment command

```bash
gunicorn project2:app
```

## License

This project does not currently include a license file. If you plan to distribute or deploy it publicly, consider adding an open-source license.
