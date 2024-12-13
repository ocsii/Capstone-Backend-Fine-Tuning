# Capstone - Fine Tuning Model on School Handbook Data using Retrieval Augmented Generation (RAG): Fullstack Web Application

## Project Overview

This project is a **Student Query Answering System** designed to provide accurate and concise responses to common student questions by leveraging a semi-fine-tuned language model. The goal is to simplify information retrieval from the school’s student handbook and other resources. It works by matching a student’s query to relevant sections in the handbook and generating an answer using AI models.

![image](https://github.com/user-attachments/assets/a3390393-c9d2-46e3-b45e-855672190a41)

### Technical Stack

- **Backend**: FastAPI, FAISS, SentenceTransformers, and CrossEncoder models.
- **Frontend**: React, connecting to the backend via API calls.
- **Serverless GPT Integration**: AWS Lambda function handling OpenAI GPT API requests.

This project contains a **Backend API**, **Data Preparation scripts**, and a **Frontend React application**. Follow the instructions below to set up and run the entire project.

## Table of Contents

1. [Project Setup](#project-setup)
2. [Requirements](#requirements)
3. [Running the Project](#running-the-project)
   - [Step 1: Setting up the Backend](#step-1-setting-up-the-backend)
   - [Step 2: Setting up the Frontend](#step-2-setting-up-the-frontend)
4. [Data Preparation](#data-preparation)

---

## Project Setup

### Cloning the Project

To begin, clone this repository using Visual Studio Code (VS Code) or your preferred IDE.

1. **Download and Install VS Code**: <a href="https://code.visualstudio.com/download" target="_blank">Download Link</a>

2. **Clone the Repository**:

   - Open VS Code, go to **View** > **Terminal**.
   - In the terminal, navigate to the directory where you want to clone the project.
   - Run the following command:

     ```bash
     git clone git@github.com:ocsii/Capstone-Backend-Fine-Tuning.git
     ```

---

## Requirements

Make sure you have the following installed before proceeding:

- **Python** (version 3.8 or higher): <a href="https://www.python.org/downloads/" target="_blank">Download Link</a>
- **Node.js** (includes npm): <a href="https://nodejs.org/" target="_blank">Download Link</a>
- **Git** (for cloning the repository): <a href="https://git-scm.com/downloads" target="_blank">Download Link</a>

---

## Running the Project

### Step 1: Setting up the Backend

1. **Navigate to the Backend Directory**:

   - Open a terminal in VS Code (or your preferred IDE).
   - Run the following command to navigate to the backend folder:
     ```bash
     cd backend
     ```

2. **Set Up Virtual Environment**:

   - Run the setup script to initialize the virtual environment and install dependencies:
     ```powershell
     ./setup.ps1
     ```
   - If the `setup.ps1` script does not run, you can set up the environment manually:
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate
     pip install -r requirements.txt
     ```

3. **Run the Backend Server**:

   - Start the server by running:
     ```bash
     uvicorn main:app --host 127.0.0.1 --port 8000 --reload
     ```
   - Alternatively, you can use the provided script:
     ```bash
     ./run.ps1
     ```

4. **Keep the Backend Running**:

   - Leave this terminal open and running the backend server. You will need to open a new terminal for the frontend setup.

---

### Step 2: Setting up the Frontend

1. **Open a New Terminal**:

   - In VS Code, open a new terminal (you should leave the backend terminal running).

2. **Navigate to the Frontend Directory**:

   - In the new terminal, navigate to the frontend folder:
     ```bash
     cd frontend
     ```

3. **Install Dependencies**:

   - Run the following command to install the necessary React dependencies:
     ```bash
     npm install
     ```

4. **Run the Frontend Application**:

   - Start the frontend locally by running:
     ```bash
     npm run dev
     ```
   - Follow the link displayed in the terminal to open the locally hosted frontend in your browser.

5. **Ensure Both Backend and Frontend Are Running**:

   - At this point, you should have two terminals open:

     - One running the backend server.
     - One running the frontend React application.

   - Both need to run simultaneously for the application to work.

---

## Data Preparation

This section contains scripts to preprocess the data for the semantic search.

1. **Navigate to the Data Preparation Directory**:

   - Open a new terminal and navigate to the data-preparation folder:
     ```bash
     cd data-preparation
     ```

2. **Set Up Virtual Environment**:

   - Run the following command to initialize the virtual environment and install dependencies:
     ```powershell
     ./setup.ps1
     ```
   - If the `setup.ps1` script does not run, set up the environment manually:
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate
     pip install -r requirements.txt
     ```
