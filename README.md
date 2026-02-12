# pda-pomodoro

A gentle Pomodoro timer designed to reduce pressure rather than increase it. This is a personal experiment built exploring “cute + accessible” focus tools. 

I’m inspired by pastel / retro pixel visual timers (the kind you find on YouTube), and I wanted to try making my own: something simple, calming, and easy on the eyes. This project also explores neurodivergence-friendly design choices, especially around low-pressure language and **PDA-aware** encouragement (PDA = Pathological Demand Avoidance). 

## Design Philosophy

I learn best by building real things that I actually want to use. 

This project started as a personal experiment: could I build a timer that felt calm, simple, and supportive rather than urgent or competitive?

Many productivity tools lean into pressure, streaks, and intensity. I wanted to explore the opposite — structure without stress or demand.

The result is a minimal Pomodoro timer. 

This project reflects both my interest in accessibility-aware design and my approach to learning tech: build something small, ship it, refine it.
---

## Features

- Default 25 / 5 Pomodoro cycle (fully customisable in Settings)
- Adjustable work and break durations
- Name each session with a specific goal or intention
- PDA-aware, low-pressure encouragement messages
- Theme switching (soft palettes)
- Mini always-on-top window (reduced visual clutter)
- Optional completion sound
- Settings saved locally (JSON)
---
## What I Learned

- Structuring a small Python application using classes
- Managing local state with JSON
- Handling assets (icons + audio) when packaging an executable
- Using PyInstaller / auto-py-to-exe to distribute a desktop app
- Thinking about UX choices, not just functionality

This project reflects my approach to learning tech: build something small, ship it, and refine it.

## Project Structure

```text
pda-pomodoro/
  src/
    pda_pomodoro.py
  assets/
    pocketwatch.ico
    <notification sound file>
  README.md
  LICENSE
  .gitignore
