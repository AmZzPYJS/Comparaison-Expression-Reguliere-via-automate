from automate import *

A1 = union(automate("c"),etoile(union(automate("a"),automate("b"))))
A2 = union(etoile(union(automate("b"),automate("a"))),automate("c"))

if egal(A1, A2):
	print("EGAL")
else:
	print("NON EGAL")
