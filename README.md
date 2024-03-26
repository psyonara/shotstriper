# Shot-Striper

Add beautiful, striped backgrounds to your screenshots.

![Shot-Striper](https://raw.githubusercontent.com/psyonara/shotstriper/master/imgs/headline.jpg)

## Installation

### Pipx

```shell
pipx install shotstriper
```

### Pip

```shell
pip install shotstriper
```

## Usage

### Quick Start

```shell
shotstriper add-background screengrab.jpg --palette-name="winter.planar-fugue"
```

This creates a new file "out.jpg", with a striped background applied, the colors used being from the "planar-fugue" palette in the "winter" category.

### Palettes

To get a list of palette categories, run:

```shell
shotstriper palette-categories
```

From the list, pick one category. Now browse through the palettes in that categories:

```shell
shotstriper browse-palettes --category sunset
```

The palettes are displayed page by page. Note the name of your favourite palette.

Note: you can browse all categories by omitting the category name.

### Adding Backgrounds

#### Using an image from the clipboard

```shell
shotstriper --from-clipboard --palette-name="sunset.quick-vignette" --output-file="new_screen.jpg"
```

### More Options

```shell
shotstriper add-background --help
```
