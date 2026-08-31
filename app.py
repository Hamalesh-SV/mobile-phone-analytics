import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Mobile Phone Analytics",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main-title {
    font-size: 40px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: gray;
    font-size: 17px;
    margin-bottom: 30px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    return pd.read_csv("mobile_phones.csv")


df = load_data()


# =========================================================
# TITLE
# =========================================================

st.markdown(
    '<div class="main-title">Mobile Phone Analytics Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Explore mobile phone prices, brands, specifications, ratings and reviews'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.title("Filters")

st.sidebar.markdown("---")


# Brand filter

brands = st.sidebar.multiselect(
    "Select Brand",
    options=sorted(df["Brand"].unique()),
    default=sorted(df["Brand"].unique())
)


# Price filter

min_price = int(df["Price"].min())
max_price = int(df["Price"].max())

price_range = st.sidebar.slider(
    "Price Range",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price),
    step=1000
)


# RAM filter

ram_options = sorted(df["RAM"].unique())

ram = st.sidebar.multiselect(
    "RAM (GB)",
    options=ram_options,
    default=ram_options
)


# Storage filter

storage_options = sorted(df["Storage"].unique())

storage = st.sidebar.multiselect(
    "Storage (GB)",
    options=storage_options,
    default=storage_options
)


st.sidebar.markdown("---")

st.sidebar.info(
    "Use the filters to dynamically explore the dataset."
)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df[
    (df["Brand"].isin(brands)) &
    (df["Price"].between(price_range[0], price_range[1])) &
    (df["RAM"].isin(ram)) &
    (df["Storage"].isin(storage))
]


# =========================================================
# DASHBOARD METRICS
# =========================================================

if len(filtered_df) > 0:

    total_phones = len(filtered_df)

    average_price = np.mean(
        filtered_df["Price"]
    )

    highest_price = np.max(
        filtered_df["Price"]
    )

    average_rating = np.mean(
        filtered_df["Rating"]
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Phones",
        f"{total_phones}"
    )

    col2.metric(
        "Average Price",
        f"₹{average_price:,.0f}"
    )

    col3.metric(
        "Highest Price",
        f"₹{highest_price:,.0f}"
    )

    col4.metric(
        "Average Rating",
        f"{average_rating:.2f}"
    )

else:

    st.warning(
        "No phones match the selected filters."
    )


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Overview",
    "Brands",
    "Pricing",
    "Specifications",
    "Ratings",
    "Insights"
])


# =========================================================
# TAB 1 - OVERVIEW
# =========================================================

with tab1:

    st.header("Dataset Overview")

    if len(filtered_df) > 0:

        st.write(
            f"Showing {len(filtered_df)} phones "
            "based on the selected filters."
        )

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Dataset Summary")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Number of Brands",
            filtered_df["Brand"].nunique()
        )

        col2.metric(
            "Average RAM",
            f"{np.mean(filtered_df['RAM']):.1f} GB"
        )

        col3.metric(
            "Average Storage",
            f"{np.mean(filtered_df['Storage']):.0f} GB"
        )

    else:

        st.info("No data available.")


# =========================================================
# TAB 2 - BRAND ANALYSIS
# =========================================================

