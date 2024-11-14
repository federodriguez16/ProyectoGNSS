from flask import Flask, render_template_string

import folium

app = Flask(__name__)

@app.route("/")
def fullscreen():
    """Simple example of a fullscreen map."""
    m = folium.Map()
    return m.get_root().render()

@app.route("/iframe")
def iframe():
    """Embed a map as an iframe on a page."""
    m = folium.Map(location=[-33.123421644558995,-64.34904595605525], zoom_start=15)  

    # set the iframe width and height
    m.get_root().width = "1000px"
    m.get_root().height = "600px"
    iframe = m.get_root()._repr_html_()

    return render_template_string(
        """
            <!DOCTYPE html>
            <html>
                <head></head>
                <body>
                    <h1>Using an iframe</h1>
                    {{ iframe|safe }}
                </body>
            </html>
        """,
        iframe=iframe,
    )


if __name__ == "__main__":
    app.run(debug=True)