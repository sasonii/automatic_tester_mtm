import subprocess
import os
from termcolor import colored
import msvcrt
import logging

def does_program_exist(program):
    if not os.path.exists(program):
        input(f"Couldn't find {program}. make sure it is in the same directory. \nPRESS ENTER TO EXIT.")
        logging.error(f"Couldn't find {program}.")
        exit()

# input from the user
def get_params():
    hw_number = input("Enter the homework number: ")
    hw_question_number = input("Enter the homework's question number: ")
    hw_name = f"hw{hw_number}q{hw_question_number}"
    program = f"{hw_name}.exe"
    does_program_exist(program)
    start, end = int(input("Enter the starting number of the tests: ")), int(input("Enter the ending number of the tests: "))
    return hw_question_number, hw_name, start, end

def create_output(program, input_file_name, output_file_name):
    if not os.path.exists(input_file_name):
            print(f"Couldn't find {input_file_name}. make sure it is in the same directory. \nChecking for the others.")
            logging.error(f"Couldn't find {input_file_name}.")
            return False
    os.system(f"{program} < {input_file_name} > {output_file_name}")
    return True

def create_outputs(hw_question_number, hw_name, start, end, range_successeded):
    for i in range(start, end + 1):
        if(not create_output(f"{hw_name}.exe", f"test{i}.in", f"Q{hw_question_number}_res{i}.txt")):
            range_successeded.remove(i)
        else:
            logging.info(f"Created output for test {i}.")

def check_outputs(hw_question_number, hw_name, range_successeded):
    arr_error = []
    for i in range_successeded:
        desired_output = (f"""Comparing files test{i}.out and Q{hw_question_number}_RES{i}.TXT\r\nFC: no differences encountered\r\n\r\n""")
        batcmd = f"FC test{i}.out  q{hw_question_number}_res{i}.txt"
        try:
            res = subprocess.Popen(batcmd, stdout=subprocess.PIPE, shell=True).stdout.read().decode('ascii')        
        except:
            print(f"Might have been a problem with test number {i}. Check it manually!")

        if(res != desired_output):
            print(colored(f"ERROR in TEST {i}", 'red'))
            arr_error.append(i)
            logging.info(f"ERROR in TEST {i}")
        else:
            print(colored(f"TEST {i} PASSED", 'yellow'))
            logging.info(f"TEST {i} PASSED")

    if arr_error == []:
        return

    print("Type q to exit. Type any other letter if you wish to open diffmerge:")
    if(msvcrt.getch() == 'q'):
        exit()
    else:
        if not os.path.exists("DiffMerge.exe"):
            input("Couldn't find DiffMerge.exe . make sure it is in the same directory. Type Enter to Exit.")
        for i in arr_error:
            os.system(f"DIFFMERGE test{i}.out q{hw_question_number}_res{i}.txt")

def main():
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='tester.log', encoding='utf-8', level=logging.DEBUG)
    
    hw_question_number, hw_name, start, end = get_params()
    logging.info('Successfully scaned input')

    range_successeded = [i for i in range(start, end + 1)]
    create_outputs(hw_question_number, hw_name, start, end, range_successeded)
    
    check_outputs(hw_question_number, hw_name, range_successeded)    
    
    input("ENTER ANYTHING TO EXIT :)")

if __name__ == "__main__":
    main()