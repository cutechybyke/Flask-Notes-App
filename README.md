# Flask Notes App

[![Flask CI](https://github.com/cutechybyke/Flask-Notes-App/actions/workflows/ci.yml/badge.svg)](https://github.com/cutechybyke/Flask-Notes-App/actions/workflows/ci.yml)

A lightweight notes application built with **Flask and SQLAlchemy**. It includes account registration, authentication and persistent user notes.

## Features

- User registration and login
- Password hashing with Werkzeug
- Flask-Login session management
- SQLite persistence through Flask-SQLAlchemy
- Blueprint-based application structure
- Authentication regression tests
- GitHub Actions CI

## Stack

Python · Flask · Flask-SQLAlchemy · Flask-Login · SQLite · Werkzeug

## Setup

```bash
git clone https://github.com/cutechybyke/Flask-Notes-App.git
cd Flask-Notes-App
python -m venv .venv
```

Activate the virtual environment, then install dependencies:

```bash
pip install -r requirements.txt
python main.py
```

## Tests

```bash
python -m unittest discover -s tests -v
```

The test suite covers registration behavior including successful account creation, duplicate email handling and password validation.

## Engineering improvements

The signup flow was corrected so a newly created account is authenticated using the actual persisted user object. Email normalization and safer form handling were added alongside regression tests and automated CI.
