import os
import glob
import subprocess

def concatenate_files():
    output_dir = "/home/eason/projects/fovy-human-design/output/v2"
    output_md = os.path.join(output_dir, "FOVY_Strategy_Report.md")
    output_html = os.path.join(output_dir, "index.html")
    css_file = "report.css"

    # Files to concatenate
    readme_path = os.path.join(output_dir, "README.md")
    chapters_dir = os.path.join(output_dir, "chapters")
    
    # Get all chapter files sorted
    chapter_files = sorted(glob.glob(os.path.join(chapters_dir, "*.md")))
    
    # Full list with README first
    all_files = [readme_path] + chapter_files
    
    print("Concatenating the following files:")
    for f in all_files:
        print(f"- {os.path.basename(f)}")

    full_content = ""
    for file_path in all_files:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Add some spacing between chapters
                full_content += content + "\n\n---\n\n"
        else:
            print(f"Warning: File not found: {file_path}")

    # Write to single MD file
    with open(output_md, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    print(f"\nSuccessfully created markdown report: {output_md}")

    # Convert to HTML using Pandoc
    # Command: pandoc input.md -o output.html --css report.css --metadata title="..." -s
    # -s means standalone (creates full HTML with head/body)
    
    pandoc_cmd = [
        "pandoc",
        output_md,
        "-o", output_html,
        "--css", css_file,
        "-s"
    ]
    
    try:
        subprocess.run(pandoc_cmd, check=True, cwd=output_dir)
        print(f"Successfully created HTML report: {output_html}")
        print("You can open this HTML file in your browser and use 'Print to PDF' to generate the final PDF.")
    except FileNotFoundError:
        print("Error: 'pandoc' command not found. Please install pandoc to generate HTML.")
    except subprocess.CalledProcessError as e:
        print(f"Error running pandoc: {e}")

if __name__ == "__main__":
    concatenate_files()
