import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def plot_temp_predictions(history_df, current_pred=None):
    """
    Plot historical temperature trend and current prediction point.
    """
    fig = px.line(history_df, x='sol', y='avg_temp', title='Historical Mars Temperature (Avg)',
                  labels={'sol': 'Sol (Martian Day)', 'avg_temp': 'Temperature (C)'})
    
    if current_pred is not None:
        # Add a marker for the prediction
        # We don't have a specific 'sol' for prediction roughly, just place it on the side or overlay
        fig.add_hline(y=current_pred, line_dash="dash", line_color="red", annotation_text=f"Pred: {current_pred:.1f}C")
    
    fig.update_layout(template="plotly_dark")
    return fig

def plot_neo_scatter(neo_data):
    """
    Scatter plot of Near Earth Objects: Miss Distance vs Relative Velocity
    Sized by Diameter.
    """
    if not neo_data:
        return go.Figure()
        
    df = pd.DataFrame(neo_data)
    
    fig = px.scatter(df, x="miss_distance_km", y="velocity_kph", 
                     size="diameter_min_km", color="hazardous",
                     hover_data=["name", "close_approach_date"],
                     title="Near Earth Objects (NEO) - Approach Data",
                     labels={"miss_distance_km": "Miss Distance (km)", "velocity_kph": "Relative Velocity (kph)"},
                     color_discrete_map={True: "red", False: "cyan"})
    
    fig.update_layout(template="plotly_dark")
    return fig
