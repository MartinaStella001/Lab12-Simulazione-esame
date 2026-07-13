from model.model import Model

mdl = Model()
mdl.creaGrafo2(2000)
nodi, archi = mdl.getDettagliGrafo2()
print(f"nodi: {nodi}, archi: {archi}")