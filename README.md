# User Guide: Blog Post Comparison App

Welcome to the Blog Post Comparison App! This guide will walk you through how to use the app and understand its results.

## What This App Does

This app compares old and new versions of blog posts to ensure that important information has been correctly transferred during updates or migrations.

## How to Use the App

1. **Prepare Your File**
   - Create a CSV file with two columns: 'old_url' and 'new_url'
   - In each row, put the URL of the old version of a blog post in the 'old_url' column and the URL of the new version in the 'new_url' column
   - Save this as a CSV file on your computer

   Example of your CSV file contents:
   ```
   old_url,new_url
   https://old-blog.com/post1,https://new-blog.com/post1
   https://old-blog.com/post2,https://new-blog.com/post2
   ```

2. **Upload Your File**
   - Open the app in your web browser (your IT department will provide the link)
   - Look for the "Choose a CSV file" button
   - Click this button and select your prepared CSV file

3. **Wait for Processing**
   - After uploading, you'll see a progress bar
   - The app is now comparing your blog posts
   - This may take a few minutes depending on how many URLs you've provided

4. **View Results**
   - Once processing is complete, you'll see a table with the comparison results
   - Scroll through this table to view the results for each pair of URLs

5. **Download Results**
   - To save the results, look for the "Download results as CSV" button
   - Click this button to download a CSV file with all the comparison details

## Understanding the Results

The results table shows:

- **old_slug**: The identifier of the old blog post
- **new_slug**: The identifier of the new blog post
- **comparison_details**: A summary of the comparison results

In the 'comparison_details' column, you'll see one of these results:

- **"All good but double check"**: This means all important information matches between the old and new versions. It's still a good idea to manually verify.

- **A list of differences**: This shows which types of information are missing or different between the old and new versions.

### Example Results

1. All Good:
   ```
   old_slug: summer-recipes
   new_slug: summer-recipes-2023
   comparison_details: All good but double check
   ```
   This means the content of "summer-recipes" and "summer-recipes-2023" match well.

2. Differences Found:
   ```
   old_slug: tech-news
   new_slug: technology-updates
   comparison_details: ImageObject: Missing in new version, Article: Mismatched
   ```
   This means:
   - The new "technology-updates" post is missing an image that was in the old "tech-news" post
   - The article content doesn't match exactly between the old and new versions

## What to Do with the Results

- For "All good" results: It's still wise to quickly check these posts manually.
- For posts with differences: Review these carefully. You may need to:
  - Add missing images
  - Update article content to match the old version
  - Check if the differences are intentional (like updated information)

If you're unsure about any results, consult with your content team or the person responsible for the blog migration.

## Need Help?

If you encounter any issues or have questions about the results, please contact your IT support team or the person who provided you with access to this app.
