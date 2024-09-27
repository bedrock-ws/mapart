from pathlib import Path

import click

from .generator import launch


@click.command()
@click.option("--address", default="0.0.0.0", help="The address to run the server on")
@click.option("--port", default=6464, type=int, help="The port to run the server on")
@click.option("--palette", default="map", type=click.Choice(["map", "closest"]), help="The block palette to use")
@click.argument("directory", type=Path)
def app(address: str, port: int, palette: str, directory: Path) -> None:
    """Create map arts for Minecraft BE world"""
    launch(address, port, palette, directory)


if __name__ == "__main__":
    app()
