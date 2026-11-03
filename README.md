# Test assignment: Working with Data and PostgreSQL

---

## Get started

1. Clone the repository
```bash
    git clone git@github.com:ilrosch/db-task.git
    cd db-task
```

2. Configure environment variables (database)
```bash
    cp .env.example .env
    # Open .env and fill in your values
```

3. Install dependencies
    - uv:
    ```bash
        uv sync
    ```
    - pip:
    ```bash
        python -m venv .venv && source .venv/bin/activate
        # (For Windows use \.venv\Scripts\activate)
        pip install -r requirements.txt
    ```

4. Run
```bash
   python main.py
```