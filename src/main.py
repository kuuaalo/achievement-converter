import sys
platform = None
def main():
#komentoriviltä - input(sys.argv)

    order = int(input("Choose 1. To import new project, 2 To open existing project:"))
    if order == 1:
        global platform
        platform = int(input("Choose 1. for Epic, 2. for Steam 3. for Ms Store:"))
        path = input("Input file path:")
        print(path)
        read/read(platform, path)
    
    if order == 2:
        print("Open existing project")
        path = input("Input file path:")
        print(path)
    if order == 3: 
        exit



if __name__ == "__main__":
    main()
print(platform)    