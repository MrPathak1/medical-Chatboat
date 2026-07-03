from medicine_info import get_medicine_details

def main():
    print("What this medicine is?")
    medicine_name = input("Enter medicine name: ").strip()
    if not medicine_name:
        print("Please enter a valid medicine name.")
        return
    details = get_medicine_details(medicine_name)
    print(details)

if __name__ == "__main__":
    main()
