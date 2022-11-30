import math
import os

import geopandas as gpd
import requests
from tqdm import tqdm


class TileOperate:
    def __init__(self, tile_url, file_path, zoom_level=18):
        self.tile_url = tile_url
        self.file_path = file_path
        self.zoom_level = zoom_level
        self.geometries = self.get_geometries()
        self.tile_list = []

    @staticmethod
    def latlon_to_epsg3857(lon, lat):
        x = lon * 20037508.34 / 180
        y = math.log(math.tan((90 + lat) * math.pi / 360)) / (math.pi / 180)
        y = y * 20037508.34 / 180
        return x, y

    @staticmethod
    def get_resolution(z):
        return 156543.03392 / math.pow(2, z)

    def get_geometries(self):
        area = gpd.read_file(self.file_path)
        return area

    def get_bbox(self):
        bbox = self.geometries.total_bounds
        return bbox

    def get_tile_coordinates(self, longitude, latitude):
        tile_x = int((longitude + 180) / 360 * 2**self.zoom_level)
        tile_y = int(
            (1 - math.log(math.tan(latitude * math.pi / 180) + 1 / math.cos(latitude * math.pi / 180)) / math.pi)
            / 2
            * 2**self.zoom_level
        )
        return tile_x, tile_y

    def get_tile_range(self):
        bbox = self.get_bbox()
        upper_left = self.get_tile_coordinates(bbox[0], bbox[3])
        lower_right = self.get_tile_coordinates(bbox[2], bbox[1])
        tile_range = upper_left[0], upper_left[1], lower_right[0], lower_right[1]
        return tile_range

    def get_tile_list(self):
        tile_range = self.get_tile_range()
        tile_list = []
        for x in range(tile_range[0], tile_range[2] + 1):
            for y in range(tile_range[1], tile_range[3] + 1):
                tile_list.append((x, y))
        return tile_list

    def set_tile_list(self):
        self.tile_list = self.get_tile_list()

    def download_all_tiles(self):
        for tile in tqdm(self.tile_list):
            self.download_tile(tile[0], tile[1])

    def download_tile(self, x, y, output="./output"):
        url = self.tile_url.format(z=self.zoom_level, x=x, y=y)
        ext = os.path.splitext(url)[1]

        r = requests.get(url)

        if r.status_code == 200:
            os.makedirs(output + f"/{self.zoom_level}/{x}/", exist_ok=True)
            if os.path.exists(output + f"/{self.zoom_level}/{x}/{y}{ext}"):
                os.remove(output + f"/{self.zoom_level}/{x}/{y}{ext}")
            with open(output + f"/{self.zoom_level}/{x}/{y}{ext}", "wb") as f:
                f.write(r.content)
        else:
            print(f"Error: {r.status_code}")

    def tile_coords_to_latlon(self, x, y):
        n = 2.0**self.zoom_level
        lon_deg = x / n * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y / n)))
        lat_deg = math.degrees(lat_rad)
        return lon_deg, lat_deg

    def tile_coords_to_latlon_bbox(self, x, y):
        right_top = self.tile_coords_to_latlon(x + 1, y)
        left_bottom = self.tile_coords_to_latlon(x, y + 1)
        return left_bottom[0], left_bottom[1], right_top[0], right_top[1]

    def tile_coords_to_epsg3857(self, x, y):
        lon, lat = self.tile_coords_to_latlon(x, y)
        return self.latlon_to_epsg3857(lon, lat)
