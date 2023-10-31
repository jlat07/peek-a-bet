import pytesseract
from PIL import Image

class ImageProcessor:
    def __init__(self, image_path):
        self.image_path = image_path


    def process_image(self, uploaded_file):
        try:
            # Convert uploaded file to PIL Image
            image = Image.open(uploaded_file)

            # Use pytesseract to extract text from the image
            extracted_text = pytesseract.image_to_string(image)
            
            # Now, process this text to structure ticket details
            ticket_details = self._structure_data(extracted_text)
            
            return ticket_details

        except Exception as e:
            print(f"Error processing image: {e}")
            return None

    def _structure_data(self, extracted_text):
        # For simplicity, let's assume each line in the extracted text is a detail
        # You can enhance this method based on the format of your tickets.
        
        lines = extracted_text.split('\n')
        structured_data = {
            "team": lines[0].strip(),
            "bet_details": lines[1].strip(),
            # ... add more as per your ticket's format
        }
        
        return structured_data
