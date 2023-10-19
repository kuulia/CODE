#import this file

def fun1():
    return 1

def clearvars(): #used for clearing all variables between different runs of main
    for el in sorted(globals()):
        if '__' not in el:
                print(f'deleted: {el}')
                del el

def write_benchmarks(filename, descriptor, runtimes):
    
    lines = [f'Benchmarks for {descriptor}\n',
              '#######################\n',
              f'The runtime of generating {descriptor} was: {runtimes[0]} ms \n',
              f'The runtime of the original lumiaro code for {descriptor} was: {runtimes[1]} ms \n',
              f'The runtime of the improved code for {descriptor} was: {runtimes[2]} ms \n',
              '#######################\n\n'
              ]
    with open(filename, 'a') as f:
        f.writelines(lines)