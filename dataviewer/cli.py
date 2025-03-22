"""
Command line interface for dataviewer package.
"""
import click
import os
from .core import DataViewer
import time
import threading
import itertools

def echo_spinner(message, done_message=None):
    """Create a spinner animation with a message."""
    def spinner_thread():
        spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        while not echo_spinner.done:
            click.echo(f'\r{message} {next(spinner)}', nl=False)
            time.sleep(0.1)
        click.echo('\r' + ' ' * (len(message) + 2))  # Clear the line
        if done_message:
            click.echo(done_message)
    
    # Start spinner in separate thread
    thread = threading.Thread(target=spinner_thread)
    thread.daemon = True  # Thread will exit when main program exits
    echo_spinner.done = False
    thread.start()
    return thread

@click.command()
@click.argument('dataset_url')
@click.option('--split', '-s', default='train', help='Dataset split to visualize (default: train)')
@click.option('--prompt', '-p', default='', help='Additional requirements for the visualization')
@click.option('--force', '-f', is_flag=True, help='Force regeneration of the viewer')
def main(dataset_url, split, prompt, force):
    """
    Create and run a Streamlit viewer for a Hugging Face dataset.
    
    DATASET_URL: Name or path of the dataset on Hugging Face Hub (e.g., 'mnist' or 'username/dataset-name')
    """
    try:
        click.secho(f"\n🔧 Setting up DataViewer for {dataset_url}", fg="green")
        
        # Create viewer based on available API keys
        viewer = DataViewer.from_environment()
        
        # Set up progress callback
        def progress_done():
            echo_spinner.done = True
            
        viewer.set_progress_callback(progress_done)
        
        # Load dataset with progress
        click.secho("\n📚 Loading dataset...", fg="blue")
        viewer.load_dataset(dataset_url)
        
        # Generate viewer with progress
        viewer_path = viewer._get_viewer_path(split)
        if force or not os.path.exists(viewer_path):
            click.secho("\n🤖 Generating Streamlit viewer...", fg="yellow")
            
            # Start spinner animation in background
            spinner_thread = echo_spinner(
                "Waiting for AI to generate visualization code",
                "✨ Viewer generated successfully!"
            )
            
            # Generate the viewer
            viewer.generate_viewer(split=split, extra_prompt=prompt, force=force)
            
            # Wait for spinner animation to finish
            spinner_thread.join()
        else:
            click.secho("\n📋 Using cached viewer", fg="green")
        
        # Run the viewer
        click.secho("\n🚀 Launching Streamlit...\n", fg="bright_green")
        viewer.run_viewer(split=split, extra_prompt=prompt, force=force)
        
    except ValueError as e:
        raise click.ClickException(str(e))
    except Exception as e:
        raise click.ClickException(f"Error: {str(e)}")

if __name__ == '__main__':
    main() 