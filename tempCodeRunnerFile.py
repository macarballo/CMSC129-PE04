    def prompt_for_inputs(self):
        """
        Sequentially prompts the user for input values for variables
        that are referenced by the BEG command.
        """
        skip_next = False  # To handle tokens after BEG
        for line_num, lexeme, token in self.token_stream:
            if skip_next:  # Skip next token if it was already processed
                skip_next = False
                continue
            
            if token == "BEG":
                # Assume the variable name comes immediately after BEG
                next_index = self.token_stream.index((line_num, lexeme, token)) + 1
                if next_index < len(self.token_stream):
                    next_line_num, next_lexeme, next_token = self.token_stream[next_index]
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
                    else:
                        messagebox.showerror(
                            "Undeclared Variable",
                            f"Variable '{next_lexeme}' is not declared. Cannot request input.",
                        )
                    skip_next = True  # Skip the next token as it's processed
                else:
                    messagebox.showerror(
                        "Syntax Error", f"BEG on line {line_num} is missing a variable."
                    )
        
        # Update the variable table after all inputs are collected
        self.display_variables_table()
