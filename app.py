"""
Wave Interference and Diffraction Visualizer
A Streamlit application for visualizing single-slit diffraction 
and double-slit interference patterns using physics-based calculations.
"""

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


def compute_single_slit_intensity(wavelength, slit_width, screen_distance, grid_size=500):
    """
    Compute single-slit diffraction intensity pattern.
    
    Physics equation: I = I0 * (sin(beta)/beta)^2
    where beta = (π * a * sin(θ)) / λ
    
    Using small-angle approximation: sin(θ) ≈ y / L
    where y is position on screen, L is screen distance
    
    Args:
        wavelength: Wavelength in nm
        slit_width: Slit width in μm
        screen_distance: Distance to screen in mm
        grid_size: Resolution of the 2D grid
    
    Returns:
        2D array of normalized intensity values (0-1)
    """
    # Convert units to consistent base (micrometers)
    wavelength_um = wavelength / 1000.0  # nm to μm
    screen_distance_um = screen_distance * 1000.0  # mm to μm
    
    # Create grid centered at origin
    max_y = 0.5 * screen_distance_um  # Half of screen distance for visual range
    y = np.linspace(-max_y, max_y, grid_size)
    x = np.linspace(-max_y, max_y, grid_size)
    Y, X = np.meshgrid(y, x)
    
    # Calculate distance from center (radial coordinate)
    r = np.sqrt(X**2 + Y**2)
    
    # Small-angle approximation: sin(θ) ≈ y / L
    sin_theta = r / screen_distance_um
    
    # Clip to valid range to avoid numerical issues
    sin_theta = np.clip(sin_theta, -0.99, 0.99)
    
    # Calculate beta parameter
    beta = (np.pi * slit_width * sin_theta) / wavelength_um
    
    # Avoid division by zero at center
    intensity = np.ones_like(beta)
    mask = beta != 0
    intensity[mask] = (np.sin(beta[mask]) / beta[mask])**2
    
    # Normalize to 0-1 range
    intensity = intensity / np.max(intensity)
    
    return intensity


def compute_double_slit_intensity(wavelength, slit_separation, screen_distance, grid_size=500):
    """
    Compute double-slit interference intensity pattern.
    
    Physics equation: I = I0 * cos^2(π * d * sin(θ) / λ)
    where d is slit separation, θ is angle
    
    Using small-angle approximation: sin(θ) ≈ y / L
    
    Args:
        wavelength: Wavelength in nm
        slit_separation: Distance between slits in μm
        screen_distance: Distance to screen in mm
        grid_size: Resolution of the 2D grid
    
    Returns:
        2D array of normalized intensity values (0-1)
    """
    # Convert units to consistent base (micrometers)
    wavelength_um = wavelength / 1000.0  # nm to μm
    screen_distance_um = screen_distance * 1000.0  # mm to μm
    
    # Create grid centered at origin
    max_y = 0.5 * screen_distance_um
    y = np.linspace(-max_y, max_y, grid_size)
    x = np.linspace(-max_y, max_y, grid_size)
    Y, X = np.meshgrid(y, x)
    
    # Calculate distance from center (radial coordinate)
    r = np.sqrt(X**2 + Y**2)
    
    # Small-angle approximation: sin(θ) ≈ y / L
    sin_theta = r / screen_distance_um
    
    # Clip to valid range
    sin_theta = np.clip(sin_theta, -0.99, 0.99)
    
    # Calculate phase difference
    phase_diff = (np.pi * slit_separation * sin_theta) / wavelength_um
    
    # Double-slit interference pattern
    intensity = np.cos(phase_diff)**2
    
    # Normalize to 0-1 range
    intensity = intensity / np.max(intensity)
    
    return intensity


