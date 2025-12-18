import comtradeapicall
import constants
from datetime import datetime
import pandas as pd

def extract_trend_data(hs_code, product_name):
    # Get current year
    current_year = datetime.now().year

    # Generate list of the previous 5 years (excluding current year)
    years = [str(year) for year in range(current_year - 5, current_year)]

    # Join them as a comma-separated string
    period = ",".join(years)
    analyze_df = comtradeapicall.getFinalData(constants.UNCOMTRADE_SUBS_KEY, 
                                              typeCode='C', 
                                              freqCode='A', 
                                              clCode='HS', 
                                              period=period,
                                              reporterCode=None, 
                                              cmdCode=hs_code, 
                                              flowCode='M', 
                                              partnerCode='360',
                                              partner2Code=None,
                                              customsCode=None, 
                                              motCode=None, 
                                              maxRecords=2500, 
                                              format_output='JSON',
                                              aggregateBy=None, 
                                              breakdownMode='classic', 
                                              countOnly=None, 
                                              includeDesc=True)
    
    # # Filter by Asia and select the necessary data
    analyze_df['continent'] = analyze_df['reporterDesc'].map(constants.COUNTRY_TO_CONTINENT)
    analyze_df['period'] = analyze_df['period'].astype(int)
    analyze_df['cifvalue'] = analyze_df['cifvalue'].fillna(0)
    analyze_df['cifvalue'] = analyze_df['cifvalue'].astype(int)
    analyze_df['qty'] = analyze_df['qty'].fillna(0)
    analyze_df['qty'] = analyze_df['qty'].astype(int)
    analyze_df['cost_per_kg'] = analyze_df['cifvalue'] / analyze_df['qty']
    analyze_df = analyze_df[analyze_df['continent']=='Asia']
    analyze_df = analyze_df[['period', 'reporterDesc', 'qty', 'cifvalue', 'cost_per_kg']]

    # Get top 3
    top_3 = analyze_df.groupby('reporterDesc', as_index=False)['qty'].sum()
    top_3 = top_3.sort_values(by='qty', ascending=False)
    top_3_countries = top_3.head(3)['reporterDesc'].tolist()
    top_3_analysis = analyze_df[analyze_df['reporterDesc'].isin(top_3_countries)]
    country1, country2, country3 = top_3_countries

    # Create separate DataFrames
    df_country1 = analyze_df[analyze_df['reporterDesc'] == country1]
    df_country2 = analyze_df[analyze_df['reporterDesc'] == country2]
    df_country3 = analyze_df[analyze_df['reporterDesc'] == country3]

    # Create a dictionary for dynamic looping
    country_dfs = {
        country1: df_country1,
        country2: df_country2,
        country3: df_country3
    }

    result_list_countries = []

    # Loop over each DataFrame
    for country, df in country_dfs.items():
        df = df.sort_values('period')  # Ensure sorted by year
        df['growth'] = df['qty'].pct_change()
        df['growth'] = (df['growth'] * 100).round(2)
        df['growth'] = df['growth'].fillna(0)
        df['growth'] = df['growth'].apply(lambda x: f"{x:.2f}%")
        df['cifvalue'] = df['cifvalue'].apply(
            lambda x: f"${x/1_000_000:.2f} M" if x >= 1_000_000 else f"${x}"
        )
        df['qty'] = df['qty'].apply(
            lambda x: f"{x/1_000:.2f}" if x >= 1_000 else f"{x}"
        )
        df['cost_per_kg'] = df['cost_per_kg'].apply(
            lambda x: f"${x:.2f} per kg" if x >= 0.01 else f"${x}"
        )
        df = df.rename(columns={'period': 'Year', 'reporterDesc ':'Country',
            'qty': 'Import Volume (ton)',
            'cifvalue':'Import value (USD)',
            'cost_per_kg': 'Cost per kg'})
        
         # Drop index before displaying
        df_display = df.reset_index(drop=True)
        df_display = df_display[['Year', 'Import Volume (ton)', 'Import value (USD)',
                                 'Cost per kg', 'growth']]
        # =====================================================
        # Ensure all years are present, fill missing with 'unavailable'
        all_years_df = pd.DataFrame({'Year': [int(y) for y in years]})
        df_display = pd.merge(all_years_df, df_display, on='Year', how='left')
        df_display = df_display.fillna('unavailable')
        # =====================================================

        # Convert each row to dict and append to the result list
        result_list_countries.append({
            "country": country,
            "product_name": product_name,
            "data": df_display.to_dict(orient='records')
        })

    return result_list_countries