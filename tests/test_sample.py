from tile_operator.operate import TileOperate


def tests_sample():
    to = TileOperate(
        tile_url="https://tile.openstreetmap.jp/{z}/{x}/{y}.png",
        file_path="tests/data/sapporo.geojson",
        zoom_level=18,
    )

    assert to.tile_coords_to_latlon(0, 0) == (-180.0, 85.0511287798066)

    bbox = to.get_bbox().tolist()
    assert bbox == [141.34745105748715, 43.06613341427342, 141.35447566877565, 43.07026242419525]

    tile_list = to.get_tile_list()
    assert tile_list[0] == (233998, 96254)
    assert tile_list[-1] == (234003, 96258)
    assert len(tile_list) == 30
