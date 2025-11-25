# Streamlit Configuration

This directory contains Streamlit configuration files for the Portfolio Tracker dashboard.

## config.toml

The `config.toml` file sets the default theme and behavior for the Streamlit application.

### Theme Settings

- **Base Theme**: Light (white background)
- **Primary Color**: `#667eea` (purple-blue) - Used for buttons, links, and interactive elements
- **Background Color**: `#ffffff` (pure white) - Main content area background
- **Secondary Background**: `#f8fafc` (light gray) - Sidebar and widget backgrounds
- **Text Color**: `#1e293b` (dark slate) - High contrast for readability<>
- **Font**: Sans serif - Clean, professional appearance

### Server Settings

- **CORS**: Disabled (for local development)
- **Max Upload Size**: 200 MB
- **XSRF Protection**: Disabled (for local use)

### Browser Settings

- **Usage Stats**: Disabled (privacy)

### How to Modify

To customize the theme, edit `.streamlit/config.toml` and adjust the values under `[theme]`:

```toml
[theme]
base = "light"                              # or "dark"
primaryColor = "#667eea"                    # Accent color
backgroundColor = "#ffffff"                  # Main background
secondaryBackgroundColor = "#f8fafc"        # Sidebar/widgets
textColor = "#1e293b"                       # Text color
font = "sans serif"                         # Font family
```

### Applying Changes

After modifying the configuration:
1. Stop the dashboard (Ctrl+C)
2. Restart: `./run_dashboard.sh`
3. Refresh your browser (Cmd+R / Ctrl+R)

### References

- [Streamlit Theme Documentation](https://docs.streamlit.io/library/advanced-features/theming)
- [Streamlit Configuration Options](https://docs.streamlit.io/library/advanced-features/configuration)

