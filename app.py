import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse, unquote

def extract_slug(url):
    parsed_url = urlparse(url)
    slug = parsed_url.path.rstrip('/').split('/')[-1]
    return unquote(slug)

def extract_schema_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    schema_details = {}
    for script in soup.find_all('script', type='application/ld+json'):
        try:
            data = json.loads(script.string)
            if data.get('@type') == 'ImageObject' and 'name' in data:
                schema_details['ImageObject'] = data['name']
            elif data.get('@type') == 'ImageObject' and 'image' in data and isinstance(data['image'], list):
                for image in data['image']:
                    if 'name' in image:
                        schema_details['ImageObject'] = image['name']
                        break
            elif 'name' in data:
                schema_type = data['@type']
                schema_details[schema_type] = data['name']
        except json.JSONDecodeError:
            continue
    return schema_details

def compare_schemas(old_schema_details, new_schema_details):
    comparison_results = {}
    for schema_type, old_name in old_schema_details.items():
        new_name = new_schema_details.get(schema_type)
        if new_name is None:
            comparison_results[schema_type] = 'Missing in new version'
        elif old_name != new_name:
            comparison_results[schema_type] = 'Mismatched'
        else:
            comparison_results[schema_type] = 'Matched'

    for schema_type in new_schema_details:
        if schema_type not in old_schema_details:
            comparison_results[schema_type] = 'Missing in old version'

    return comparison_results

def compare_blog_posts(old_url, new_url):
    old_slug = extract_slug(old_url)
    new_slug = extract_slug(new_url)
    old_schema_details = extract_schema_details(old_url)
    new_schema_details = extract_schema_details(new_url)
    schema_comparison = compare_schemas(old_schema_details, new_schema_details)

    return old_slug, new_slug, schema_comparison

def show_how_to_use():
    st.markdown("""
    ## How to Use the Blog Post Comparison App

    This app allows you to compare schema details between old and new versions of blog posts. Here's how to use it:

    1. Prepare a CSV file containing the old and new URLs of the blog posts you want to compare. The CSV file should have two columns: "old_url" and "new_url".
       - Example CSV format:
         ```
         old_url,new_url
         https://example.com/old-post-1,https://example.com/new-post-1
         https://example.com/old-post-2,https://example.com/new-post-2
         ```

    2. In the app, click on the "Choose a CSV file" button and select your prepared CSV file.

    3. The app will process the URLs and display the comparison results in a table format.

    4. The comparison results will show the following information for each blog post:
       - "old_slug": The slug (last part of the URL) of the old blog post.
       - "new_slug": The slug of the new blog post.
       - "schema_comparison": The comparison of schema details between the old and new versions.
         - "Matched": The schema detail is present and matches in both versions.
         - "Mismatched": The schema detail is present in both versions but has different values.
         - "Missing in old version": The schema detail is present in the new version but missing in the old version.
         - "Missing in new version": The schema detail is present in the old version but missing in the new version.

    5. You can download the comparison results as a CSV file by clicking on the "Download results as CSV" button.

    That's it! You can now easily compare schema details between old and new versions of your blog posts using this app.
    """)

def main():
    st.title("Post Migration - Schema Comparison App")

    # Sidebar menu
    menu_options = ["Compare Blog Posts", "How to Use"]
    selected_option = st.sidebar.selectbox("Select an option", menu_options)

    if selected_option == "Compare Blog Posts":
        # File uploader
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

        if uploaded_file is not None:
            # Read the CSV file
            df = pd.read_csv(uploaded_file)

            # Check if the CSV has the required columns
            if 'old_url' in df.columns and 'new_url' in df.columns:
                st.write("File uploaded successfully. Processing...")

                # Process the URLs
                comparison_data = []
                progress_bar = st.progress(0)
                for index, row in df.iterrows():
                    old_slug, new_slug, schema_comparison = compare_blog_posts(row['old_url'], row['new_url'])
                    comparison_data.append((old_slug, new_slug, schema_comparison))
                    progress_bar.progress((index + 1) / len(df))

                # Create comparison DataFrame
                comparison_df = pd.DataFrame(comparison_data, columns=['old_slug', 'new_slug', 'schema_comparison'])
                comparison_df['comparison_details'] = comparison_df['schema_comparison'].apply(
                    lambda x: ', '.join([f'{k}: {v}' for k, v in x.items()]))

                # Display results
                st.write("Comparison Results:")
                st.dataframe(comparison_df)

                # Download link for results
                csv = comparison_df.to_csv(index=False)
                st.download_button(
                    label="Download results as CSV",
                    data=csv,
                    file_name="comparison_results.csv",
                    mime="text/csv",
                )
            else:
                st.error("The CSV file must contain 'old_url' and 'new_url' columns.")
        else:
            st.write("Please upload a CSV file to start the comparison.")
    else:
        show_how_to_use()

if __name__ == "__main__":
    main()
