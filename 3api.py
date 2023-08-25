from flask import Flask, request, jsonify
import json
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/json_to_xml', methods=['POST'])
def json_to_xml():
    try:
        # Получите JSON из запроса
        json_data = request.get_json()

        # Преобразуйте JSON в XML
        xml_data = json_to_xml_converter(json_data)

        # Верните XML как ответ
        return xml_data, 200, {'Content-Type': 'application/xml'}

    except Exception as e:
        return str(e), 400

def json_to_xml_converter(json_data):
    root = ET.Element("data")
    json_to_xml_recursive(json_data, root)
    xml_data = ET.tostring(root, encoding='utf8').decode('utf8')
    return xml_data

def json_to_xml_recursive(data, parent):
    if isinstance(data, dict):
        for key, value in data.items():
            element = ET.SubElement(parent, key)
            json_to_xml_recursive(value, element)
    elif isinstance(data, list):
        for item in data:
            json_to_xml_recursive(item, parent)
    else:
        parent.text = str(data)

if __name__ == '__main__':
    app.run(debug=True)