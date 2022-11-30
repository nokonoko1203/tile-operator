import traceback

import click

import tile_operator


@click.group(help=f"Tile operator v{tile_operator.__version__}")
@click.version_option(version=tile_operator.__version__, message="Tile operator v%(version)s")
@click.option("-v", "--verbose", default=False, is_flag=True, help="verbose mode")
@click.pass_context
def main(context, debug, verbose):
    context.obj = dict(debug=debug, verbose=verbose)


@main.command(help="Tile Operation")
@click.argument("url", type=click.Path(exists=True))
@click.argument("file_path", type=click.Path(exists=True))
@click.argument("zoom_level", type=click.Path(exists=True))
@click.pass_context
def operate(context, url, file_path, zoom_level):
    """Tile Operation"""
    try:
        if context.obj["verbose"]:
            click.echo(f"\nTile operation\n")
            click.echo(f" Options:")
            click.echo(f"  url={url}")
            click.echo(f"  file_path={file_path}")
            click.echo(f"  zoom_level={zoom_level}")
            click.echo(f"\n")

    except Exception as e:
        click.echo(e)
        traceback.print_exc()


if __name__ == "__main__":
    main()
