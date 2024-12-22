# mapart - Create map arts for Minecraft BE worlds

![Mona Lisa in Minecraft](assets/screenshot-mona-lisa1.jpg)
![Mona Lisa in Minecraft](assets/screenshot-mona-lisa2.jpg)


## Installation

```console
pipx install git+https://github.com/bedrock-ws/mapart.git
```


## Usage

```console
mapart share
```

`share` is a path to a directory containing images. Within Minecraft the player
can use `#foo/bar/image.png` which would "print" the image located at
`share/foo/bar/image.png` into the Minecraft world.

You can override the address and port with their appropiate flags `--address`
and `--port` (e.g. `mapart --address localhost --port 8000 share`).

The `--palette` flag can be used to set the block palette. For example certain
blocks represent a different color on a map. `closest` is optimal for pixel
arts and `map` (default) is optimal for map arts.

## Tutorial

1. Create a directory `share` and put images in there.
2. Launch the app with `mapart share`.
3. Launch Minecraft.
4. Connect to the websocket with `/connect XXX.XXX.XX.XXX:6464` (insert the IP
   address of the server).
5. Go to an area in your Minecraft world that is far away from your beloved
   creations.
6. Create a map.
7. Goto the top left position visible on the map.
8. Generate the map art with `#path/to/image.png`

