# Capstone - Fine Tuning Model on School Handbook Data - Fullstack Web Applicaation

This project contains a **Backend API**, **Data Preparation scripts**, and a **Frontend React application**. Follow the instructions below to set up each component.

## Table of Contents

1. [Project Setup](#project-setup)
2. [Requirements](#requirements)
3. [Backend](#backend)
4. [Data Preparation](#data-preparation)
5. [Frontend](#frontend)
6. [Troubleshooting](#troubleshooting)
7. [Resources](#resources)

---

## Project Setup

### Cloning the Project

To begin, clone this repository using Visual Studio Code (VS Code) or your preferred IDE.

1. **Download and Install VS Code**: [Download Link](https://code.visualstudio.com/download)
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

- **Python** (version 3.8 or higher): [Download Link](https://www.python.org/downloads/)
- **Node.js** (includes npm): [Download Link](https://nodejs.org/)
- **Git** (for cloning the repository): [Download Link](https://git-scm.com/downloads)

---

## Backend

This directory contains the backend API logic. Follow the steps below to set it up:

1. **Navigate to the Backend Directory**:

   ```bash
   cd backend
   ```

2. **Setup Virtual Environment**:

   - Run the following command to initialize the virtual environment and install dependencies:
     ```powershell
     ./setup.ps1
     ```
   - If the `setup.ps1` script does not run, you can set up the environment manually with these commands:
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate
     pip install -r requirements.txt
     ```

3. **Run the Backend Server**:
   - Start the server by running:
     ```bash
     uvicorn queryLambdaRender:app --host 127.0.0.1 --port 8000 --reload
     ```
   - Ensure you are in the /backend directory before running the command

---

## Frontend

The frontend is a React application that serves as the user interface.

1. **Navigate to the Frontend Directory**:

   ```bash
   cd frontend
   ```

2. **Install Dependencies**:

   - Run the following command to install the necessary React dependencies:
     ```bash
     npm install
     ```

3. **Run the Frontend Application**:
   - Start the frontend locally with:
     ```bash
     npm run dev
     ```
   - Follow the link in the terminal to open locally hosted frontend.

---

## Data Preparation

Boring section - It contains scripts to preprocess the data for the semantic search.

1. **Navigate to the Data Preparation Directory**:

   ```bash
   cd data-preparation
   ```

2. **Setup Virtual Environment**:

   - Run the following command to initialize the virtual environment and install dependencies:
     ```powershell
     ./setup.ps1
     ```
   - If the `setup.ps1` script does not run, you can set up the environment manually with these commands:
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate
     pip install -r requirements.txt
     ```

---
