# Programming Exercise 04 - Syntax Analysis

## Overview
This program implements a simple syntax and static semantic analyzer as a part of a custom compiler for a programming language. The program reads a stream of tokens generated by the lexical analyzer, performs syntax and semantic analysis, and outputs the result, including any errors detected during analysis.

The program is built using Python's **tkinter** library to provide a graphical user interface (GUI), where users can input code, compile it, and see the results of lexical, syntax, and semantic analysis.

## Features
- **Open File**: Load a source code file (.iol extension) into the editor.
- **Compile Code**: Analyze the input program code, perform lexical analysis, and display tokenization results.
- **Syntax and Semantic Analysis**: Automatically performed after lexical analysis, checking for syntax and semantic errors.
- **Show Tokenized Code**: Display the tokenized version of the input program.
- **Error Handling**: Detect and display lexical, syntax, and semantic errors, including line numbers.
- **Variable Table**: List all variables and their corresponding types after the code is compiled.
- **Save Token File**: The tokenized code can be saved to a .tkn file.

## Program Flow
1. **Open File or New File**: Users can load a program code from a file or manually enter code in the editor.
2. **Compile Code**: When the "Compile Code" button is clicked, the program performs lexical analysis on the input.
3. **Display Results**:
   - Lexical errors (if any) are displayed in the output area.
   - The list of variables and their types is shown in a table.
4. **Syntax and Semantic Analysis**: The program automatically performs syntax and static semantic analysis after lexical analysis. Any errors found are displayed in the output console.
5. **Show Tokenized Code**: Clicking this button will display the tokenized form of the input program in the output area.
6. **Save Token File**: The tokenized code can be saved for future reference as a .tkn file.

## Functionality Details

### Syntax Analysis
The syntax analyzer checks whether the sequence of tokens follows the grammatical rules of the custom programming language. If any syntax errors are found, they are reported with the line number.

### Semantic Analysis
The static semantic analyzer checks for issues related to variable declaration and usage, ensuring that all variables are properly declared and used according to the language's rules.

## Usage Instructions
1. **Open a File**: Click on "File" -> "Open File" to load an existing .iol file containing the program code.
2. **Write or Edit Code**: Alternatively, write or edit the code directly in the editor.
3. **Compile Code**: Press the "Compile Code" button to perform lexical analysis, followed by syntax and semantic analysis.
4. **View Tokenized Code**: Press "Show Tokenized Code" to view the tokenized output in the console.
5. **Save Tokenized Output**: Save the tokenized output by clicking "Save Tokenized Output."
