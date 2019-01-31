import parse_data

def main():
    parsed_data = parse_data.parse_data()
    print(len(parsed_data.keys()))
    print((parsed_data['Driving'][0].keys()))

if __name__ == "__main__":
    main()