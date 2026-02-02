import streamlit as st
import numpy as np
import pandas as pd

st.title("🏠 Home Price Normal Distribution Simulator")

# 1) Population distributions
st.header("1) Population Price Distributions")

# Sidebar inputs for population distributions
st.sidebar.subheader("Population Distribution Parameters")

pop_mean_starter = st.sidebar.slider("Starter Homes Mean", 50_000, 500_000, 200_000, step=10_000)
pop_std_starter  = st.sidebar.slider("Starter Homes Std Dev", 10_000, 200_000, 50_000, step=5_000)

pop_mean_intermediate = st.sidebar.slider("Intermediate Homes Mean", 200_000, 1_000_000, 450_000, step=20_000)
pop_std_intermediate  = st.sidebar.slider("Intermediate Homes Std Dev", 20_000, 300_000, 75_000, step=5_000)

pop_mean_luxury = st.sidebar.slider("Luxury Homes Mean", 500_000, 5_000_000, 1_500_000, step=50_000)
pop_std_luxury  = st.sidebar.slider("Luxury Homes Std Dev", 50_000, 500_000, 150_000, step=10_000)

# Price grid for plotting distributions
x = np.linspace(0, 6_000_000, 1500)

# Build PDFs
pdf_starter = (1/(pop_std_starter*np.sqrt(2*np.pi))) * np.exp(-0.5*((x - pop_mean_starter)/pop_std_starter)**2)
pdf_intermediate = (1/(pop_std_intermediate*np.sqrt(2*np.pi))) * np.exp(-0.5*((x - pop_mean_intermediate)/pop_std_intermediate)**2)
pdf_luxury = (1/(pop_std_luxury*np.sqrt(2*np.pi))) * np.exp(-0.5*((x - pop_mean_luxury)/pop_std_luxury)**2)

# Plot population distributions
pop_df = pd.DataFrame({
    "Price": x,
    "Starter Population": pdf_starter,
    "Intermediate Population": pdf_intermediate,
    "Luxury Population": pdf_luxury
})
st.line_chart(pop_df.set_index("Price"))

# 2) For‑sale distributions
st.header("2) For‑Sale Distribution Parameters (Multipliers)")

st.sidebar.subheader("For Sale Dist Multipliers")

mult_mean_starter  = st.sidebar.slider("Starter Mean Multiplier", 0.5, 1.5, 1.0, step=0.05)
mult_std_starter   = st.sidebar.slider("Starter Std Dev Multiplier", 0.2, 2.0, 1.0, step=0.05)

mult_mean_inter = st.sidebar.slider("Intermediate Mean Multiplier", 0.5, 1.5, 1.0, step=0.05)
mult_std_inter  = st.sidebar.slider("Intermediate Std Dev Multiplier", 0.2, 2.0, 1.0, step=0.05)

mult_mean_luxury = st.sidebar.slider("Luxury Mean Multiplier", 0.5, 1.5, 1.0, step=0.05)
mult_std_luxury  = st.sidebar.slider("Luxury Std Dev Multiplier", 0.2, 2.0, 1.0, step=0.05)

# Compute sale distributions
sale_mean_starter = pop_mean_starter * mult_mean_starter
sale_std_starter  = pop_std_starter  * mult_std_starter

sale_mean_inter = pop_mean_intermediate * mult_mean_inter
sale_std_inter  = pop_std_intermediate  * mult_std_inter

sale_mean_luxury = pop_mean_luxury * mult_mean_luxury
sale_std_luxury  = pop_std_luxury  * mult_std_luxury

# PDFs for for-sale
pdf_sale_starter = (1/(sale_std_starter*np.sqrt(2*np.pi))) * np.exp(-0.5*((x - sale_mean_starter)/sale_std_starter)**2)
pdf_sale_inter = (1/(sale_std_inter*np.sqrt(2*np.pi))) * np.exp(-0.5*((x - sale_mean_inter)/sale_std_inter)**2)
pdf_sale_lux = (1/(sale_std_luxury*np.sqrt(2*np.pi))) * np.exp(-0.5*((x - sale_mean_luxury)/sale_std_luxury)**2)

