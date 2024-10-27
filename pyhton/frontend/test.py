import PySimpleGUI as psg
from PIL import Image
import io
import base64

# Function to convert image to base64
def convert_to_base64(image_path):
    with Image.open(image_path) as img:
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode("utf-8")

# Corrected file path using raw string
image_path = r'C:\Users\chris\Desktop\Root\Work\C\Synthea-Arm\pyhton\frontend\images\Logo.jpg'
image_base64 = convert_to_base64(image_path)

layout = [
    [psg.Text(
        text='Python GUIs for Humans',
        font=('Arial Bold', 16),
        size=20,
        expand_x=True,
        justification='center'
    )],
    [psg.Image(
        data=image_base64,
        expand_x=True,
        expand_y=True
    )]
]

window = psg.Window('HelloWorld', layout, size=(715, 350), keep_on_top=True)

while True:
    event, values = window.read()
    print(event, values)
    if event in (None, 'Exit'):
        break

window.close()