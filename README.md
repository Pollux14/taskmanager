# Task Manager

This repository contains our project for a simple **Distributed Task Manager** application. Built as a full-stack app with separate frontend and backend services, the project demonstrates **Docker containerization** and orchestration with **Docker Compose**.

---

## Project Overview

The **Task Manager** allows users to **create, read, update, and delete tasks** through a clean web interface. Each task includes:

1. **Title**
2. **Description**
3. **Status** (Pending, In-Progress, Completed)

The application consists of:

1. **Backend** – Python Flask REST API (serving data in memory)
2. **Frontend** – HTML, CSS, JavaScript
3. **Deployment** – Docker & Docker Compose

---

## Features

1. **Web Interface**  
   Users can view all tasks in a clean dashboard.
2. **Add New Tasks**  
   Create a task by entering a title, description, and selecting a status.
3. **Edit or Delete Tasks**  
   Update task information or remove tasks as needed.
4. **Status Display**  
   Visual badges indicate whether a task is Pending, In-Progress, or Completed.
5. **In-Memory Data Handling**  
   All CRUD operations are handled in memory (no persistent database).

---

## Technologies Used

- **Python Flask** – Backend API
- **HTML / CSS / JavaScript** – Frontend
- **Docker** – Containerization
- **Docker Compose** – Service orchestration

---

## Key Features

1. **Dockerized Deployment**  
   Backend and frontend run in isolated containers.
2. **Task CRUD Operations**  
   Create, update, and delete tasks in real time (in memory).
3. **Simple Web UI**  
   Clean, responsive task dashboard.

---

