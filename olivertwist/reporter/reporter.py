import json
import os
import pathlib
import shutil

from jinja2 import Environment, PackageLoader

root = pathlib.Path(__file__).parent
target_dir = pathlib.Path(os.getcwd()) / "target"

templates_dir = root / "templates"
css_dir = root / "html" / "css"
webfonts_dir = root / "html" / "webfonts"
images_dir = root / "html" / "images"
env = Environment(loader=PackageLoader("olivertwist.reporter", "templates"))
index_template = env.get_template("index.html")
model_template = env.get_template("model.html")


def output_json(oliver_twist_json):
    shutil.rmtree(target_dir, ignore_errors=True)
    os.mkdir(target_dir)
    filename = target_dir / "oliver_twist.json"
    with open(filename, "w") as outfile:
        json.dump(oliver_twist_json, outfile)


def render_html_report(oliver_twist_json):
    shutil.copytree(css_dir, target_dir / "css")
    shutil.copytree(webfonts_dir, target_dir / "webfonts")
    shutil.copytree(images_dir, target_dir / "images")

    filename = target_dir / "index.html"
    with open(filename, "w") as fh:
        fh.write(index_template.render(oliver_twist_json))

    for model in oliver_twist_json["models"]:
        filename = os.path.join(target_dir, model["model_name"] + ".html")
        with open(filename, "w") as fh:
            fh.write(model_template.render(model))
