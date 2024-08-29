import re
import os
import PyPDF2

# Function to read a PDF file
def read_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
                else:
                    print(f"Warning: No text extracted from page {reader.pages.index(page)}")
            return text
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return None

# Function to read a text file
def read_text(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading text file: {e}")
        return None

# Extract information from the transcript
def extract_information(transcript):
    # Define regex patterns for extracting specific information

    # Customer Requirements
    car_type_pattern = r"(hatchback|suv|sedan)"
    fuel_type_pattern = r"(diesel|petrol|electric|hybrid)"
    color_pattern = r"(black|white|red|blue|silver|gray)"
    distance_travelled_pattern = r"(\d+(\.\d+)?\s*(km|miles))"
    make_year_pattern = r"\b(19|20)\d{2}\b"
    transmission_pattern = r"(automatic|manual)"

    # Company Policies
    free_rc_transfer_pattern = r"free\s*RC\s*transfer"
    money_back_guarantee_pattern = r"5\s*[-–]?\s*day\s*money\s*back\s*guarantee"
    free_rsa_pattern = r"free\s*RSA\s*for\s*(one|1)\s*year"
    return_policy_pattern = r"return\s*polic(?:y|ies)"

    # Customer Objections
    refurbishment_quality_pattern = r"refurbishment\s*(quality|issues?)"
    car_issues_pattern = r"(issues?\s*with\s*(the\s*)?car|car\s*problems?)"
    price_issues_pattern = r"(price\s*issues?|too\s*expensive|high\s*price)"
    experience_issues_pattern = r"(long\s*wait(\s*ing)?\s*time|salesperson'?s?\s*behavior)"

    # Print transcript content for debugging
    print("Transcript Content:\n", transcript)

    # Extract information using regex
    extracted_info = {
        "CustomerRequirements": {
            "CarType": re.search(car_type_pattern, transcript, re.IGNORECASE),
            "FuelType": re.search(fuel_type_pattern, transcript, re.IGNORECASE),
            "Color": re.search(color_pattern, transcript, re.IGNORECASE),
            "DistanceTravelled": re.search(distance_travelled_pattern, transcript, re.IGNORECASE),
            "MakeYear": re.search(make_year_pattern, transcript),
            "TransmissionType": re.search(transmission_pattern, transcript, re.IGNORECASE),
        },
        "CompanyPolicies": {
            "FreeRCTransfer": re.search(free_rc_transfer_pattern, transcript, re.IGNORECASE),
            "MoneyBackGuarantee": re.search(money_back_guarantee_pattern, transcript, re.IGNORECASE),
            "FreeRSA": re.search(free_rsa_pattern, transcript, re.IGNORECASE),
            "ReturnPolicy": re.search(return_policy_pattern, transcript, re.IGNORECASE),
        },
        "CustomerObjections": {
            "RefurbishmentQuality": re.search(refurbishment_quality_pattern, transcript, re.IGNORECASE),
            "CarIssues": re.search(car_issues_pattern, transcript, re.IGNORECASE),
            "PriceIssues": re.search(price_issues_pattern, transcript, re.IGNORECASE),
            "CustomerExperienceIssues": re.search(experience_issues_pattern, transcript, re.IGNORECASE),
        }
    }

    # Post-process the extracted data to clean up the results
    for category, details in extracted_info.items():
        print(f"\nCategory: {category}")  # Debugging output
        for key, match in details.items():
            details[key] = match.group(0) if match else "Not Mentioned"
            print(f"{key}: {details[key]}")  # Debugging output

    return extracted_info

# Main function to handle the input file and extract information
def process_transcript(file_path):
    # Determine the file type (PDF or text)
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == '.pdf':
        transcript = read_pdf(file_path)
    elif file_extension == '.txt':
        transcript = read_text(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a PDF or text file.")

    if not transcript:
        raise ValueError("Failed to read the transcript from the file.")

    # Extract and return the information from the transcript
    return extract_information(transcript)

# Example usage
if _name_ == "_main_":
    file_path = r"C:\dummy\conv2.txt"  # Use a raw string for the file path or double backslashes
    try:
        extracted_data = process_transcript(file_path)

        # Print the extracted information
        print("\nExtracted Information:")
        for category, details in extracted_data.items():
            print(f"\n{category}:")
            for key, value in details.items():
                print(f"  {key}: {value}")
    except Exception as e:
        print(f"An error occurred: {e}")