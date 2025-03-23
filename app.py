from flask import Flask, render_template, request, jsonify, Response, make_response
from happytransformer import HappyTextToText, TTSettings

app = Flask(__name__)

# Load the grammar correction model
happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")

@app.route("/")
def home() -> str:
    """
    Renders the home page.

    Returns:
        str: The rendered HTML content of the home page.
    """
    return render_template("index.html")

@app.route("/correct", methods=["POST"])
def correct_grammar() -> Response:
    """
    Corrects the grammar of the provided input text.

    Returns:
        Response: A JSON response containing the corrected text or an error message.
    """
    # Get the input text from the user
    input_data = request.json or {}
    input_text: str = input_data.get("text", "")

    # Check if input_text is empty
    if not input_text:
        response = make_response(jsonify({"error": "No text provided"}))
        response.status_code = 400
        return response

    # Add the prefix "grammar: " and generate the corrected text
    args: TTSettings = TTSettings(num_beams=5, min_length=1)
    result = happy_tt.generate_text(f"grammar: {input_text}", args=args)

    # Return the corrected text as JSON
    response = make_response(jsonify({"corrected_text": result.text}))
    response.status_code = 200
    return response

if __name__ == "__main__":
    app.run(debug=True)
