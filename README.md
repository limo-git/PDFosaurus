# Dinosaur in a PDF

A fully interactive, self-contained T-Rex game embedded directly inside a PDF using low-level PDF syntax and embedded JavaScript. No external tools, no dependencies—just raw PDF internals powering an interactive experience inside Adobe Acrobat.
Try it out: https://github.com/limo-git/PDFosaurus/blob/main/dinosaur_game.pdf
## Features

- **Pure PDF Syntax:** Built using low-level PDF object structures, including form fields and annotations.
- **Embedded JavaScript:** Game logic, interactions, and UI are powered by Acrobat's built-in JavaScript engine.
- **No External Dependencies:** Runs entirely within Adobe Acrobat without requiring any plugins.
- **Customizable UI:** Modify button placements, colors, and game elements directly in the PDF structure.

## How It Works

- **Form Fields as Game Elements:** The playing field and pixels are represented as PDF form fields with specific attributes.
- **JavaScript for Game Logic:** Functions such as `jump()`, `initialize_game()`, and `restart_game()` control the game flow.
- **Button-Driven Interactions:** Buttons are linked to JavaScript actions that modify game state dynamically.
- **PDF Rendering Rules:** Elements are positioned using absolute coordinates within the PDF page structure.

## Code Overview

- **`PLAYING_FIELD_OBJ`** – Defines the main game canvas as a PDF annotation.
- **`PIXEL_OBJ`** – Represents each pixel in the game as an interactive field.
- **`BUTTON_OBJ`** – Buttons for actions like jumping and restarting.
- **`STREAM_OBJ`** – Stores JavaScript execution logic.
- **`add_button()` & `add_text()`** – Helper functions for adding UI elements dynamically.

## Running the Game

1. Open the generated PDF in **Adobe Acrobat Reader** (not all viewers support embedded JavaScript).
2. Click the **Start Game** button to initialize the gameplay.
3. Use the **Jump** button to control the dino.
4. Restart the game anytime with the **Restart** button.

## Why This Matters

This project demonstrates the powerful, often overlooked capabilities of PDFs as an interactive medium. It showcases how form fields, annotations, and embedded JavaScript can be leveraged beyond traditional document handling, opening possibilities for **advanced automation, security workflows, and creative applications**.

This works in **PDFium (Chromium-based browsers)** and **PDF.js (Firefox)**. It is not tested for or intended to function in other engines (though modifications might make it work in Acrobat).
