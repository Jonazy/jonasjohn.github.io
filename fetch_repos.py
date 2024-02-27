import requests
import base64

def fetch_repositories():
    # Make a request to the GitHub API to fetch information about your repositories
    response = requests.get('https://api.github.com/users/yourusername/repos')
    repositories = response.json()
    return repositories

def fetch_readme(repository):
    # Make a request to the GitHub API to fetch the repository's README file
    response = requests.get(f"https://api.github.com/repos/yourusername/{repository['name']}/readme")
    if response.status_code == 200:
        readme_content = base64.b64decode(response.json()['content']).decode('utf-8')
        return readme_content
    else:
        return None

def generate_repository_cards(repositories):
    # Generate Markdown content for repository cards
    repository_cards_md = ''
    for repository in repositories:
        name = repository['name']
        description = repository['description']
        if not description:
            # Fetch the README content to use as description
            readme_content = fetch_readme(repository)
            if readme_content:
                # Extract the first line of the README content as the description
                description_lines = readme_content.split('\n')
                description = description_lines[0] if description_lines else "No description provided"
        # Modify this part according to your repository's structure
        # Extract image URL from the repository description (assuming it's included in the description)
        image_url = 'https://example.com/default_image.jpg'  # Default image URL if not found in description
        if 'image_url' in description:
            image_url = description.split('image_url: ')[1].split('\n')[0].strip()  # Extract image URL from description
        repository_cards_md += f"""
[![{name}]({image_url})]({repository['html_url']})
**{name}**: {description}

"""
    return repository_cards_md

if __name__ == '__main__':
    # Fetch repositories from your GitHub account
    repositories = fetch_repositories()
    # Generate Markdown content for repository cards
    repository_cards_md = generate_repository_cards(repositories)
    # Update README file with generated repository cards
    with open('README.md', 'r') as file:
        readme_content = file.read()
    updated_readme_content = readme_content.replace('<!-- REPOSITORIES_PLACEHOLDER -->', repository_cards_md)
    with open('README.md', 'w') as file:
        file.write(updated_readme_content)
