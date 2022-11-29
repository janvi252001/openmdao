from openmdao.test_suite.components.sellar_feature import SellarMDAWithUnits
import numpy as np
import openmdao.api as om

#build the model
prob=om.Problem(model=SellarMDAWithUnits())

model=prob.model
model.add_design_var('z', lower=np.array([-10.0, 0.0]), upper=np.array([10.0, 10.0]))
model.add_design_var('x', lower=0.0, upper=10.0)
model.add_objective('obj')
model.add_constraint('con1', upper=0.0)
model.add_constraint('con2', upper=0.0)

#setup optimization
driver=prob.driver=om.ScipyOptimizeDriver(optimizer='SLSQP',tol=1e-9,disp=False)

#create a recorder variable 
recorder=om.SqliteRecorder('cases.sql')
#attah the recorder to the problem
prob.add_recorder(recorder)

prob.setup()
prob.set_solver_print(0)
prob.run_driver()
prob.record("after_run_driver")

#instantiate casereader
cr=om.CaseReader("cases.sql")
#isolate "problem" as your source 
driver_cases=cr.list_cases('problem',out_stream=None)
#get the first case from recorder
case=cr.get_case('after_run_driver')

# These options will give outputs as the model sees them
# Gets value but will not convert units
const=case['con1']
print(const)

# get_val can convert your result's units if desired
const_K = case.get_val("con1", units='K')

print(const_K)

# list_outputs will list your model's outputs and return a list of them too
print(case.list_outputs())

# This code below will find all the objectives, design variables, and constraints that the
# problem source contains
objectives = case.get_objectives()
print(objectives['obj'])

design_vars = case.get_design_vars()
print(design_vars['x'])

constraints = case.get_constraints()
print(constraints['con1'])