def plot_intensity(intensity, title, wavelength, cmap='hot'):
    """
    Create a matplotlib figure showing the intensity pattern.
    
    Args:
        intensity: 2D array of intensity values
        title: Plot title
        wavelength: Wavelength in nm (for display)
        cmap: Colormap name
    
    Returns:
        matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=(8, 8), facecolor='#0e1117')
    ax.set_facecolor('#0e1117')
    
    # Display intensity as image
    im = ax.imshow(intensity, cmap=cmap, origin='lower', extent=[-1, 1, -1, 1])
    
    # Labels and title
    ax.set_xlabel('Position (normalized)', color='white', fontsize=11)
    ax.set_ylabel('Position (normalized)', color='white', fontsize=11)
    ax.set_title(f'{title}\nWavelength: {wavelength:.0f} nm', 
                 color='white', fontsize=13, fontweight='bold', pad=15)
    
    # Style colorbar
    cbar = plt.colorbar(im, ax=ax, label='Normalized Intensity')
    cbar.ax.tick_params(colors='white')
    cbar.set_label('Normalized Intensity', color='white')
    
    # Style tick labels
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_edgecolor('white')
    
    plt.tight_layout()
    
    return fig


def main():
    """Main Streamlit application."""
    # Page configuration
    st.set_page_config(
        page_title="Wave Interference and Diffraction Visualizer",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom styling for dark theme
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background-color: #0e1117;
        }
        [data-testid="stSidebar"] {
            background-color: #161b22;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Title
    st.title("🌊 Wave Interference and Diffraction Visualizer")
    st.markdown("---")
    
    # Sidebar controls
    st.sidebar.header("Parameters")
    
    # Wavelength slider (400-700 nm, visible spectrum)
    wavelength = st.sidebar.slider(
        "Wavelength (nm)",
        min_value=400,
        max_value=700,
        value=550,
        step=10,
        help="Visible spectrum range"
    )
    
    # Slit width slider
    slit_width = st.sidebar.slider(
        "Slit Width - a (μm)",
        min_value=0.5,
        max_value=10.0,
        value=5.0,
        step=0.5,
        help="Width of single slit for diffraction"
    )
    
    # Slit separation slider
    slit_separation = st.sidebar.slider(
        "Slit Separation - d (μm)",
        min_value=1.0,
        max_value=20.0,
        value=10.0,
        step=0.5,
        help="Distance between two slits for interference"
    )
    
    # Screen distance slider
    screen_distance = st.sidebar.slider(
        "Screen Distance - L (mm)",
        min_value=10,
        max_value=500,
        value=100,
        step=10,
        help="Distance from slits to observation screen"
    )
    
    st.sidebar.markdown("---")
    
    # Mode selection
    mode = st.sidebar.radio(
        "Visualization Mode",
        ("Single Slit Diffraction", "Double Slit Interference"),
        help="Choose which pattern to visualize"
    )
    
    # Compute intensity based on selected mode
    if mode == "Single Slit Diffraction":
        intensity = compute_single_slit_intensity(
            wavelength=wavelength,
            slit_width=slit_width,
            screen_distance=screen_distance
        )
        title = "Single-Slit Diffraction Pattern"
        description = (
            "Shows the diffraction pattern produced by a single slit. "
            "The central maximum is bright with progressively weaker secondary maxima. "
            "Narrower slits produce wider diffraction patterns."
        )
    else:  # Double Slit Interference
        intensity = compute_double_slit_intensity(
            wavelength=wavelength,
            slit_separation=slit_separation,
            screen_distance=screen_distance
        )
        title = "Double-Slit Interference Pattern"
        description = (
            "Shows the interference pattern produced by two slits. "
            "Bright fringes occur where waves constructively interfere, "
            "dark fringes where they destructively interfere. "
            "Closer slits produce finer fringe spacing."
        )
    
    # Display description
    st.info(description)
    
    # Create and display plot
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = plot_intensity(intensity, title, wavelength)
        st.pyplot(fig, use_container_width=True)
    
    with col2:
        st.subheader("Current Settings")
        st.write(f"**Wavelength:** {wavelength} nm")
        if mode == "Single Slit Diffraction":
            st.write(f"**Slit Width:** {slit_width} μm")
        else:
            st.write(f"**Slit Separation:** {slit_separation} μm")
        st.write(f"**Screen Distance:** {screen_distance} mm")
        
        st.markdown("---")
        st.subheader("Physics Notes")
        if mode == "Single Slit Diffraction":
            st.markdown("""
            **Formula:** $I = I_0 \\left(\\frac{\\sin(\\beta)}{\\beta}\\right)^2$
            
            **Where:** $\\beta = \\frac{\\pi a \\sin(\\theta)}{\\lambda}$
            
            - $a$ = slit width
            - $\\theta$ ≈ $y/L$ (small angle)
            - $\\lambda$ = wavelength
            """)
        else:
            st.markdown("""
            **Formula:** $I = I_0 \\cos^2\\left(\\frac{\\pi d \\sin(\\theta)}{\\lambda}\\right)$
            
            - $d$ = slit separation
            - $\\theta$ ≈ $y/L$ (small angle)
            - $\\lambda$ = wavelength
            """)


if __name__ == "__main__":
    main()
