def get_os(allowed_os):
    print("\n##########\nWARNING!!!\n##########")
    print("\nOS")
    print("==")
    print("Skipping the os parameter prevents you from entering user data.")
    print("This means you will be limited to using Windows instances with")
    print("any template created. Hit 'N' to accept this, or any other key")
    print("to  choose from a list of supported OS.\n")
    if input("Choose OS? [Y/n] ").lower() != 'n':
        counter = 1
        print("\nSupported OS:")
        for os in allowed_os:
            print(f"{counter} - {os}")
            counter += 1

        try:
            index = int(input("\nEnter a number to choose an OS: ")) -1
            if -1 < index < counter:
                return allowed_os[index]
        except:
            print("Not a valid value")
            return None
    else:
        return None