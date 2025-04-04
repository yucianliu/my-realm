import os
import markdown
from jinja2 import Environment, FileSystemLoader

# Configuration
CONTENT_DIR = 'content'
TEMPLATES_DIR = 'templates'
OUTPUT_DIR = 'public'

env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

def render_markdown(markdown_path):
    with open(markdown_path, 'r', encoding='utf-8') as f:
        content = f.read()
        md = markdown.Markdown(extensions=['meta'])
        html = md.convert(content)
        metadata = md.Meta
        body = html
        return metadata, body

def render_template(template_name, output_path, **context):
    template = env.get_template(template_name)
    rendered_html = template.render(context)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(rendered_html)

def generate_list_page(content_type, template_name, output_filename, title):
    content_path = os.path.join(CONTENT_DIR, content_type)
    items = []
    for filename in os.listdir(content_path):
        if filename.endswith('.md'):
            filepath = os.path.join(content_path, filename)
            metadata, _ = render_markdown(filepath)
            metadata['slug'] = filename.replace('.md', '')
            items.append(metadata)

    render_template(
        template_name,
        os.path.join(OUTPUT_DIR, output_filename),
        title=title,
        items=items,
        content_type=content_type
    )

def generate_single_page(content_type, template_name):
    content_path = os.path.join(CONTENT_DIR, content_type)
    for filename in os.listdir(content_path):
        if filename.endswith('.md'):
            filepath = os.path.join(content_path, filename)
            metadata, body = render_markdown(filepath)
            slug = filename.replace('.md', '')
            output_path = os.path.join(OUTPUT_DIR, content_type, f'{slug}.html')
            render_template(
                template_name,
                output_path,
                metadata=metadata,
                content=body,
                content_type=content_type
            )

def generate_static_page(content_filename, template_name, output_filename, title):
    filepath = os.path.join(CONTENT_DIR, content_filename)
    metadata, body = render_markdown(filepath)
    render_template(
        template_name,
        os.path.join(OUTPUT_DIR, output_filename),
        title=title,
        content=body,
        metadata=metadata
    )

if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, 'static', 'css'), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, 'static', 'js'), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, 'static', 'images'), exist_ok=True)
    # os.makedirs(os.path.join(OUTPUT_DIR, 'artworks'), exist_ok=True)
    # os.makedirs(os.path.join(OUTPUT_DIR, 'uiux'), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, 'projects'), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, 'blog'), exist_ok=True)

    # Copy static files
    for item in os.listdir(os.path.join('static', 'css')):
        os.system(f'cp static/css/{item} public/static/css/')
    for item in os.listdir(os.path.join('static', 'js')):
        os.system(f'cp static/js/{item} public/static/js/')
    for item in os.listdir(os.path.join('static', 'images')):
        os.system(f'cp -r static/images/{item} public/static/images/') # Use -r for directories

    # Generate main pages
    generate_static_page('index.md', 'index.html', 'index.html', 'Home')
    generate_static_page('about.md', 'about.html', 'about.html', 'About')

    # Generate project list and individual project pages
    generate_list_page('projects', 'projects.html', 'projects/index.html', 'Projects')
    generate_single_page('projects', 'project.html')

    # Generate blog list and individual blog posts
    generate_list_page('blog', 'blog.html', 'blog/index.html', 'Blog')
    generate_single_page('blog', 'post.html')

    # # Generate artwork list and individual artwork pages
    # generate_list_page('artworks', 'artworks.html', 'artworks/index.html', 'Artworks')
    # generate_single_page('artworks', 'artwork.html')

    # # Generate UI/UX design list and individual UI/UX design pages
    # generate_list_page('uiux', 'uiux_designs.html', 'uiux/index.html', 'UI/UX Designs')
    # generate_single_page('uiux', 'uiux_design.html')

    print("Portfolio website generated in the 'public' directory.")