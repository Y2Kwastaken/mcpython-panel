from utils.panel_utils import Panel_Interface
from utils.cosmetics import cinput, cprint


def addStuff(panel: Panel_Interface):
    num1 = cinput("Input the first number you want to add: ")
    num2 = cinput("Input the second number you want to add: ")
    cprint(f'The Answer is {int(num1)+int(num2)}')
    panel.feedback.pause_panel()


def subtractStuff(panel: Panel_Interface):
    num1 = cinput("Input the first number you want to subtract: ")
    num2 = cinput("Input the second number you want to subtract: ")
    cprint(f'The Answer is {int(num1)-int(num2)}')
    panel.feedback.pause_panel()


def exit(panel: Panel_Interface):
    panel.close()


choices = {
    '0': ["Add", addStuff],
    '1': ["Subtract", subtractStuff],
    '2': ["Exit", exit]
}

def onCall():
    panel = Panel_Interface(choices, "Another", "&3", "Another Example Panel", "self")
    panel.launch()