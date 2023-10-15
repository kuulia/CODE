#import this file

def fun1():
    return 1

def clearvars(): #used for clearing all variables between different runs of main
    for el in sorted(globals()):
        if '__' not in el:
                print(f'deleted: {el}')
                del el