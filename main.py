
import typer
from api_calls import ArubaAPIClient
from typing_extensions import Annotated

app = typer.Typer()


@app.command()
def login(base_url: Annotated[str, typer.Argument()],
         username: Annotated[str, typer.Argument()],
          password: Annotated[str, typer.Argument()]):
    """Authenticate with the Aruba Mobility Controller."""
    client = ArubaAPIClient(base_url, username, password)
    client.test_login()
    client.logout()

@app.command()
def show_command(base_url: Annotated[str, typer.Argument()],
                username: Annotated[str, typer.Argument()],
                password: Annotated[str, typer.Argument()],
                show_command: Annotated[str, typer.Argument()]):
    """Retrieve system information from the Aruba Mobility Controller."""
    client = ArubaAPIClient(base_url, username, password)
    client.show_command(show_command)
    client.logout()

@app.command()
def upgrade(base_url: Annotated[str, typer.Argument()],
            username: Annotated[str, typer.Argument()], 
            password: Annotated[str, typer.Argument()], 
            filename: Annotated[str, typer.Argument()], 
            partition: Annotated[str, typer.Argument()]):
    """Upgrade Aruba Mobility Controller using TFTP."""
    client = ArubaAPIClient(base_url, username, password)
    client.upgrade(filename, partition)
    client.logout()

if __name__ == "__main__":
    app()