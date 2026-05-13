import basic1
import os


def read_file_or_input():
    while True:
        file_path = input("Enter file path or press enter to type text (or type 'Q' to quit): ")

        if file_path.lower() == 'q':
            break  # Ausführung des Programms anhalten

        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as file:
                    text = file.read()
                    print("\nPROCESSING THE FILE...\n")
                    process_text(file_path, text)  
            except Exception as e:
                print("An error occurred:", str(e))
        else:
            print("\nThe specified file doesn't exist. Please type text (end input with an empty line):\n")
            text_lines = []
            while True:
                line = input('Shell > ')
                if line.strip() == "":
                    break
                text_lines.append(line)
            text = '\n'.join(text_lines)
            print("\nPROCESSING THE FILE...\n")
            process_text('<stdin>', text)


def process_text(file_name, text):
    instructions = text.split('\n')  #  Anweisungen au Zeilen aufteilen
    for line_number, line in enumerate(instructions, start=1):
        if line.strip() == "":
            continue  # Leere Zeile ignorieren
        print(f"\n\n\n ************** PROCESSING LINE {line_number}: {line} **************")
        tokens, ast, intermediate_code, result, error = basic1.run(file_name, line, line_number)

        if error:
            print(f"Error in line {line_number}:")
            print(error.as_string())
        else:
            print(f"\n** TOKEN LIST FOR LINE {line_number} **\n{tokens}")
            print(f"\n** ABSTRACT SYNTAX TREE FOR LINE {line_number} **\n{ast.node}")
            print(f"\n** GENERATED INTERMEDIATE INSTRUCTIONS FOR LINE {line_number} **")
            for intermediate_instruction in intermediate_code:
                print(intermediate_instruction)
            print(f"\n** FINAL RESULT FOR LINE {line_number} **\n{result}")


read_file_or_input()