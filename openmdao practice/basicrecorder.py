import openmdao.api as om 
import numpy as np

class SellarMDAWithUnits(om.Group):

    class SellarDis1Units(om.ExplicitComponent):

        def setup(self):

            self.add_input('z',val=np.zeros(2),units='degC')
            self.add_input('x',val=0,units='degC')
            self.add_input('y2',val=1.0,units='degC')
            self.add_output('y1',val=1.0,units='degC')

        def setup_partials(self):
            self.declare_partials('*','*',method='fd')
            return super().setup_partials()

        def compute(self,inputs,outputs):
            z1=inputs['z'][0]
            z2=inputs['z'][1]
            x1=inputs['x']
            y2=inputs['y2']

            outputs['y1']=z1**2+z2+x1-0.2*y2

    class SellarDis2Units(om.ExplicitComponent):

        def setup(self):
            self.add_input('z',val=np.zeros(2),units='degC')
            self.add_input('y1',val=1.0,units='degC')
            self.add_output('y2',val=1.0,units='degC')

        def setup_partials(self):
            self.declare_partials('*','*',method='fd')
            return super().setup_partials()

        def compute(self,inputs,outputs):
            z1=inputs['z'][0]
            z2=inputs['z'][1]
            y1=inputs['y1']

            if y1.real<0.0:
                y1*=-1

            outputs['y2']=y1**.5+z1+z2

    def setup(self):
        cycle = self.add_subsystem('cycle', om.Group(), promotes=['*'])
        cycle.add_subsystem('d1', self.SellarDis1Units(), promotes_inputs=['x', 'z', 'y2'],
                            promotes_outputs=['y1'])
        cycle.add_subsystem('d2', self.SellarDis2Units(), promotes_inputs=['z', 'y1'],
                            promotes_outputs=['y2'])

        cycle.set_input_defaults('x', 1.0, units='degC')
        cycle.set_input_defaults('z', np.array([5.0, 2.0]), units='degC')

        # Nonlinear Block Gauss Seidel is a gradient free solver
        cycle.nonlinear_solver = om.NonlinearBlockGS()

        self.add_subsystem('obj_cmp', om.ExecComp('obj = x**2 + z[1] + y1 + exp(-y2)',
                                                  z={'val': np.array([0.0, 0.0]), 'units': 'degC'},
                                                  x={'val': 0.0, 'units': 'degC'},
                                                  y1={'units': 'degC'},
                                                  y2={'units': 'degC'}),
                           promotes=['x', 'z', 'y1', 'y2', 'obj'])

        self.add_subsystem('con_cmp1', om.ExecComp('con1 = 3.16 - y1', y1={'units': 'degC'},
                                                   con1={'units': 'degC'}),
                           promotes=['con1', 'y1'])
        self.add_subsystem('con_cmp2', om.ExecComp('con2 = y2 - 24.0', y2={'units': 'degC'},
                                                   con2={'units': 'degC'}),
                           promotes=['con2', 'y2'])
    



