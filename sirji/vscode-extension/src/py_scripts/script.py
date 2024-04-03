import sys

def main():
    # Example processing: Print arguments
    for arg in sys.argv[1:]:  # sys.argv[0]  is the script name
        if arg == "Browse":
            print("Browse: https://www.amp-what.com/unicode/search/refresh")
        elif arg == "Execute":
            print("Execute: ls -alt | tee sirji.log")
        elif arg == "Create":
            print("Create: Hello World")
        else:
            print("Unrecognized command. Please use Browse, Execute or Create")

if __name__ == "__main__":
    main()