import openmdao.api as om 

class parab(om.ExplicitComponent):

    def setup(self):
        self.add_input('x',0.0)
        self.add_input('y',0.0)
        self.add_output('f_xy',0.0)

    def setup_partials(self):
        self.declare_partials('*','*',method='fd')
        return super().setup_partials()

    def compute(self, inputs, outputs):

        x=inputs['x']
        y=inputs['y']

        outputs['f_xy']= x**2.0 + 4.0*x*y +(y+4.0)**3.0
        return super().compute(inputs, outputs)

if __name__ == "__main__":

    model=om.Group()
    model.add_subsystem('para',parab())

    prob=om.Problem(model)
    prob.setup()

    prob.set_val('para.x',2.0)
    prob.set_val('para.y',3.0)

    prob.run_model()
    print(prob['para.f_xy'])


