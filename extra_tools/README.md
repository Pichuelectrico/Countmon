# Countmon - Extra Tools

> **Origin:** Countmon is built on top of [DotDotGoose](https://github.com/persts/DotDotGoose), an open source image counting tool developed by the American Museum of Natural History. We use DotDotGoose as our base and extend it to fit our own needs.

---

## Export Geographic Coordinates

By default, Countmon stores coordinates in pixel coordinates. If your images are georeferenced you can use the `export_geographic.py` script to transform the pixel coordinates into geographic coordinates.

For this script to work your images must be GeoTiffs or tifs, jpgs, pngs with associated world files (`.tfw`, `.jgw`, `.pgw` respectively).

```bash
# Linux & macOS
python3 -m venv geo-env
source geo-env/bin/activate
python -m pip install --upgrade pip
python -m pip install rasterio

# Windows
python -m venv geo-env
geo-env\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install rasterio
```

With your virtual environment activated, simply run:

```bash
python export_geographic.py
```

and follow the prompts.

---

## Convert GeoJSON to External Annotations

There is an undocumented feature, still under development, that allows you to use the Labelme software to delineate polygons to define counting areas on individual images when you have considerable overlap between images in your project.

If your images are georeferenced and you have polygon layers that denote your counting boundary, you can use the `geojson_to_annotation.py` script to convert those polygons into a format that Countmon can consume.

For this script to work your images must be GeoTiffs or tifs, jpgs, pngs with associated world files (`.tfw`, `.jgw`, `.pgw` respectively). Currently, the script assumes that your images and exported (GeoJSON) polygons are in the same coordinate system.

```bash
# Linux & macOS
python3 -m venv geo-env
source geo-env/bin/activate
python -m pip install --upgrade pip
python -m pip install rasterio

# Windows
python -m venv geo-env
geo-env\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install rasterio
```

With your virtual environment activated, simply run:

```bash
python geojson_to_annotation.py
```

and follow the prompts.
