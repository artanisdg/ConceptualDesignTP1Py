import subprocess

avl = subprocess.Popen(["avl.exe"],stdin=subprocess.PIPE, text=True)

Specs = open("Specs1.csv","a")
Specs.write("C, R, S, V")
Specs.close()


print("PLOP",file=avl.stdin)
print("G",file=avl.stdin)
print(file=avl.stdin)
print("Quit",file=avl.stdin)

