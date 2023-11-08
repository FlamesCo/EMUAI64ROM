import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QMessageBox

class CPU:
    def __init__(self):
        self.registers = [0] * 32
        self.pc = 0
        self.memory = [0] * 65536

    def load_program(self, program):
        for addr, value in enumerate(program):
            self.memory[addr] = value

    def fetch_instruction(self):
        instruction = self.memory[self.pc]
        self.pc += 1
        return instruction

    def execute_instruction(self, instruction):
        opcode = (instruction >> 26) & 0x3F
        rs = (instruction >> 21) & 0x1F
        rt = (instruction >> 16) & 0x1F
        rd = (instruction >> 11) & 0x1F
        imm = instruction & 0xFFFF

        if opcode == 0x20:  # Example: ADD instruction
            self.registers[rd] = self.registers[rs] + self.registers[rt]

    def run(self):
        while True:
            instruction = self.fetch_instruction()
            if instruction == 0:
                break
            self.execute_instruction(instruction)

class EmulatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("emuai64 GUI")
        self.setGeometry(100, 100, 400, 200)

        self.cpu = CPU()
        self.program_loaded = False

        load_button = QPushButton("Load Program", self)
        load_button.clicked.connect(self.load_program)
        load_button.setGeometry(50, 50, 150, 30)

        run_button = QPushButton("Run Program", self)
        run_button.clicked.connect(self.run_program)
        run_button.setGeometry(50, 100, 150, 30)
        run_button.setEnabled(False)

        quit_button = QPushButton("Quit", self)
        quit_button.clicked.connect(self.quit_emulator)
        quit_button.setGeometry(50, 150, 150, 30)

    def load_program(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Load Program", "", "Binary Files (*.bin)")
        if file_path:
            with open(file_path, 'rb') as file:
                program = list(file.read())
            self.cpu.load_program(program)
            self.program_loaded = True
            self.statusBar().showMessage("Program loaded successfully.")
            self.findChild(QPushButton, "Run Program").setEnabled(True)

    def run_program(self):
        if self.program_loaded:
            self.cpu.run()
            self.statusBar().showMessage("Program execution completed.")
        else:
            QMessageBox.critical(self, "Error", "No program loaded.")

    def quit_emulator(self):
        sys.exit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmulatorWindow()
    window.show()
    sys.exit(app.exec_())
