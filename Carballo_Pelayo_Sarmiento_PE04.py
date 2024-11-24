import csv
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from typing import Tuple

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
        code = self.editor_area.get(1.0, tk.END).strip()
        if not code:
            messagebox.showwarning("Warning", "Input program code is empty.")
            return

        # Perform lexical analysis
        self.token_stream = self.lexical_analysis(code)
        self.output_area.config(state="normal")  # Allow editing to update content
        self.output_area.delete(1.0, tk.END)  # Clear output area
        self.console_area.config(state="normal")  # Allow editing to update content
        self.console_area.delete(1.0, tk.END)  # Clear token console

        if self.error_list:
            self.display_lexical_errors()
        else:
            self.output_area.insert(
                tk.END, "Compilation successful! No lexical errors found.\n\n"
            )
            self.display_variables_table()

        # Make the areas non-editable again
        self.output_area.config(state="disabled")
        self.console_area.config(state="disabled")

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

    # Placeholder function for semantic analysis
    def semantic_analysis(self) -> bool:
        if not self.token_saved:
            messagebox.showwarning("Warning", "Please save the tokenized output first.")
            return False

        self.console_area.config(state="normal")  # Ensure we can insert text
        self.console_area.insert(tk.END, "----------------------------------------------\n")
        self.console_area.insert(tk.END, "Loading tokens for Static Semantic Analysis...\n")
        self.console_area.config(state="disabled")  # Disable editing after inserting text

        self.load_tokens()

        self.console_area.config(state="normal")  # Re-enable insertion for next step
        self.console_area.insert(tk.END, "Performing Semantic Analysis...\n")

        # Initialize semantic errors list
        semantic_errors = []

        # Process each token in the token stream for semantic analysis
        stack = []  # To hold current context (declaration or assignment)

        for line_num, lexeme, token in self.token_stream:
            if token == "INT":  # Integer variable declaration
                stack.append(("DECLARATION", token))
                self.variables[lexeme] = {"type": token, "value": "0"}  # Initialize integer variable with default 0

            elif token == "STR":  # String variable declaration
                stack.append(("DECLARATION", token))
                self.variables[lexeme] = {"type": token, "value": ""}  # Initialize string variable with empty string

            elif token == "IDENT":  # Variable usage
                var_name = lexeme
                if var_name not in self.variables:
                    semantic_errors.append(f"Line {line_num}: Undeclared variable '{var_name}' used.")
                else:
                    # Ensure correct context of variable usage
                    if stack and stack[-1][0] == "DECLARATION":
                        stack.pop()  # Pop the declaration context after a variable is used

            elif token == "ASSIGN":  # Assignment operation
                if not stack:
                    semantic_errors.append(f"Line {line_num}: Invalid assignment outside declaration context.")
                stack.append(("ASSIGNMENT", lexeme))  # Track assignment for further checks

            elif token in ["ADD", "SUB", "MULT", "DIV", "MOD"]:  # Arithmetic operations
                # Look for the operands involved in the operation
                operand1 = lexeme
                operand2 = self.token_stream[line_num + 1][1]  # Assuming the next token is the second operand

                # Check types of the operands
                if operand1 in self.variables and operand2 in self.variables:
                    type1 = self.variables[operand1]["type"]
                    type2 = self.variables[operand2]["type"]

                    # Check if types are compatible for arithmetic operations (only INT allowed)
                    if type1 != "INT" or type2 != "INT":
                        semantic_errors.append(
                            f"Line {line_num}: Type mismatch: Cannot apply {token} to {operand1} ({type1}) and {operand2} ({type2})."
                        )
                    elif type1 != type2:
                        semantic_errors.append(
                            f"Line {line_num}: Type mismatch: Cannot apply {token} to operands of different types: {operand1} ({type1}) and {operand2} ({type2})."
                        )

            elif token == "STR_INPUT":  # User input for string type (STR)
                if stack and stack[-1][0] == "ASSIGNMENT":
                    var_name = stack.pop()[1]  # Pop the assignment, get the variable name
                    var_type = self.variables.get(var_name, {}).get("type", None)
                    if var_type and var_type != "STR":
                        semantic_errors.append(
                            f"Line {line_num}: Type mismatch: Cannot assign STR_INPUT to variable '{var_name}' of type '{var_type}'."
                        )

            elif token == "INT_LIT":  # Integer literal assignment
                if stack and stack[-1][0] == "ASSIGNMENT":
                    var_name = stack.pop()[1]  # Pop the assignment, get the variable name
                    var_type = self.variables.get(var_name, {}).get("type", None)
                    if var_type and var_type != "INT":
                        semantic_errors.append(
                            f"Line {line_num}: Type mismatch: Cannot assign INT_LIT to variable '{var_name}' of type '{var_type}'."
                        )

            elif token == "BEG":  # Input operation
                var_name = lexeme
                if var_name not in self.variables:
                    semantic_errors.append(f"Line {line_num}: Undeclared variable '{var_name}' used in input operation.")
                else:
                    var_type = self.variables.get(var_name, {}).get("type", None)
                    if var_type == "STR":
                        # Accept user input for string variables
                        continue
                    elif var_type == "INT":
                        # Accept user input for integer variables
                        continue
                    else:
                        semantic_errors.append(f"Line {line_num}: Invalid input type for variable '{var_name}'.")

            elif token == "PRINT":  # Output operation
                expr = lexeme
                if expr not in self.variables and not expr.isdigit():
                    semantic_errors.append(f"Line {line_num}: Invalid expression in PRINT operation. Must be a variable or literal.")
                elif expr in self.variables:
                    var_type = self.variables.get(expr, {}).get("type", None)
                    if var_type == "STR" or var_type == "INT":
                        continue

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
