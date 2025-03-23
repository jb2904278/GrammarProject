from happytransformer import HappyTextToText, TTSettings
import torch

def initialize_model() -> HappyTextToText:
    """
    Initializes the HappyTextToText model for grammar correction and assigns the model to the
    best available device (CUDA, MPS, GPU, or CPU).

    Returns:
        HappyTextToText: The loaded grammar correction model.

    Raises:
        SystemExit: If model initialization fails.
    """
    try:
        # Check for the best available device
        if torch.cuda.is_available():
            device = torch.device("cuda")
            print("CUDA device is available. Using GPU for inference.")
        elif torch.backends.mps.is_available():
            device = torch.device("mps")
            print("MPS device is available. Using MPS for inference.")
        else:
            device = torch.device("cpu")
            print("No CUDA or MPS device found, falling back to CPU.")

        # Initialize the model with the selected device
        model = HappyTextToText("T5", "vennify/t5-base-grammar-correction", device=device)
        return model
    except Exception as e:
        print(f"Error initializing model: {e}")
        exit(1)  # Exit if the model initialization fails

# Initialize model once globally
happy_tt: HappyTextToText = initialize_model()

# Set up the text generation settings
args: TTSettings = TTSettings(num_beams=5, min_length=1)

def correct_grammar(input_text: str) -> str:
    """
    Corrects the grammar of the provided input text using the initialized model.

    Args:
        input_text (str): The sentence to be corrected.

    Returns:
        str: The corrected sentence or an error message if correction fails.
    """
    try:
        print(f"Correcting grammar for input: {input_text}")  # Debugging line
        result = happy_tt.generate_text(f"grammar: {input_text}", args=args)
        return result.text
    except Exception as e:
        print(f"Error during text generation: {e}")
        return "Error: Could not generate the corrected text."

# Example usage
if __name__ == "__main__":
    try:
        input_text: str = "This sentences has has bads grammar."
        corrected_text: str = correct_grammar(input_text)
        if corrected_text:
            print(f"Corrected Sentence: {corrected_text}")
        else:
            print("Failed to correct the sentence.")
    except Exception as e:
        print(f"An error occurred: {e}")
