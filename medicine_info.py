import requests

def get_medicine_details(medicine_name):
    """
    Fetches details about a medicine by searching online.
    This example uses the OpenFDA API for demonstration purposes.
    """
    try:
        # Replace with a valid API or web scraping logic
        url = f"https://api.fda.gov/drug/label.json?search={medicine_name}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes

        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            result = data["results"][0]
            description = result.get("description", ["No description available."])[0]
            purpose = result.get("purpose", ["No purpose available."])[0]
            dosage = result.get("dosage_and_administration", ["No dosage information available."])[0]
            precautions = result.get("warnings", ["No precautions available."])[0]
            return (f"💊 Medicine: {medicine_name}\n"
                    f"📄 Description: {description}\n"
                    f"🎯 Purpose: {purpose}\n"
                    f"💊 Dosage and Administration: {dosage}\n"
                    f"⚠️ Precautions: {precautions}")
        else:
            return f"❌ No information found for medicine: {medicine_name}"
    except requests.exceptions.RequestException as e:
        return f"❌ Error fetching details: {str(e)}"
