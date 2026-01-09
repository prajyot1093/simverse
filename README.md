# Wave Interference and Diffraction Visualizer

A Streamlit-based physics simulation to visualize single-slit diffraction and double-slit interference patterns using real-time parameter controls.

## Features

- **Single-Slit Diffraction**: Visualize diffraction patterns with adjustable slit width and wavelength
- **Double-Slit Interference**: Explore interference patterns with customizable slit separation and width
- **Real-time Controls**: Interactive sliders to adjust wavelength, slit dimensions, and screen distance
- **Physics-based Calculations**: Accurate simulations using wave optics principles

## Tech Stack

- Python
- Streamlit
- NumPy
- Matplotlib

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd simverse
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application locally:
```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`.

## Deployment

This application is deployed on Streamlit Cloud. Visit the live demo at [https://simverse-yueg8vy86b4e88et6l2gxt.streamlit.app/].

## Physics Background

The visualizer implements fundamental wave optics equations:

- **Single-Slit Diffraction**: I = I₀ × (sin(β)/β)² where β = (π × a × sin(θ)) / λ
- **Double-Slit Interference**: Combines diffraction envelope with interference fringes

## License

MIT License
