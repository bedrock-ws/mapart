from pathlib import Path

import adorable  # type: ignore
from bedrock.consts import NAME
from bedrock.context import PlayerMessageContext, ReadyContext
from bedrock.ext import ui
from bedrock.server import Server
from PIL import Image
import rgbmatch  # type: ignore

from . import palettes


ImageType = Image.Image

PREFIX = "#"
PALETTE = palettes.DETAILED_MAP
RED = adorable.Color8bit.from_name("red")
BLUE = adorable.Color8bit.from_name("blue")
YELLOW = adorable.Color8bit.from_name("yellow")
MAP_SIZE = 128
FILL_COLOR = "white"
"""The color to fill empty space when squaring an image"""


def pixelate(im: ImageType) -> ImageType:
    return im.resize((MAP_SIZE, MAP_SIZE), resample=Image.Resampling.BILINEAR)

def quadratic(im: ImageType) -> bool:
    return im.size[0] == im.size[1]

def square_image(im: ImageType):
    size = max(im.size)
    bg = Image.new("RGB", (size, size), FILL_COLOR)
    bg.paste(im, (int((size - im.size[0]) / 2), int((size - im.size[1]) / 2)))
    return bg


def launch(address: str, port: int, root_dir: Path) -> None:
    server = Server()

    @server.server_event
    async def ready(ctx: ReadyContext) -> None:
        print(f"{RED.fg:\N{MIDDLE DOT} LIVE} at {BLUE.bg: {ctx.host}:{ctx.port} } via {YELLOW.fg:{root_dir}}")

    @server.game_event
    async def player_message(ctx: PlayerMessageContext) -> None:
        if ctx.sender == NAME:
            return
    
        message = ctx.message
        if not message.startswith(PREFIX):
            return

        path = root_dir / message.removeprefix(PREFIX).strip()
        if ".." in path.parts:
            await ctx.reply(ui.red("Error: Cannot use `..` for paths"))
            return
        if not path.exists():
            await ctx.reply(ui.red("Error: The provided path does not exist"))
            return
        if not path.is_file():
            await ctx.reply(ui.red("Error: The provided points to a path"))
            return

        im = Image.open(path).convert("RGB")
        if not quadratic(im):
            im = square_image(im)
        im = pixelate(im)

        await ctx.server.run(f"inputpermission set {ctx.sender} movement disabled")
        x = z = 1
        for (r, g, b) in im.getdata():
            closest_rgb = rgbmatch.closest_rgb((r, g, b), PALETTE.keys())
            block = PALETTE[closest_rgb]
            await ctx.server.run(
                f"setblock ~{x - 1} ~-1 ~{z - 1} {block}",
                wait=False
            )

            if x % MAP_SIZE == 0:
                x = 1
                z += 1
            else:
                x += 1

        await ctx.reply(ui.green("Success: Done placing image"))
        await ctx.server.run(f"inputpermission set {ctx.sender} movement enabled")

    server.start(address, port)
