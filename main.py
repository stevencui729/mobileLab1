import parse_data

def main():
    parsed_data = parse_data.parse_data()
    print(len(parsed_data.keys()))


if __name__ == "__main__":
    main()