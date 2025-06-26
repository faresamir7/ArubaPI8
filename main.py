
import typer
from api_calls import ArubaAPIClient

app = typer.Typer()


@app.command()
def login(base_url: str, username: str, password: str):
    """Authenticate with the Aruba Mobility Controller."""
    client = ArubaAPIClient(base_url, username, password)
    client.test_login()
    client.logout()

@app.command()
def show_command(base_url: str, username: str, password: str, show_command: str):
    """Retrieve system information from the Aruba Mobility Controller."""
    client = ArubaAPIClient(base_url, username, password)
    client.show_command(show_command)
    client.logout()

if __name__ == "__main__":
    app()