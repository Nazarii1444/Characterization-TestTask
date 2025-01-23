# STDF File Editor Documentation

## Overview
This project is a web-based STDF (Standard Test Data Format) file editor.

#### It allows users to:

1. Upload a `.bin` STDF file and decode it.
2. View and edit the file's data in a table format.
3. Encode the modified data back into a `.bin` file for download.

---
## Installation
1. Clone the repo: `git clone https://github.com/Nazarii1444/Characterization-TestTask.git` and navigate into folder
2. Create Python virtual environment: `python -m venv venv`
3. Activate environment `source ./venv/bin/activate`
4. Install Python dependencies: `pip install -r requirements.txt`
5. Go to `http://localhost:8000/home`

---

## Features

- **Upload File**: Upload a `.bin` STDF file to the application.
- **Display Data**: Render the decoded data in a table with editable inputs.
- **Edit Data**: Modify test parameters directly in the table.
- **Download File**: Save the updated data as a new `.bin` file.
- **Docs**: Visit `http://localhost:8000/docs` for viewing documentation.

### Technologies Used
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: FastAPI

---

## Directory Structure
```plaintext
├── app
│   ├── api
│   │   └── endpoints
│   │       └── stdf.py
│   ├── schemas
│   │   └── stdf.py
│   ├── services
│   │   ├── decoder.py
│   │   └── encoder.py
│   ├── static
│   │   ├── css
│   │   │   └── styles.css
│   │   ├── html
│   │   │   └── index.html
│   │   ├── js
│   │       └── script.js
│   ├── config.py
│   └── main.py
```

---

## Implementation

### Frontend

#### `index.html` This file provides the UI for the application, allowing users to upload and edit `.bin` files.
- File upload and download buttons.
- Editable table for displaying and modifying file data.

#### `script.js` This JavaScript file handles file upload, data display, editing, and downloading functionality.

---

### Backend
- **GET `/`**: Returns "Hello World!"
- **GET `/home`**: Renders main web page

#### Endpoints for handling file decoding and encoding.

- **POST `/decode`**: Decodes a `.bin` file into JSON format.
- **POST `/encode`**: Encodes the updated JSON back into a `.bin` file.

---

## Usage Workflow

1. Open the web application at `http://localhost:8000/home`
2. Upload a `.bin` file using the **Upload File** options (you can use example of binary file in BIN folder)
3. Click `Upload File` button.
4. Edit the data displayed in the table.
5. Enter a filename for the updated file with `.bin` extension included.
6. Click `Download File` to save the modified `.bin` file.

## Binary file structure
The binary file is structured to store test data in a format inspired by the Standard Test Data Format (STDF). It consists of three types of records:
- MIR
- PRR
- PTR

Each record has a fixed structure with predefined fields.

Record Specifications:
- MIR (Master Information Record):

    - Header (4 bytes): ASCII string "MIR".
    - Temperature (4 bytes): 32-bit floating-point value.
    - Operator Name (20 bytes): ASCII string, padded with null bytes if less than 20 characters.

- PRR (Part Result Record):
    - Header (4 bytes): ASCII string "PRR".
    - Part Number (4 bytes): 32-bit integer.
    - Pass/Fail Status (1 byte): Integer value where 0 = Fail and 1 = Pass.

- PTR (Parametric Test Record):

  - Header (4 bytes): ASCII string "PTR".
  - Test Name (20 bytes): ASCII string, padded with null bytes if less than 20 characters.
  - Test Value (4 bytes): 32-bit floating-point value.
  - Low Limit (4 bytes): 32-bit floating-point value.
  - High Limit (4 bytes): 32-bit floating-point value.
  - Pass/Fail Status (1 byte): Integer value where 0 = Fail and 1 = Pass.

## Binary File Layout
```
[MIR Header] [Temperature] [Operator Name]
[PRR Header] [Part Number] [Pass/Fail Status]
[PTR Header] [Test Name] [Test Value] [Low Limit] [High Limit] [Pass/Fail Status]
[PRR Header] [Part Number] [Pass/Fail Status]
[PTR Header] [Test Name] [Test Value] [Low Limit] [High Limit] [Pass/Fail Status]
```