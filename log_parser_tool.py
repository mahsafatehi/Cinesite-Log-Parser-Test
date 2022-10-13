from PySide2.QtWidgets import QApplication, QWidget, \
    QLabel, QFileDialog, QVBoxLayout, QTabWidget
import sys
import re


def log_parser(file_path):
    errors = []
    warnings = []
    renders = []
    memories = []
    line_number = 0
    all_errors = ""
    all_warnings = ""
    render_time = ""
    memory_usage = ""
    error = re.compile("error", re.IGNORECASE)  # Compile a case-insensitive regex
    warning = re.compile("warning", re.IGNORECASE)  # Compile a case-insensitive regex
    render = re.compile("render done in", re.IGNORECASE)  # Compile a case-insensitive regex
    memory = re.compile("memory used", re.IGNORECASE)  # Compile a case-insensitive regex
    with open(file_path, mode='r') as my_file:
        for line in my_file:
            line_number += 1
            if error.search(line) is not None:  # If a match is found
                errors.append((line_number, line.rstrip('\n')))
            elif warning.search(line) is not None:  # If a match is found
                warnings.append((line_number, line.rstrip('\n')))
            elif render.search(line) is not None:  # If a match is found
                renders.append((line_number, line.rstrip('\n')))
            elif memory.search(line) is not None:  # If a match is found
                memories.append((line_number, line.rstrip('\n')))
    for err in errors:  # Iterate over the list of tuples
        all_errors = all_errors + "Line " + str(err[0]) + ": " + err[1] + "\n"
    for war in warnings:  # Iterate over the list of tuples
        all_warnings = all_warnings + "Line " + str(war[0]) + ": " + war[1] + "\n"
    for ren in renders:  # Iterate over the list of tuples
        render_time = render_time + "Line " + str(ren[0]) + ": " + ren[1] + "\n"
    for mem in memories:  # Iterate over the list of tuples
        memory_usage = memory_usage + "Line " + str(mem[0]) + ": " + mem[1] + "\n"
    return [all_errors, all_warnings, render_time, memory_usage]


class Window(QWidget):
    def __init__(self):
        super().__init__()

        # Browser
        file_path, _ = QFileDialog.getOpenFileName(
            None
        )

        # Parser
        result = log_parser(file_path)

        # Window design
        layout = QVBoxLayout()
        label1 = QLabel(result[0])  # Add a label for all errors
        label2 = QLabel(result[1])  # Add a label for all warnings
        label3 = QLabel(result[2])  # Add a label for rendering time
        label4 = QLabel(result[3])  # Add a label for memory usage
        tab = QTabWidget()
        tab.addTab(label1, "Errors")  # Add a tab named errors
        tab.addTab(label2, "Warnings")  # Add a tab named warnings
        tab.addTab(label3, "Render Time")  # Add a tab named render time
        tab.addTab(label4, "Memory Usage")  # Add a tab named memory usage
        layout.addWidget(tab)
        self.setLayout(layout)
        self.setWindowTitle("Result")


if __name__ == '__main__':
    my_app = QApplication(sys.argv)
    window = Window()
    window.show()
    my_app.exec_()
    sys.exit()
