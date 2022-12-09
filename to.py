import traceback

import click

import tile_operator
from tile_operator.operate import TileOperate


@click.group(help=f"Tile operator v{tile_operator.__version__}")
@click.version_option(version=tile_operator.__version__, message="Tile operator v%(version)s")
@click.option("-v", "--verbose", default=False, is_flag=True, help="verbose mode")
@click.pass_context
def main(context, verbose):
    context.obj = dict(verbose=verbose)


@main.command(help="Tile Operation")
@click.argument("tile_url", type=str)
@click.argument("file_path", type=click.Path(exists=True))
@click.argument("zoom_level", type=int)
@click.pass_context
def download(context, tile_url, file_path, bbox, zoom_level):
    """Tile Download"""
    try:
        if context.obj["verbose"]:
            click.echo(f"\nTile Download\n")
            click.echo(f" Options:")
            click.echo(f"  tile_url={tile_url}")
            click.echo(f"  file_path={file_path}")
            click.echo(f"  bbox={bbox}")
            click.echo(f"  zoom_level={zoom_level}")
            click.echo(f"\n")

    except Exception as e:
        click.echo(e)
        traceback.print_exc()

    to = TileOperate(
        tile_url=tile_url,
        file_path=file_path,
        bbox=bbox,
        zoom_level=zoom_level,
    )
    to.set_tile_list()
    to.download_all_tiles()


if __name__ == "__main__":
    main()
