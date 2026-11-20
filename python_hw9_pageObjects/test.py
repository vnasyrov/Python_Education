def show(*args):
    print(args)

values = ('Maths', 'Physics')

show(values)      # строка 1
show(*values)     # строка 2
