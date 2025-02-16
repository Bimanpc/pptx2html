from flask import Flask, request, send_file
import os
import comtypes.client

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def convert_pptx_to_pdf(input_path, output_path):
    powerpoint = comtypes.client.CreateObject("PowerPoint.Application")
    powerpoint.Visible = 1
    presentation = powerpoint.Presentations.Open(input_path)
    presentation.SaveAs(output_path, 32)  # 32 = PDF format
    presentation.Close()
    powerpoint.Quit()

@app.route("/convert", methods=["POST"])
def convert():
    if "file" not in request.files:
        return "No file uploaded", 400

    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_path = os.path.join(OUTPUT_FOLDER, file.filename.replace(".pptx", ".pdf"))

    file.save(input_path)
    convert_pptx_to_pdf(input_path, output_path)

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
