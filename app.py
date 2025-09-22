#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, flash
import yaml
import os

app = Flask(__name__)
app.secret_key = "supersecretkey123"

# Save directly into the j2 folder
OUTPUT_DIR = os.path.expanduser("~/ANA-Robocorp/j2")
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add_device", methods=["GET", "POST"])
def add_device():
    if request.method == "POST":
        device_name = request.form.get("device_name")
        device_type = request.form.get("device_type")

        if not device_name or not device_type:
            flash("Please enter all required fields!", "danger")
            return redirect(url_for("add_device"))

        # YAML structure
        device_data = {
            "hostname": device_name,
            "device_type": device_type.lower(),
            "vlans": [],
            "interfaces": [],
            "static_routes_v4": [],
            "static_routes_v6": [],
            "ospf": {"enabled": False, "process_id": "", "router_id": "", "networks": []},
            "rip": {"enabled": False, "version": 2, "networks": []},
            "snmp": {"enabled": False},
            "gnmi": {"enabled": False},
        }

        # Save into j2 folder
        yaml_path = os.path.join(OUTPUT_DIR, f"{device_name}.yaml")
        with open(yaml_path, "w") as f:
            yaml.dump(device_data, f, default_flow_style=False, sort_keys=False)

        flash(f"Device {device_name} ({device_type}) saved successfully!", "success")
        return redirect(url_for("index"))

    return render_template("add_device.html")

if __name__ == "__main__":
    app.run(debug=True)
