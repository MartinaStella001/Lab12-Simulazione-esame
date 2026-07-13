from model.model import Model

mdl = Model()
mdl.creaGrafo(2018)
nodi, archi = mdl.getDetails()
print(f"nodi:{nodi}, archi:{archi}")