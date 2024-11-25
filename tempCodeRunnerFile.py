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