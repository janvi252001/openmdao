
from typing_extensions import Self
import openmdao.api as om
import numpy as np 

#INDEPENDENT VARIABLE 
#---------------------------------------------------------------------------------
#Defining independent variable and set  its value 

"""comp=om.IndepVarComp('indep_var')
prob=om.Problem(comp).setup()

print(prob.get_val('indep_var'))

prob.set_val('indep_var',2.0)
print(prob.get_val('indep_var'))"""

#DEFINING ONE INDEPENDENT VARIABLE WITH DEFAULT VALUE

'''comp=om.IndepVarComp('indep_var',2.0)#can also write val=2.0
prob=om.Problem(comp).setup()

print(prob.get_val('indep_var'))'''

#DEFINING ONE INDEPENDENT VAR WITH DEFAULT VALUE AND ADDITIONAL OPTIONS 

"""comp=om.IndepVarComp('indep_var',2.0,units='m',lower=10,upper=0)
prob=om.Problem(comp).setup()

print(prob.get_val('indep_var'))"""

#Define one independent array variable

"""array=np.array([[1.,2,],[3.,4,],])
comp=om.IndepVarComp('indep_var',val=array)
prob=om.Problem(comp).setup()

print(prob.get_val('indep_var'))"""

#Define two independent variables using the add_output method.
"""comp=om.IndepVarComp()
comp.add_output('indep_var1')
comp.add_output('indep_var2',2.0)

prob=om.Problem(comp).setup()

print(prob.get_val('indep_var1'))
print(prob.get_val('indep_var2'))"""
#-------------------------------------------------------------------------------------
#EXPLICIT COMPONENT 

class Rect(om.ExplicitComponent):
    
     def setup(self):
        self.add_input('length',val=1)
        self.add_input('width',val=1)
        self.add_output('area',val=1)

     def setup_partials():
        self.declare_partials('*','*')

     def compute(self,inputs,outputs):
        outputs['area']=input['length'] *  inputs['width']

     def compute_partials(self, inputs, partials):
      partials['area', 'length'] = inputs['width']
      partials['area', 'width'] = inputs['length']

    


    



    