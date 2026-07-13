from model.model import Model

mdl=Model()
mdl.creaGrafo(2.2)
nodi,archi = mdl.getDettagli()
print(f"nodi: {nodi},archi: {archi}")