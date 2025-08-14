# Box File Extractor API

This FastAPI app provides three endpoints to interact with Box files:

1. `/get-file-id`: Get the most recent file ID from a Box folder.
2. `/get-file-content`: Retrieve the content of a file by ID.
3. `/extract-columns`: Extract specific columns from CSV content.

## Deployment on Render

1. Push this project to a GitHub repository.
2. Create a new Web Service on [Render](https://render.com).
3. Set the environment to Python.
4. Use the start command: `uvicorn main:app --host 0.0.0.0 --port 10000`
5. Deploy and test your endpoints.
