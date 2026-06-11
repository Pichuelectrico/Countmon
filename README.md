# Countmon

Countmon is a free, open source tool to assist with manually counting objects in images.

![Screen Shot](doc/source/example.png)

*Point data collected with Countmon will be very valuable training and validation data for any future efforts with computer assisted counting.*

---

> **Based on [DotDotGoose](https://github.com/persts/DotDotGoose)** — Countmon is built on top of DotDotGoose, an open source counting tool developed by the American Museum of Natural History. We use it as our base and extend it for our own needs.

---

### Dependencies

Countmon is developed with the following libraries:

* PyQt6 (6.7.1)
* Pillow (10.3.0)
* Numpy (1.26.4)

## Installation

```bash
git clone https://github.com/persts/DotDotGoose
python3 -m venv ddg-env
source ddg-env/bin/activate
python -m pip install --upgrade pip
python -m pip install -r ./DotDotGoose/requirements.txt
```

## Launching Countmon

```bash
cd DotDotGoose
python3 main.py
```
