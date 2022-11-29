#Simple program on ExecComp

import openmdao.api as om 
import numpy as np

'''prob=om.Problem()
model=prob.model

model.add_subsystem('comp',om.ExecComp('y=x+1'))
model.set_input_defaults('comp.x',2.0)

prob.setup()
prob.run_model()
print(prob.get_val('comp.y'))'''

#Multiple outputs 
'''prob=om.Problem()
model=prob.model

model.add_subsystem('comp',om.ExecComp(['y1=x+1','y2=x-1']),promotes=['x'])
prob.setup()
prob.set_val('x',2.0)
prob.run_model()

print(prob.get_val('comp.y1'))
print(prob.get_val('comp.y2'))'''

#ARRAYS
'''prob=om.Problem()
model=prob.model

model.add_subsystem('comp',om.ExecComp('y=x[1]',x=np.array([1,2,3]),y=0))
prob.setup()
prob.run_model()
print(prob.get_val('comp.y'))'''

#MATH FUNCTIONS 

'''prob = om.Problem()
model = prob.model

model.add_subsystem('comp', om.ExecComp('z = sin(x)**2 + cos(y)**2'))

prob.setup()

prob.set_val('comp.x', np.pi/2.0)
prob.set_val('comp.y', np.pi/2.0)

prob.run_model()

print(prob.get_val('comp.z'))'''

#VARIABLE PROPERTIES 
'''prob = om.Problem()
model = prob.model

model.add_subsystem('comp', om.ExecComp('z=x+y',
                                        x={'val': 0.0, 'units': 'inch'},
                                        y={'val': 0.0, 'units': 'inch'},
                                        z={'val': 0.0, 'units': 'inch'}))

prob.setup()

prob.set_val('comp.x', 12.0, units='inch')
prob.set_val('comp.y', 1.0, units='ft')

prob.run_model()

print(prob.get_val('comp.z'))'''

#DAIGONAL PARTS 
'''p=om.Problem()
model=p.model

model.add_subsystem('comp',om.ExecComp('y=3*x+2.5', has_diag_partials=True,x=np.ones(5),y=np.ones(5)))
p.setup()
p.set_val('comp.x',np.ones(5))
p.run_model()

J=p.compute_totals(of=['comp.y'],wrt=['comp.x'],return_format='array')
print(J)
'''
#OPTIONS
#variables share same shape set up by constructor and common units specified by setting the option 
'''model=om.Group()
xcomp=model.add_subsystem('comp',om.ExecComp('y=2*x',shape=(2,)))
xcomp.options['units']='m'
p=om.Problem(model)
p.setup()
p.set_val('comp.x',[100,200],units='cm')
p.run_model()
print(p.get_val('comp.y'))'''

#USER FUNCTION REGISTRATION

'''try:
    om.ExecComp.register("my func",lambda x:x*x,complex_safe=True)
except NameError:
    pass
p=om.Problem()
comp=p.model.add_subsystem("comp",om.ExecComp("y=2*myfunnc(x)"))
p.setup()
p.run_model()
J=p.compute_totals(of=['comp.y'],wrt=['comp.x'])
print(J['comp.y',''comp.x][0][0])
'''
#COMPLEX UNSAFE USER FUNCTION REGISTRATION
'''try:
    om.ExecComp.register("unsafe", lambda x: x * x, complex_safe=False)
except NameError:
    pass
p = om.Problem()
comp = p.model.add_subsystem("comp", om.ExecComp("y = 2 * unsafe(x)"))

# because our function is complex unsafe, we must declare that the partials
# with respect to 'x' use 'fd' instead of 'cs'
comp.declare_partials('*', 'x', method='fd')

p.setup()
p.run_model()
J = p.compute_totals(of=['comp.y'], wrt=['comp.x'])
print(J['comp.y', 'comp.x'][0][0])'''

#ADDING EXPRESSION 
'''import numpy as np

class ConfigGroup(om.Group):
    def setup(self):
        excomp = om.ExecComp('y=x',
                             x={'val' : 3.0, 'units' : 'mm'},
                             y={'shape' : (1, ), 'units' : 'cm'})

        self.add_subsystem('excomp', excomp, promotes=['*'])

    def configure(self):
        self.excomp.add_expr('z = 2.9*x',
                             z={'shape' : (1, ), 'units' : 's'})

p = om.Problem()
p.model.add_subsystem('sub', ConfigGroup(), promotes=['*'])
p.setup()
p.run_model()

print(p.get_val('z'))
print(p.get_val('y'))''''

#CONSTANTS 
'''prob = om.Problem()
C1 = prob.model.add_subsystem('C1', om.ExecComp('x = a + b'))
prob.setup()
prob.set_solver_print(level=0)
prob.run_model()
print(list(C1._inputs._names))
['C1.a','C1.b']'''

'''prob = om.Problem()
C1 = prob.model.add_subsystem('C1', om.ExecComp('x = a + b', a={'val': 6, 'constant':True}))
prob.setup()
prob.set_solver_print(level=0)
prob.run_model()
print(list(C1._inputs._names))
['C1.b']'''

