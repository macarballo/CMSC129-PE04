import csv
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from typing import Tuple
import tkinter.simpledialog as simpledialog

# Main application class
class CompilerUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Programming Exercise 04: Syntax and Semantic Analysis for IOL")
        self.geometry("1200x700")
        self.configure(bg="#f0f0f0")
        self.font_style = ("Courier", 12)

        # File and Token Stream Paths
        self.file_path = None
        self.token_file_path = "output.tkn"
        self.token_saved = False  # To track if tokens have been saved

        # Create Menu Bar
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New File", command=self.new_file)
        file_menu.add_command(label="Open File", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)

        # Create a frame for buttons and align them horizontally
        button_frame = tk.Frame(self, bg="#f0f0f0")
        button_frame.pack(pady=15)

        # Button style for consistent appearance
        button_style = {
            "font": ("Courier", 12, "bold"),
            "bg": "#6A9FB5",
            "fg": "white",
            "relief": tk.RAISED,
            "bd": 2,
            "activebackground": "#55859B",
        }

        # Buttons for compile, view tokenized code, and save tokenized output
        compile_button = tk.Button(
            button_frame, text="Compile Code", command=self.compile_code, **button_style
        )
        compile_button.pack(side=tk.LEFT, padx=15, ipadx=10, ipady=5)

        show_tokenized_button = tk.Button(
            button_frame,
            text="Show Tokenized Code",
            command=self.show_tokenized_code,
            **button_style,
        )
        show_tokenized_button.pack(side=tk.LEFT, padx=15, ipadx=10, ipady=5)

        output_button = tk.Button(
            button_frame,
            text="Save Tokenized Output",
            command=self.save_token_file,
            **button_style,
        )
        output_button.pack(side=tk.LEFT, padx=15, ipadx=10, ipady=5)

        # I/O Frame (for input code editor and output console)
        io_frame = tk.Frame(self, bg="#f0f0f0")
        io_frame.pack(padx=15, pady=15, expand=True, fill=tk.BOTH)

        # Code Editor Section (Left side)
        code_editor_frame = tk.Frame(io_frame, bg="#f0f0f0")
        code_editor_frame.pack(
            side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH
        )

        code_editor_label = tk.Label(
            code_editor_frame,
            text="Built-in Code Editor",
            font=("Courier", 12, "bold"),
            bg="#f0f0f0",
        )
        code_editor_label.pack(anchor=tk.NW, pady=(0, 10))

        # Code editor area for input code
        self.editor_area = scrolledtext.ScrolledText(
            code_editor_frame,
            wrap=tk.WORD,
            height=12,
            width=50,
            font=("Courier", 12),
            bd=2,
            relief=tk.SUNKEN,
            padx=10,
            pady=10,
        )
        self.editor_area.pack(padx=5, pady=5, expand=True, fill=tk.BOTH)

        # Tokenized Code Section (Right side of code editor)
        token_output_frame = tk.Frame(io_frame, bg="#f0f0f0")
        token_output_frame.pack(
            side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH
        )

        token_output_label = tk.Label(
            token_output_frame,
            text="Compiled Code Output",
            font=("Courier", 12, "bold"),
            bg="#f0f0f0",
        )
        token_output_label.pack(anchor=tk.NW, pady=(0, 10))

        # Output area for compiled code output
        self.output_area = scrolledtext.ScrolledText(
            token_output_frame,
            wrap=tk.WORD,
            height=12,
            width=50,
            font=("Courier", 12),
            bd=2,
            relief=tk.SUNKEN,
            padx=10,
            pady=10,
        )
        self.output_area.pack(padx=5, pady=5, expand=True, fill=tk.BOTH)

        # Output Console Section (For tokenized code, below the editor and output)
        output_frame = tk.Frame(self, bg="#f0f0f0")
        output_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        output_label = tk.Label(
            output_frame,
            text="Built-in Console (Analysis Results)",
            font=("Courier", 12, "bold"),
            bg="#f0f0f0",
        )
        output_label.pack(anchor=tk.NW, pady=(0, 10))

        # Console area for showing analysis results
        self.console_area = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            height=8,
            width=100,
            font=("Courier", 12),
            bd=2,
            relief=tk.SUNKEN,
            padx=10,
            pady=10,
        )
        self.console_area.pack(padx=5, pady=5, expand=True, fill=tk.BOTH)

        # Store token stream, error list, and variable details (name, type)
        self.token_stream = []
        self.error_list = []
        self.variables = {}

        self.production_filename = "IOL_Grammar.prod"
        self.parse_table_filename = "IOL_ParseTable.ptbl"
        self.is_production_loaded = False
        self.is_parsetable_loaded = False

        self.productions_values = None
        self.parse_table_values = None
        self.token_stream_for_syntax_analysis = None

    # Clear editor, output, and console when creating a new file
    def new_file(self):
        self.editor_area.delete(1.0, tk.END)
        self.file_path = None
        # Clear output and console areas when a new file is opened
        self.output_area.config(state="normal")
        self.output_area.delete(1.0, tk.END)
        self.output_area.config(state="disabled")
        self.console_area.config(state="normal")
        self.console_area.delete(1.0, tk.END)
        self.console_area.config(state="disabled")

    # Open file, read content, and populate editor area
    def open_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("IOL files", "*.iol")])
        if self.file_path:
            with open(self.file_path, "r") as file:
                code = file.read()
            self.editor_area.delete(1.0, tk.END)
            self.editor_area.insert(tk.END, code)

    # Save file if file path exists
    def save_file(self):
        if self.file_path:
            with open(self.file_path, "w") as file:
                file.write(self.editor_area.get(1.0, tk.END).strip())
            messagebox.showinfo("Info", "File saved successfully.")
        else:
            self.save_file_as()

    # Prompt user for a new file path to save the file
    def save_file_as(self):
        self.file_path = filedialog.asksaveasfilename(
            defaultextension=".iol", filetypes=[("IOL files", "*.iol")]
        )
        if self.file_path:
            with open(self.file_path, "w") as file:
                file.write(self.editor_area.get(1.0, tk.END).strip())
            messagebox.showinfo("Info", "File saved successfully.")

    # Compile the code and perform lexical analysis
    def compile_code(self):
        """
        Handles the compilation of code entered by the user.
        """
        # Get the code from the editor area
        code = self.editor_area.get(1.0, tk.END).strip()
        if not code:
            messagebox.showwarning("Warning", "Input program code is empty.")
            return

        # Reset variables and token stream to ensure fresh compilation
        self.variables = {}  # Clear existing variables
        self.token_stream = []  # Clear existing tokens
        self.error_list = []  # Clear previous errors

        # Perform lexical analysis
        self.token_stream = self.lexical_analysis(code)

        # Update UI elements
        self.output_area.config(state="normal")
        self.output_area.delete(1.0, tk.END)  # Clear previous output
        self.console_area.config(state="normal")
        self.console_area.delete(1.0, tk.END)  # Clear previous console output

        if self.error_list:
            self.display_lexical_errors()
        else:
            self.output_area.insert(
                tk.END, "Compilation successful! No lexical errors found.\n\n"
            )
            self.display_variables_table()

            # Prompt for inputs (every time `compile_code` is called)
            self.prompt_for_inputs()

        # Lock the UI elements to prevent unintended edits
        self.output_area.config(state="disabled")
        self.console_area.config(state="disabled")
        
    def prompt_for_inputs(self):
        """
        Sequentially prompts the user for input values for variables
        that are referenced by the BEG command.
        """
        i = 0  # Pointer to iterate through the token stream
        while i < len(self.token_stream):
            line_num, lexeme, token = self.token_stream[i]

            if token == "BEG":
                # Check the next token for the variable name
                if i + 1 < len(self.token_stream):
                    next_line_num, next_lexeme, next_token = self.token_stream[i + 1]

                    if next_token == "IDENT" and next_lexeme in self.variables:
                        var_name = next_lexeme
                        var_type = self.variables[var_name]["type"]

                        # Prompt user for input based on variable type
                        try:
                            if var_type == "INT":
                                input_value = simpledialog.askinteger(
                                    "Input Required",
                                    f"Enter an integer value for {var_name}:",
                                    parent=self,
                                )
                            elif var_type == "STR":
                                input_value = simpledialog.askstring(
                                    "Input Required",
                                    f"Enter a string value for {var_name}:",
                                    parent=self,
                                )

                            if input_value is not None:  # User provided input
                                self.variables[var_name]["value"] = input_value
                                print(f"Input received for {var_name}: {input_value}")
                            else:
                                messagebox.showwarning(
                                    "Input Cancelled",
                                    f"No value provided for {var_name}.",
                                )
                        except ValueError:
                            messagebox.showerror(
                                "Invalid Input",
                                f"Invalid input for {var_name}. Expected type: {var_type}.",
                            )
                        i += 1  # Skip the variable token as it's processed
                    else:
                        messagebox.showerror(
                            "Undeclared Variable",
                            f"Variable '{next_lexeme}' is not declared. Cannot request input.",
                        )
                else:
                    messagebox.showerror(
                        "Syntax Error", f"BEG on line {line_num} is missing a variable."
                    )
            i += 1  # Move to the next token

        # Update the variable table after all inputs are collected
        self.display_variables_table()

    # Show tokenized code in the console area
    def show_tokenized_code(self):
        if not self.token_stream:
            messagebox.showinfo(
                "Info", "No tokenized code available. Compile the code first."
            )
            return

        self.console_area.config(state="normal")  # Allow editing to update content
        self.console_area.delete(1.0, tk.END)
        token_content = ""
        for line_num, lexeme, token in self.token_stream:
            # Skip newline tokens for readability
            if token == "NEWLN":
                continue
            token_content += f"Line {line_num}: {lexeme} -> {token}\n"

        self.console_area.insert(tk.END, token_content)
        self.console_area.config(state="disabled")  # Make it non-editable after updating

    # Save the tokenized output to a file
    def save_token_file(self):
        if not self.token_stream:
            messagebox.showwarning(
                "Warning", "No tokenized output available. Compile the code first."
            )
            return

        # Save tokens with line numbers
        token_content = "\n".join(
            f"{line_num} -> {lexeme} -> {token}" for line_num, lexeme, token in self.token_stream if token != "NEWLN"
        )
        with open(self.token_file_path, "w") as file:
            file.write(token_content)
        messagebox.showinfo(
            "Info", f"Tokenized output saved as {self.token_file_path}."
        )
        self.token_saved = True

        # Trigger Syntax and Semantic Analysis after saving the tokens
        syntax_analysis_success = self.syntax_analysis()
        if not syntax_analysis_success:
            return

        self.semantic_analysis()

    # Perform lexical analysis to generate tokens and identify errors
    def lexical_analysis(self, code):
        tokens = []
        self.error_list = []
        keywords = {
            "IOL",
            "LOI",
            "INTO",
            "IS",
            "BEG",
            "NEWLN",
            "PRINT",
            "ADD",
            "SUB",
            "MULT",
            "DIV",
            "MOD",
        }
        types = {"INT", "STR"}
        lines = code.splitlines()

        for line_num, line in enumerate(lines, start=1):
            words = line.split()
            if not words:
                continue

            for i, word in enumerate(words):
                if word in keywords or word in types:
                    tokens.append((line_num, word, word))
                    if word in types and i + 1 < len(words):
                        var_name = words[i + 1]
                        if var_name.isidentifier():
                            default_value = 0 if word == "INT" else "Unassigned"
                            self.variables[var_name] = {
                                "type": word,
                                "value": default_value,
                            }
                        else:
                            self.error_list.append(
                                f"Invalid identifier '{var_name}' on line {line_num}"
                            )
                elif word.isdigit():
                    tokens.append((line_num, word, "INT_LIT"))
                elif word.isidentifier():
                    tokens.append((line_num, word, "IDENT"))
                else:
                    tokens.append((line_num, word, "ERR_LEX"))
                    self.error_list.append(f"Unknown lexeme '{word}' on line {line_num}")

            # Add a NEWLN token at the end of each line
            last_word = words[-1]
            if not last_word.endswith("LOI"):
                tokens.append((line_num, "\\n", "NEWLN"))

        return tokens

    def parse_tokens_with_grammar(self, productions: list, parse_table: dict) -> Tuple[bool, str]:
        """
        Parses tokens from the input field using a specified grammar.

        Args:
            productions (list): List of production rules as (line_number, non_terminal, production).
            parse_table (dict): Dictionary representing the parse table.

        Returns:
            bool: True if the input is valid based on the grammar; False otherwise.
        """
        input_tokens = [token for _, __, token in self.token_stream]
        error_msg = None
        if not input_tokens:
            error_msg = "Error: No input tokens provided!"
            print(error_msg)
            return False, error_msg

        starting_production_rule = productions[0][
            1
        ]  # Start symbol is the LHS of the first production
        stack = [starting_production_rule]
        input_buffer = input_tokens + ["$"]
        parsing_steps = []
        is_valid = True

        while stack:
            stack_top = stack[-1]
            current_input = input_buffer[0]

            # Match terminal symbols
            if stack_top == current_input:
                stack.pop()
                input_buffer.pop(0)
                action = f"Match {stack_top}"
                print(action)

            # Expand non-terminal symbols
            elif stack_top in parse_table:
                if current_input in parse_table[stack_top]:
                    production_number = parse_table[stack_top][current_input]
                    if production_number == "":
                        error_msg = f"Error: No rule found for {stack_top} with input {current_input}"
                        print(error_msg)
                        is_valid = False
                        break
                    else:
                        stack.pop()
                        production = productions[int(production_number) - 1]
                        rhs = production[2].split() if production[2] != "e" else []
                        stack.extend(reversed(rhs))
                        action = f"Output {production[1]} -> {production[2]}"
                        print(action)
                else:
                    error_msg = f"Error: No matching terminal for {stack_top} with input {current_input}"
                    print(error_msg)
                    is_valid = False
                    break

            # Handle unexpected tokens
            else:
                error_msg = f"Error: Unexpected token {stack_top}"
                print(error_msg)
                is_valid = False
                break

            parsing_steps.append((stack.copy(), input_buffer.copy(), action))

        # Ensure input buffer is exhausted
        if input_buffer != ["$"]:
            error_msg = "Error: Input buffer not exhausted."
            print(error_msg)
            return False, error_msg

        return is_valid, error_msg

    def load_productions(self, file_path):
        """
        Loads production rules from a .prod file.

        Args:
            file_path (str): Path to the production file.

        Returns:
            list: List of production rules.
        """
        productions = []
        with open(file_path, newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                productions.append(row)
        return productions

    def load_parse_table(self, file_path):
        """
        Loads parse table from a .ptbl file.

        Args:
            file_path (str): Path to the parse table file.

        Returns:
            dict: Dictionary representing the parse table.
        """
        parse_table = {}
        with open(file_path, newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            headers = next(reader)[1:]
            for row in reader:
                non_terminal = row[0]
                parse_table[non_terminal] = {
                    headers[i]: row[i + 1] for i in range(len(headers))
                }
        return parse_table

    # Placeholder function for syntax analysis
    def syntax_analysis(self):
        if not self.token_saved:
            messagebox.showwarning("Warning", "Please save the tokenized output first.")
            return False

        self.console_area.config(state="normal")  # Ensure we can insert text
        self.console_area.insert(tk.END, "----------------------------------------------\n")
        self.console_area.insert(tk.END, "Loading tokens for Syntax Analysis...\n")
        self.console_area.config(state="disabled")  # Disable editing after inserting text

        productions_values = self.load_productions(self.production_filename)
        parse_table_values = self.load_parse_table(self.parse_table_filename)

        self.console_area.config(state="normal")  # Re-enable insertion for next step
        self.console_area.insert(tk.END, "Performing Syntax Analysis...\n")

        result, error_msg = self.parse_tokens_with_grammar(
            parse_table=parse_table_values, productions=productions_values
        )

        # Display syntax analysis errors
        if not result:
            self.console_area.insert(tk.END, "Syntax Analysis unsuccessful.\n\nSyntax Errors:\n" + error_msg)
        else:
            self.console_area.insert(tk.END, "Syntax Analysis successful! No syntax errors found.\n")

        self.console_area.insert(tk.END, "\nSyntax Analysis completed.\n")
        self.console_area.config(state="disabled")  # Disable editing after completion

        return result

    def semantic_analysis(self) -> bool:
        if not self.token_saved:
            messagebox.showwarning("Warning", "Please save the tokenized output first.")
            return False

        self.console_area.config(state="normal")
        self.console_area.insert(tk.END, "----------------------------------------------\n")
        self.console_area.insert(tk.END, "Loading tokens for Static Semantic Analysis...\n")
        self.console_area.config(state="disabled")

        # Load tokens and add debug statement
        self.load_tokens()
        print("Tokens loaded successfully.")
        print("Token Stream:", self.token_stream)

        self.console_area.config(state="normal")
        self.console_area.insert(tk.END, "Performing Semantic Analysis...\n")

        # Initialize semantic errors list
        semantic_errors = []

        # Store input values in a dictionary
        input_values = {}

        # Start processing each token in the token stream
        stack = []
        current_var = None

        print("Starting semantic analysis loop...")  # Debug line

        def get_input_value(var_name, var_type):
            # Check if input has already been provided for the variable
            if var_name in input_values:
                return input_values[var_name]  # Return previously stored value

            # Prompt for input only if it's not already provided
            input_value = None
            if var_type == "INT":
                input_value = simpledialog.askinteger("Input Required", f"Enter an integer value for {var_name}:")
                if input_value is None:  # If user cancels or closes the dialog
                    raise ValueError(f"No input provided for {var_name}. Semantic Analysis aborted.")
            elif var_type == "STR":
                input_value = simpledialog.askstring("Input Required", f"Enter a string value for {var_name}:")
                if input_value is None:  # If user cancels or closes the dialog
                    raise ValueError(f"No input provided for {var_name}. Semantic Analysis aborted.")

            input_values[var_name] = input_value  # Store the input value in the dictionary
            return input_value

        for i, (line_num, lexeme, token) in enumerate(self.token_stream):
            # Handling declarations
            if token in {"INT", "STR"}:
                stack.append(("DECLARATION", token))
                current_var = lexeme
                # Initialize variable with default values based on type
                self.variables[current_var] = {"type": token, "value": None}

            elif token == "IDENT":  # Handling identifier usage
                var_name = lexeme
                if var_name not in self.variables:
                    semantic_errors.append(f"Line {line_num}: Undeclared variable '{var_name}' used.")
                elif stack and stack[-1][0] == "DECLARATION":
                    stack.pop()
                else:
                    current_var = var_name  # Store current variable for assignment or input

            elif token == "INTO":
                if current_var:
                    stack.append(("ASSIGNMENT", current_var))
                else:
                    semantic_errors.append(f"Line {line_num}: Missing variable in assignment.")

            elif token == "IS":  # Handles the 'IS' keyword for assignment
                if stack and stack[-1][0] == "ASSIGNMENT":
                    var_name = stack.pop()[1]  # Get variable to assign
                    if var_name not in self.variables:
                        semantic_errors.append(f"Line {line_num}: Undeclared variable '{var_name}' in assignment.")

            elif token in {"ADD", "SUB", "MULT", "DIV", "MOD"}:  # Arithmetic operations
                if current_var in self.variables:
                    type1 = self.variables[current_var]["type"]
                    if type1 != "INT":
                        semantic_errors.append(
                            f"Line {line_num}: Type mismatch: {token} operation requires INT, found {type1}."
                        )
                else:
                    semantic_errors.append(f"Line {line_num}: Invalid operation, variable '{current_var}' not found.")

            elif token == "INT_LIT":
                if stack and stack[-1][0] == "ASSIGNMENT":
                    var_name = stack.pop()[1]  # Get variable to assign
                    if self.variables[var_name]["type"] != "INT":
                        semantic_errors.append(
                            f"Line {line_num}: Type mismatch: Cannot assign INT_LIT to '{var_name}' of type '{self.variables[var_name]['type']}'."
                        )
                    else:
                        self.variables[var_name]["value"] = int(lexeme)
                elif current_var in self.variables and self.variables[current_var]["type"] == "INT":
                    self.variables[current_var]["value"] = int(lexeme)
                else:
                    semantic_errors.append(f"Line {line_num}: Type mismatch or missing assignment context for '{current_var}'.")

            elif token == "BEG":  # Input operation after BEG keyword
                if i + 1 < len(self.token_stream):
                    next_token = self.token_stream[i + 1]
                    next_lexeme = next_token[1]
                    if next_lexeme in self.variables:
                        var_name = next_lexeme
                        var_type = self.variables[var_name]["type"]

                        # Get input value dynamically from user
                        input_value = get_input_value(var_name, var_type)
                        self.variables[var_name]["value"] = input_value
                        print(f"Input received for {var_name}: {input_value}")
                    else:
                        semantic_errors.append(f"Line {line_num}: Undeclared variable '{next_lexeme}' used in input operation.")
                else:
                    semantic_errors.append(f"Line {line_num}: Missing variable after BEG command.")

            elif token == "PRINT":  # Output operation
                if i + 1 < len(self.token_stream):
                    next_token = self.token_stream[i + 1]
                    next_lexeme = next_token[1]
                    next_token_type = next_token[2]
                    if next_lexeme in self.variables:
                        output_value = self.variables[next_lexeme]['value']
                        print(f"DEBUG: PRINT operation for variable '{next_lexeme}': {output_value}")
                        self.console_area.insert(tk.END, f"Line {line_num} Output: {output_value}\n")
                    elif next_lexeme.isdigit():
                        output_value = next_lexeme
                        print(f"DEBUG: PRINT operation for digit '{next_lexeme}'")
                        self.console_area.insert(tk.END, f"Line {line_num} Output: {output_value}\n")
                    elif next_token_type in {"ADD", "SUB", "MULT", "DIV", "MOD"}:
                        semantic_errors.append(f"Line {line_num}: Invalid operation '{next_lexeme}' in PRINT statement.")
                    else:
                        print(f"DEBUG: Invalid expression in PRINT operation for lexeme: {next_lexeme}")
                        semantic_errors.append(f"Line {line_num}: Invalid expression in PRINT operation.")
                else:
                    semantic_errors.append(f"Line {line_num}: Missing expression after PRINT command.")

            elif token == "NEWLN":  # Handle new line
                self.console_area.insert(tk.END, "\n")
            
            elif token in {"IOL", "LOI"}:  # Handle special tokens
                continue  # Just ignore these tokens for now

            else:
                print(f"DEBUG: Unhandled token: {token} with lexeme: {lexeme}")

        # Display results of semantic analysis
        if semantic_errors:
            error_msg = "Static Semantic Analysis unsuccessful.\n\nSemantic Errors:\n" + "\n".join(semantic_errors)
            self.console_area.insert(tk.END, error_msg)
        else:
            self.console_area.insert(tk.END, "Static Semantic Analysis successful! No semantic errors found.\n")

        self.console_area.insert(tk.END, "\nStatic Semantic Analysis completed.\n\n")
        return not semantic_errors

    # Load tokens from the saved .tkn file for analysis.
    def load_tokens(self):
        self.token_stream = []
        try:
            with open(self.token_file_path, "r") as file:
                for line in file:
                    # Parse line number, lexeme, and token
                    line_num, lexeme, token = line.strip().split(" -> ")
                    self.token_stream.append((int(line_num), lexeme, token))
            self.console_area.insert(tk.END, "Tokens loaded successfully.\n")
        except FileNotFoundError:
            messagebox.showerror(
                "Error", f"Token file '{self.token_file_path}' not found."
            )
        except Exception as e:
            messagebox.showerror(
                "Error", f"An error occurred while loading tokens: {e}"
            )

    def display_lexical_errors(self):
        error_msg = "Lexical Errors:\n"
        error_msg += "\n".join(self.error_list)
        self.output_area.insert(tk.END, error_msg)

    def display_variables_table(self):
        # Calculate the longest variable name for dynamic column width
        max_var_length = max((len(var) for var in self.variables), default=8)
        var_col_width = max(max_var_length, len("Variable")) + 2
        type_col_width = max(len("Type"), 10) + 2
        value_col_width = max(len("Value"), 15) + 2

        # Clear the info area and add the header for the table
        self.output_area.delete(1.0, tk.END)
        header = f"{'Variable':<{var_col_width}} {'Type':<{type_col_width}} {'Value':<{value_col_width}}\n"
        self.output_area.insert(tk.END, header)
        self.output_area.insert(
            tk.END, "-" * (var_col_width + type_col_width + value_col_width) + "\n"
        )

        # Display each variable with its name, type, and value
        for variable, details in self.variables.items():
            var_type = details.get("type", "Unassigned")
            value = details.get("value", "Unassigned")
            row = f"{variable:<{var_col_width}} {var_type:<{type_col_width}} {value:<{value_col_width}}\n"
            self.output_area.insert(tk.END, row)

# Run the application
if __name__ == "__main__":
    app = CompilerUI()
    app.mainloop()