with tab2:

    st.header("Brand Analysis")

    if len(filtered_df) > 0:

        # Number of phones by brand

        st.subheader("Number of Phones by Brand")

        brand_count = (
            filtered_df["Brand"]
            .value_counts()
        )

        fig, ax = plt.subplots(
            figsize=(10, 5)
        )

        sns.barplot(
            x=brand_count.index,
            y=brand_count.values,
            ax=ax
        )

        ax.set_xlabel("Brand")
        ax.set_ylabel("Number of Phones")
        ax.set_title(
            "Number of Mobile Phones by Brand"
        )

        plt.xticks(rotation=45)

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)


        # Average price by brand

        st.subheader("Average Price by Brand")

        avg_price = (
            filtered_df
            .groupby("Brand")["Price"]
            .mean()
            .sort_values(ascending=False)
        )

        fig, ax = plt.subplots(
            figsize=(10, 5)
        )

        sns.barplot(
            x=avg_price.index,
            y=avg_price.values,
            ax=ax
        )

        ax.set_xlabel("Brand")
        ax.set_ylabel("Average Price")
        ax.set_title(
            "Average Mobile Phone Price by Brand"
        )

        plt.xticks(rotation=45)

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)


        # Brand summary

        st.subheader("Brand Summary")

        brand_summary = (
            filtered_df
            .groupby("Brand")
            .agg(
                Phones=("Model", "count"),
                Average_Price=("Price", "mean"),
                Average_Rating=("Rating", "mean"),
                Average_RAM=("RAM", "mean")
            )
            .round(2)
            .sort_values(
                "Average_Price",
                ascending=False
            )
        )

        st.dataframe(
            brand_summary,
            use_container_width=True
        )

    else:

        st.info(
            "No data available for brand analysis."
        )


# =========================================================
# TAB 3 - PRICING ANALYSIS
# =========================================================

with tab3:

    st.header("Pricing Analysis")

    if len(filtered_df) > 0:

        # Price distribution

        st.subheader("Price Distribution")

        fig, ax = plt.subplots(
            figsize=(10, 5)
        )

        sns.histplot(
            filtered_df["Price"],
            bins=10,
            kde=True,
            ax=ax
        )

        ax.set_title(
            "Mobile Phone Price Distribution"
        )

        ax.set_xlabel("Price")
        ax.set_ylabel("Number of Phones")

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)


        # Price statistics

        st.subheader("Price Statistics")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Minimum",
            f"₹{filtered_df['Price'].min():,.0f}"
        )

        col2.metric(
            "Average",
            f"₹{filtered_df['Price'].mean():,.0f}"
        )

        col3.metric(
            "Median",
            f"₹{filtered_df['Price'].median():,.0f}"
        )

        col4.metric(
            "Maximum",
            f"₹{filtered_df['Price'].max():,.0f}"
        )


        # Affordable phones

        st.subheader("Most Affordable Phones")

        cheapest = (
            filtered_df
            .sort_values("Price")
            .head(5)
        )

        st.dataframe(
            cheapest[
                [
                    "Brand",
                    "Model",
                    "Price",
                    "RAM",
                    "Storage",
                    "Rating"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )


        # Expensive phones

        st.subheader("Most Expensive Phones")

        expensive = (
            filtered_df
            .sort_values(
                "Price",
                ascending=False
            )
            .head(5)
        )

        st.dataframe(
            expensive[
                [
                    "Brand",
                    "Model",
                    "Price",
                    "RAM",
                    "Storage",
                    "Rating"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No data available for price analysis."
        )


# =========================================================
# TAB 4 - SPECIFICATIONS
# =========================================================

with tab4:

    st.header("Specifications Analysis")

    if len(filtered_df) > 0:

        # RAM vs Price

        st.subheader("RAM vs Price")

        fig, ax = plt.subplots(
            figsize=(10, 5)
        )

        sns.scatterplot(
            data=filtered_df,
            x="RAM",
            y="Price",
            hue="Brand",
            s=100,
            ax=ax
        )

        ax.set_title(
            "RAM vs Mobile Phone Price"
        )

        ax.set_xlabel("RAM (GB)")
        ax.set_ylabel("Price")

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)


        if filtered_df["RAM"].nunique() > 1:

            ram_correlation = np.corrcoef(
                filtered_df["RAM"],
                filtered_df["Price"]
            )[0, 1]

            st.metric(
                "RAM-Price Correlation",
                f"{ram_correlation:.2f}"
            )


        # Storage vs Price

        st.subheader("Storage vs Price")

        fig, ax = plt.subplots(
            figsize=(10, 5)
        )

        sns.scatterplot(
            data=filtered_df,
            x="Storage",
            y="Price",
            hue="Brand",
            s=100,
            ax=ax
        )

        ax.set_title(
            "Storage vs Mobile Phone Price"
        )

        ax.set_xlabel("Storage (GB)")
        ax.set_ylabel("Price")

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)


        if filtered_df["Storage"].nunique() > 1:

            storage_correlation = np.corrcoef(
                filtered_df["Storage"],
                filtered_df["Price"]
            )[0, 1]

            st.metric(
                "Storage-Price Correlation",
                f"{storage_correlation:.2f}"
            )


        # Average price by RAM

        st.subheader("Average Price by RAM")

        ram_price = (
            filtered_df
            .groupby("RAM")["Price"]
            .mean()
            .sort_index()
        )

        fig, ax = plt.subplots(
            figsize=(10, 5)
        )

        sns.barplot(
            x=ram_price.index,
            y=ram_price.values,
            ax=ax
        )

        ax.set_title(
            "Average Price by RAM"
        )

        ax.set_xlabel("RAM (GB)")
        ax.set_ylabel("Average Price")

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)


        # Average price by Storage

        st.subheader("Average Price by Storage")

        storage_price = (
            filtered_df
            .groupby("Storage")["Price"]
            .mean()
            .sort_index()
        )

        fig, ax = plt.subplots(
            figsize=(10, 5)
        )

        sns.barplot(
            x=storage_price.index,
            y=storage_price.values,
            ax=ax
        )

        ax.set_title(
            "Average Price by Storage"
        )

        ax.set_xlabel("Storage (GB)")
        ax.set_ylabel("Average Price")

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)

    else:

        st.info(
            "No data available for specifications analysis."
        )


