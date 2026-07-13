from model.model import Model

mdl = Model()
mdl.creaGrafo("Drama")
nodi,archi = mdl.getDettagliGrafo()
print(f"nodi:{nodi}, archi:{archi}")