# Andre Ortega
# Homework 2

# On this machine (virtual Kali), run with 'sudo python3 enumerate.py' command

import os
import psutil # Already installed on this machine by default

# 1. Enumerate all the running processes

def functionOne():

    print("\n" + '-' * 50)
    print("\tENUMERATING ALL PROCESSES\n" + '-' * 50 + '\n')

    #psutil.process_iter(attrs=None, ad_value=None)

    for proc in psutil.process_iter():
        try:
            Name = proc.name()
            ID = proc.pid
            print(Name, ' ::: ', ID)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    print("\n" + '-' * 50)
    print("\tDONE.\n" + '-' * 50 + '\n')

# 2. List all the running threads within process boundary

def functionTwo(pid):

    flag = 0
    for proc in psutil.process_iter():
        try:
            ID = proc.pid
            if pid == ID:

                flag = 1

                Name = proc.name()
                numThreads = proc.num_threads()

                print("\n" + '-' * 50)
                print("\tProcess Name: " + Name)
                print("\tNumber of Threads: " + str(numThreads))


                threadList = proc.threads()
                for n in threadList:
                    print("\t\t" + str(n))

                print('-' * 50)

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    if flag == 0:
        print("\n" + '-' * 50)
        print("\tNO PROCESS WITH THAT PID\n" + '-' * 50 + '\n')

# 3. Enumerate all the loaded modules within the process

# stackoverflow.com/questions/5553917/how-to-list-all-dlls-loaded-by-a-process-with-python
def functionThree(pid):

    if psutil.pid_exists(pid) is True:

        p = psutil.Process(pid)
        Name = p.name()

        print("\n" + '-' * 50)
        print("Process Name: " + Name + "\nLOADED MODULES:")

        for module in p.memory_maps():
            print("\t" + str(module.path))

        print('-' * 50 + "\n")

    else:
        print("\n" + '-' * 50)
        print("\tNO PROCESS WITH THAT PID\n" + '-' * 50 + '\n')


# 4. Show all the executable pages within the process

def functionFour(pid):

    if psutil.pid_exists(pid) is True:

        p = psutil.Process(pid)
        Name = p.name()

        print("\n" + '-' * 50)
        print("Process Name: " + Name + "\nEXECUTABLE PAGES:")

        for module in p.memory_maps():

            filepath = str(module.path)

            if os.path.isfile(filepath) and os.access(filepath, os.X_OK):
                print("\t" + filepath)

        print('-' * 50 + "\n")

    else:
        print("\n" + '-' * 50)
        print("\tNO PROCESS WITH THAT PID\n" + '-' * 50 + '\n')

# 5. Read the memory
def functionFive(pid):

    if psutil.pid_exists(pid) is True:

        p = psutil.Process(pid)
        Name = p.name()

        print("\n" + '-' * 50)
        print("ENTER THE NUMBER OF THE FILE YOU'D LIKE TO READ")

        idx = 1
        execList = []

        for module in p.memory_maps():

            filepath = str(module.path)

            if os.path.isfile(filepath) and os.access(filepath, os.X_OK):
                execList += [filepath]
                print(str(idx) + " -->\t" + filepath)
                idx += 1

        print('-' * 50)

        check = False
        usrIdx = int(input("> "))

        while check is False:
            if (usrIdx > 0) and (usrIdx < idx):
                #check = True
                break
            else:
                usrIdx = int(input("Enter a value between 1 and " + str(idx - 1) + "\n> "))

        #for x in execList:
            #print(x)

        binary = open(execList[usrIdx - 1], "rb")

        filesize = os.path.getsize(execList[usrIdx - 1])
        print(str(filesize) + " bytes loaded from " + execList[usrIdx-1])

        #byte = binary.read(1)
        #while byte:
            #print(byte)
            #byte = binary.read(1)

        print("\nHow would you like to view the data?\n"
                "1. Select an offset and an amount of bytes to print\n"
                "2. Dump it all!")

        check = False
        usrIdx = int(input("> "))
        while check is False:
            if (usrIdx > 0) and (usrIdx < 3):
                break
            else:
                usrIdx = int(input("Enter either 1 or 2\n> "))

        if usrIdx == 1:
            offset = int(input("\nWhat offset (Enter decimal!)\n> "))
            amount = int(input("\nHow many bytes do you want to read?\n> "))
            bytes = binary.read(offset)
            bytes = binary.read(amount)
            print(bytes)

        else:
            bytes = binary.read(filesize)
            print(bytes)


        binary.close()

    else:
        print("\n" + '-' * 50)
        print("\tNO PROCESS WITH THAT PID\n" + '-' * 50 + '\n')


# Driver Section

exit = 0
while exit == 0:
#    try:
        userInput = input("What would you like to do?\n"
                "1. Enumerate all the running processes.\n"
                "2. List all the running threads within a process boundary\n"
                "3. Enumerate all the loaded modules within a process\n"
                "4. Show all the executable pages within a process\n"
                "5. Read the memory of a selected process\n"
                "6. EXIT\n> ")

        choice = int(userInput)

        if choice == 1:

            functionOne()

        elif choice == 2:

            pid = int(input("Select a pid\n> "))
            functionTwo(pid)

        elif choice == 3:

            pid = int(input("Select a pid\n> "))
            functionThree(pid)

        elif choice == 4:

            pid = int(input("Select a pid\n> "))
            functionFour(pid)

        elif choice == 5:

            pid = int(input("Select a pid\n> "))
            functionFive(pid)

        elif choice == 6:
            break

        else:
            print("\nTry again\n")
#    except:
#        print("\nTry again!\n")