# =========================================================
# TAB 5 - RATINGS
# =========================================================

with tab5:

    st.header("Rating Analysis")

    if len(filtered_df) > 0:

        # Rating distribution

        st.subheader("Rating Distribution")

        fig, ax = plt.subplots(
            figsize=(10, 5)
        )

        sns.histplot(
            filtered_df["Rating"],
            bins=10,
            kde=True,
            ax=ax
        )

        ax.set_title(
            "Mobile Phone Rating Distribution"
        )

        ax.set_xlabel("Rating")
        ax.set_ylabel("Number of Phones")

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)


        # Rating by brand

        st.subheader("Average Rating by Brand")

        rating_by_brand = (
            filtered_df
            .groupby("Brand")["Rating"]
            .mean()
            .sort_values(ascending=False)
        )

        fig, ax = plt.subplots(
            figsize=(10, 5)
        )

        sns.barplot(
            x=rating_by_brand.index,
            y=rating_by_brand.values,
            ax=ax
        )

        ax.set_title(
            "Average Rating by Brand"
        )

        ax.set_xlabel("Brand")
        ax.set_ylabel("Average Rating")

        plt.xticks(rotation=45)

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)


        # Top rated phones

        st.subheader("Top Rated Phones")

        top_rated = (
            filtered_df
            .sort_values(
                "Rating",
                ascending=False
            )
            .head(5)
        )

        st.dataframe(
            top_rated[
                [
                    "Brand",
                    "Model",
                    "Price",
                    "RAM",
                    "Storage",
                    "Rating",
                    "Reviews"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )


        # Camera and Battery

        st.subheader("Camera and Battery Analysis")

        col1, col2 = st.columns(2)

        with col1:

            fig, ax = plt.subplots(
                figsize=(7, 5)
            )

            sns.scatterplot(
                data=filtered_df,
                x="Camera",
                y="Price",
                hue="Brand",
                s=100,
                ax=ax
            )

            ax.set_title(
                "Camera vs Price"
            )

            ax.set_xlabel("Camera (MP)")
            ax.set_ylabel("Price")

            st.pyplot(
                fig,
                use_container_width=True
            )

            plt.close(fig)


        with col2:

            fig, ax = plt.subplots(
                figsize=(7, 5)
            )

            sns.scatterplot(
                data=filtered_df,
                x="Battery",
                y="Price",
                hue="Brand",
                s=100,
                ax=ax
            )

            ax.set_title(
                "Battery vs Price"
            )

            ax.set_xlabel("Battery (mAh)")
            ax.set_ylabel("Price")

            st.pyplot(
                fig,
                use_container_width=True
            )

            plt.close(fig)

    else:

        st.info(
            "No data available for rating analysis."
        )


# =========================================================
# TAB 6 - INSIGHTS
# =========================================================

with tab6:

    st.header("Key Insights")

    if len(filtered_df) > 0:

        price_by_brand = (
            filtered_df
            .groupby("Brand")["Price"]
            .mean()
        )

        rating_by_brand = (
            filtered_df
            .groupby("Brand")["Rating"]
            .mean()
        )

        ram_price = (
            filtered_df
            .groupby("RAM")["Price"]
            .mean()
        )

        storage_price = (
            filtered_df
            .groupby("Storage")["Price"]
            .mean()
        )


        # Find insights

        highest_rated_brand = (
            rating_by_brand.idxmax()
        )

        most_expensive_brand = (
            price_by_brand.idxmax()
        )

        most_affordable_brand = (
            price_by_brand.idxmin()
        )

        highest_ram = (
            ram_price.idxmax()
        )

        highest_storage = (
            storage_price.idxmax()
        )


        # Display insights

        col1, col2 = st.columns(2)

        with col1:

            st.success(
                f"Highest Rated Brand: "
                f"{highest_rated_brand} "
                f"({rating_by_brand.max():.2f}/5)"
            )

            st.info(
                f"Most Expensive Brand: "
                f"{most_expensive_brand} "
                f"(₹{price_by_brand.max():,.0f} average)"
            )

            st.warning(
                f"Most Affordable Brand: "
                f"{most_affordable_brand} "
                f"(₹{price_by_brand.min():,.0f} average)"
            )


        with col2:

            st.info(
                f"Highest-Priced RAM Category: "
                f"{highest_ram} GB"
            )

            st.info(
                f"Highest-Priced Storage Category: "
                f"{highest_storage} GB"
            )


            most_expensive_phone = (
                filtered_df
                .sort_values(
                    "Price",
                    ascending=False
                )
                .iloc[0]
            )

            st.success(
                f"Most Expensive Phone: "
                f"{most_expensive_phone['Brand']} "
                f"{most_expensive_phone['Model']} "
                f"(₹{most_expensive_phone['Price']:,.0f})"
            )


        # Correlation heatmap

        st.subheader("Feature Correlation")

        correlation_data = filtered_df[
            [
                "Price",
                "RAM",
                "Storage",
                "Camera",
                "Battery",
                "Rating",
                "Reviews"
            ]
        ]

        correlation_matrix = (
            correlation_data.corr()
        )

        fig, ax = plt.subplots(
            figsize=(10, 7)
        )

        sns.heatmap(
            correlation_matrix,
            annot=True,
            fmt=".2f",
            ax=ax
        )

        ax.set_title(
            "Mobile Phone Feature Correlation"
        )

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)


        # Summary

        st.subheader("Analysis Summary")

        st.write(
            f"""
            The selected dataset contains {len(filtered_df)} phones.

            The average phone price is
            ₹{filtered_df['Price'].mean():,.0f}.

            The average customer rating is
            {filtered_df['Rating'].mean():.2f} out of 5.

            {highest_rated_brand} has the highest average rating
            among the selected brands.

            {most_expensive_brand} has the highest average price.

            {most_affordable_brand} has the lowest average price.
            """
        )

    else:

        st.info(
            "Select different filters to generate insights."
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Mobile Phone Analytics Dashboard | "
    "Python | NumPy | Pandas | Matplotlib | Seaborn | Streamlit"
)
