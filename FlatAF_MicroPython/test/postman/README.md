# FlatAF Postman Testing Guide

This guide explains how to test the `web_server.py` Alpaca API controller using Postman. It provides instructions for setting up your environment, importing collections, and running tests.

## Table of Contents

- [FlatAF Postman Testing Guide](#flataf-postman-testing-guide)
  - [Table of Contents](#table-of-contents)
  - [Requirements](#requirements)
    - [Option 1: Postman Desktop App](#option-1-postman-desktop-app)
    - [Option 2: Postman Web App with Postman Agent](#option-2-postman-web-app-with-postman-agent)
  - [Setup Instructions](#setup-instructions)
  - [Using the Tests](#using-the-tests)
  - [Additional Notes](#additional-notes)
  - [Licensing](#licensing)

---

## Requirements

You can use either the Postman Desktop App or the Postman Web App with Agent:

### Option 1: Postman Desktop App
- [Download Postman Desktop](https://www.postman.com/downloads/)

### Option 2: Postman Web App with Postman Agent
- [Use Postman Web](https://web.postman.co/)
- [Download Postman Agent](https://www.postman.com/downloads/)

**Required Files (included in this directory):**
- `postman_environment.json`
- `postman_collection.json`

---

## Setup Instructions

1. **Open Postman**  
   Launch the Postman application on your desktop.

2. **Import the Environment**  
   - Drag and drop `postman_environment.json` into the **Environments** tab in the left sidebar.

3. **Import the Collection**  
   - Drag and drop `postman_collection.json` into the **Collections** tab in the left sidebar.

4. **Set Active Environment**  
   - In the upper-right dropdown, choose the environment labeled ``Environment Variables``

---

## Using the Tests

1. **Select the FlatAF API Collection**
   - Expand the imported collection in the sidebar.
   - You will see individual requests representing the controller endpoints in `web_server.py`.

2. **Run a Single Request**
   - Click a request.
   - Review or modify input parameters as needed.
   - Click **Send**.

3. **Run the Full Test Suite**
   - Click the collection name (**FlatAF API**).
   - Click the **▶ Run** button to launch the Collection Runner.
   - Ensure the correct environment is selected.
   - Click **Run FlatAF API Test Suite**

4. **Review Results**
   - Each test will report pass/fail status in the Collection Runner.
   - Postman uses `pm.test()` assertions to evaluate responses.

---

## Additional Notes

- These tests assume the FlatAF device is connected to the network and the `web_server.py` service is running and accessible via the IP in your environment.
- The UUID and other values in the environment file are placeholders and may be safely replaced as needed.
- Additional test coverage for edge cases will be provided by Alpaca ConformU compliance testing.

## Licensing
See the [FlatAF main project license](../../../LICENSE.md) for full licensing details.
