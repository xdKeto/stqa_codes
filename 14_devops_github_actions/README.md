# Continuous Integration Pipeline using GitHub Actions

We are going to build a Continuous Integration (CI) Pipeline using GitHub Actions. By the end of this lab, we will have a "Robot" that automatically:
1. Lints our code (checks for style errors) every time we push.
2. Tests our code every time we push.
3. Badges our repository to show off our build status.

To start, it is highly recommended that you create a new repository on your local machine, and an empty repository with the same name in your own GitHub account. Many features are only possible when you have your own account.

## Part 1: Prepare Your Project for Automation

1. GitHub Actions needs a set of instructions to know what software to install. We provide this via a requirements.txt file. Ensure you have a file named `requirements.txt` in the project root. The file should contain at least the following necessary tools:
    ```
    flask
    pytest
    flake8
    ```
2. Copy the pet shop app from this directory to your project root:
    ```
    |- templates/
        |- index.html
    |- app.py
    ```
3. Commit these initial files to your local repository:
    ```
    git add .
    git commit -m "Initial commit"
    ```
4. If you have not created a GitHub repository, create an empty one at GitHub. Afterwards, push the local repository into GitHub:
    ```
    git remote add origin YOUR_REPOSITORY_LINK
    git branch -M main
    git push origin main
    ```

## Part 2: Create the Pipeline (The "Workflow")

GitHub looks for special instructions in a folder named `.github`.

1. Inside your project folder, create these nested folders:
    ```
    |- .github/
        |- workflows/
    ```
2. Inside `.github/workflows/`, create a file named `ci.yaml`.
3. For now, create a "Hello World" version of a YAML file to test that the workflow runs properly. Copy the following code into `ci.yaml`.

    ```yaml
    name: CI Pipeline

    on: [push]

    jobs:
    build:
        runs-on: ubuntu-latest
        
        steps:
        - name: Say Hello
            run: echo "The pipeline is working!"
    ```
4. Commit and push the file.
5. Directly after pushing, go to the `Actions` tab at GitHub and observe the workflow running.

## Part 3: Linting

We are going to implement static analysis using a linter called `flake8` to catch bad code styles before we even check if it works.

1. Modify `ci.yaml`: Update the steps section to check out the code and set up Python.
    ```yaml
    steps:
      - name: Checkout Code
        uses: actions/checkout@v3   # Downloads the code to the runner

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    ```
2. Add a step to run the linter in the steps part of the `ci.yaml` file.
    ```yaml
      - name: Lint with Flake8
        run: flake8 . --count --select=E1,F4 --show-source --statistics
    ```
3. Commit and push the code to GitHub.
4. Go to the `Actions` tab in GitHub, and observe the results.
5. Fix the styling errors found by the linter, push the new code back to GitHub, and repeat until there are no styling errors.

## Part 4: Unit Testing

1. Copy the unit tests from this directory to your project root.
    ```
    |- tests/
        |- test_app.py
    |- pytest.ini
    ```
2. Add a step to run pytest in the steps part of the `ci.yaml` file.
    ```yaml
      - name: Run Unit Tests
        run: pytest
    ```
3. Commit and push the code to GitHub.
4. Go to the `Actions` tab in GitHub, and observe the results.
5. Fix the failing unit tests, push the new code back to GitHub, and repeat until all tests pass.
