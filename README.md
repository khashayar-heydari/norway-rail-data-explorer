# Norway Rail Data Explorer

A Python project for collecting and analysing Norwegian railway departure data using the Entur API.

I built this project to get more experience working with APIs, databases, data processing and Python.

## What it does

The program can:

- Search for Norwegian railway stations
- Fetch upcoming departures from Entur
- Show scheduled and expected departure times
- Store departure data in a SQLite database
- Avoid storing duplicate departures
- Calculate delays
- Compare delay statistics between stations
- Generate a graph of average delays using Matplotlib

## Project structure

```text
src/
├── entur_api.py
├── database.py
├── analysis.py
└── visualization.py