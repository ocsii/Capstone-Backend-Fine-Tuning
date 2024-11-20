# Capstone - Fine Tuning Model on School Handbook Data: Fullstack Web Applicaation

## Project Overview

This project is a **Student Query Answering System** designed to provide accurate and concise responses to common student questions by leveraging a semi-fine-tuned language model. The goal is to simplify information retrieval from the school’s student handbook and other resources. It works by matching a student’s query to relevant sections in the handbook and generating an answer using AI models.

![image](https://github.com/user-attachments/assets/452b51f5-47da-4e86-bd99-a54632e6ca3b)

### Technical Stack

- **Backend**: FastAPI, FAISS, SentenceTransformers, and CrossEncoder models.
- **Frontend**: React, connecting to the backend via API calls.
- **Serverless GPT Integration**: AWS Lambda function handling OpenAI GPT API requests.

This project contains a **Backend API**, **Data Preparation scripts**, and a **Frontend React application**. Follow the instructions below to set up each component.

## Table of Contents

1. [Project Setup](#project-setup)
2. [Requirements](#requirements)
3. [Backend](#backend)
4. [Frontend](#frontend)
5. [Data Preparation](#data-preparation)

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

## Backend

This directory contains the backend API logic. Follow the steps below to set it up:

1. **Navigate to the Backend Directory**:

   - To run backend simultaneously, create a new powershell terminal

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
     uvicorn main:app --host 127.0.0.1 --port 8000 --reload
     ```

      or

     ```bash
     ./run.ps1
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
