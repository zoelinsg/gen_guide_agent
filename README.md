# History Research Desk

History Research Desk is a focused AI assistant for historical research and storytelling, built with Google ADK and Gemini.

It helps users explore historical figures, events, artifacts, and timeline comparisons through natural language questions. The assistant uses Wikipedia as a grounding source and returns concise, documentary-style answers for learning and exploration.

## Overview

This project is designed as a single-purpose history research assistant rather than a general chatbot.

Its goal is to make historical topics easier to understand by combining:
- fact lookup for historical context
- concise structured summaries
- story-friendly explanations
- lightweight learning guidance

## Features

- Historical question answering
- Historical figure and event lookup
- Era and timeline comparison
- Artifact background and current location
- Book recommendations
- Study suggestions
- Concise documentary-style summaries
- Optional mini story mode for historical figure prompts

## How It Works

The system follows a simple research-and-format workflow:

1. Collect historical background information from Wikipedia
2. Organize the findings into a concise and readable answer

The response is designed to be structured, skimmable, and suitable for learning.

## Example Questions

- Tell me about Qin Shi Huang.
- Were Napoleon and George Washington in the same era?
- Recommend three books for learning Roman history.
- How should I start studying Chinese history?
- What is the Rosetta Stone and where is it now?
- Did Japanese writing take influence from Chinese writing?

## Tech Stack

- Google ADK
- Gemini
- Python
- Wikipedia via LangChain community tools
- Google Cloud Logging
- Cloud Run for deployment

## Project Scope

This project focuses on historical research and explanation.

It does not provide:
- real-time news
- academic database access
- primary-source verification
- guaranteed scholarly completeness

## Why This Project

I have always enjoyed listening to historical stories and learning about fascinating people, events, and cultures from the past.

This project was inspired by the idea of building a companion-like history assistant that can:
- answer historical questions
- tell story-driven summaries
- recommend ways to learn more
- make history feel more approachable and engaging

## Deployment

This project is designed to be deployed as an HTTP-callable AI agent on Cloud Run.

## Notes

- Wikipedia is used as the main grounding source.
- Responses are designed to be concise, structured, and easy to read.
- This project is intended for demo, learning, and exploratory use.

## Demo
[▶ Watch Demo on YouTube](https://youtu.be/mrNPT4sVOBo)

[![Demo Video](https://img.youtube.com/vi/mrNPT4sVOBo/0.jpg)](https://youtu.be/mrNPT4sVOBo)

## License
MIT License