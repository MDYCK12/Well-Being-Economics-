# FUNCTION CRETAING PLOTS BASED ON COUNTRY AND TYPE OF INDICATOR

def plot_series(df, country, indicator):
    """Plot time series for a specific country and indicator."""
    # Filter and prepare data
    data = df[(df["INDICATOR"]==indicator) & (df["COUNTRY"]==country)]
    years = [c for c in data.columns if str(c).isdigit() and len(str(c))==4]
    melted = data.melt(id_vars=['COUNTRY', 'INDICATOR'], value_vars=years, var_name='YEAR', value_name='VALUE')
    melted['YEAR'] = pd.to_numeric(melted['YEAR'])
    
    # Plot
    plt.figure(figsize=(12, 6))
    plt.plot(melted.sort_values('YEAR')['YEAR'], melted.sort_values('YEAR')['VALUE'], marker='o', linewidth=2)
    plt.title(f"{country} - {indicator}")
    plt.xlabel('Year'); plt.ylabel('Value'); plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    return melted.sort_values('YEAR')