# Plot for-sale distributions
sale_df = pd.DataFrame({
    "Price": x,
    "Starter For‑Sale": pdf_sale_starter,
    "Intermediate For‑Sale": pdf_sale_inter,
    "Luxury For‑Sale": pdf_sale_lux
})
st.line_chart(sale_df.set_index("Price"))

# 3) Display summary of parameters
st.header("Summary of Distribution Parameters")
st.write("""
**Population Distributions**  
- Starter: mean = {:,}, std = {:,}  
- Intermediate: mean = {:,}, std = {:,}  
- Luxury: mean = {:,}, std = {:,}  
""".format(
    pop_mean_starter, pop_std_starter,
    pop_mean_intermediate, pop_std_intermediate,
    pop_mean_luxury, pop_std_luxury
))

st.write("""
**For‑Sale Distributions (Derived)**  
- Starter: mean = {:,} ({:.0%} of pop), std = {:,} ({:.0%} of pop)  
- Intermediate: mean = {:,} ({:.0%} of pop), std = {:,} ({:.0%} of pop)  
- Luxury: mean = {:,} ({:.0%} of pop), std = {:,} ({:.0%} of pop)  
""".format(
    sale_mean_starter, mult_mean_starter, sale_std_starter, mult_std_starter,
    sale_mean_inter, mult_mean_inter, sale_std_inter, mult_std_inter,
    sale_mean_luxury, mult_mean_luxury, sale_std_luxury, mult_std_luxury
))
st.header("📋 Counts and Overall Averages")

# Editable table for counts of homes
count_df = pd.DataFrame({
    "Category": ["Starter", "Intermediate", "Luxury"],
    "Population Count": [1000000, 2000000, 500000],  # initial guesses
    "For-Sale Count": [50000, 80000, 20000]
})

edited = st.data_editor(count_df, num_rows="fixed")
st.write("### Enter counts for each category (population and for‑sale)")

# Extract counts
pop_counts = edited["Population Count"].values
sale_counts = edited["For-Sale Count"].values

# Compute weighted average prices for populations
# (simple weighted means of distribution means using counts)
pop_means = np.array([pop_mean_starter, pop_mean_intermediate, pop_mean_luxury])
sale_means = np.array([sale_mean_starter, sale_mean_inter, sale_mean_luxury])

total_pop   = pop_counts.sum()
total_sale  = sale_counts.sum()

weighted_pop_avg  = (pop_means * pop_counts).sum() / total_pop if total_pop > 0 else np.nan
weighted_sale_avg = (sale_means * sale_counts).sum() / total_sale if total_sale > 0 else np.nan

st.markdown(f"### 📌 Weighted Average Prices")
st.write(f"**Population average price:** ${weighted_pop_avg:,.0f}")
st.write(f"**For‑Sale average price:** ${weighted_sale_avg:,.0f}")

# Plot combined comparison charts
st.header("📈 Population vs For‑Sale Distributions by Category")

# Helper function to build DataFrame for each category
def build_dist_df(x_vals, pop_pdf, sale_pdf):
    return pd.DataFrame({
        "Price": x_vals,
        "Population": pop_pdf,
        "For Sale": sale_pdf
    })

# Starter
starter_chart_df = build_dist_df(x, pdf_starter, pdf_sale_starter)

#st.subheader("Starter Homes")
#st.line_chart(starter_chart_df.set_index("Price"))

# Intermediate
inter_chart_df = build_dist_df(x, pdf_intermediate, pdf_sale_inter)
#st.subheader("Intermediate Homes")
#st.line_chart(inter_chart_df.set_index("Price"))

# Luxury
luxury_chart_df = build_dist_df(x, pdf_luxury, pdf_sale_lux)
#st.subheader("Luxury Homes")
#st.line_chart(luxury_chart_df.set_index("Price"))

st.header("📈 Population vs For‑Sale Distributions by Category (Side‑by‑Side)")

# Create three columns
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Starter Homes")
    st.line_chart(starter_chart_df.set_index("Price"))

with col2:
    st.subheader("Intermediate Homes")
    st.line_chart(inter_chart_df.set_index("Price"))

with col3:
    st.subheader("Luxury Homes")
    st.line_chart(luxury_chart_df.set_index("Price"))

