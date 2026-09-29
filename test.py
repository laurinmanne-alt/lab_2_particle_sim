import math
import inspect
import ast
import tkinter as tk

# Colors for nicer printouts
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
END = '\033[0m'
BOLD = '\033[1m'

def print_statistics(failing_method_or_class=""):
    global pass_tests, fail_tests, unimplemented
    all_tests = pass_tests+fail_tests+unimplemented

    print()
    if pass_tests:
       print(f"{GREEN} ✅ {pass_tests} out of {all_tests} passed.{END}")
    if fail_tests:
        print(f"{RED} ❌ {fail_tests} out of {all_tests} failed.{END}")
        if failing_method_or_class:
            print(f"In order to run further tests, {failing_method_or_class} must be implemented correctly.")
    if unimplemented:
        print(f"{YELLOW} 🚧 {unimplemented} out of {all_tests} unimplemented.{END}")
    if all_tests==0:
        print("Nothing has been implemented yet!")
    print() 

def test(fun, x, y, eq=lambda x, y: x == y, fname=None):
    global pass_tests, fail_tests
    if not fname:
        fname, lpar, rpar = fun.__name__, "(", ")"
    elif fname.endswith(","): # partially applied: f(arg1,
        lpar, rpar = " ", ")"
    else:
        lpar, rpar = "(", ")"
    if type(x) == tuple:
        z = fun(*x)
    else:
        z = fun(x)
    if eq(z, y):
        pass_tests = pass_tests + 1
    else:
        if isinstance(y, (list, zip)): # membership test, not equality
            eq_repr = "\nfound among:\n   "
        else:
            eq_repr = "=="

        print("Condition failed:")
        print(f"Expected:\n    {fname}{lpar}{x}{rpar} {eq_repr} {y}")
        print(     f"Got:\n    {fname}{lpar}{x}{rpar} == {z}")
        fail_tests = fail_tests + 1

def diff(gold, user): # To print out useful diffs
    diff = []
    gold_dict = gold.__dict__
    user_dict = user.__dict__

    for key in gold_dict:
        if key not in user_dict:
            diff.append(f"Missing attribute: {key}")
        elif (gval := gold_dict[key]) != (uval := user_dict[key]):
            msg = ["",
                f"*** expected: {key}={gval}",
                f"!!!      got: {RED}{key}={uval}{END}",
                ""]
            diff.append("\n".join(msg))
    return "\n".join(diff)

def test_particles(fname, ps, qs, eq=lambda x, y: x==y):
    global pass_tests, fail_tests
    for p,q in zip(ps,qs):
        try:
            assert eq(p, q)
        except AssertionError:
            print(f"Particle.{fname}:", end=" ")
            if hasattr(q, '__dict__'):
                print()
                print(diff(q, p))
            elif isinstance(q, (list, tuple, zip)):
                print(f"multiple correct answers were tried but none matched.")
                print("Your solution should match one of the solutions below:")
                print()
                for i in q:
                    print(f"{diff(i, p)}")
            else:
                print(f"   Expected  {p}\nto be equal to, contained among, or some other way similar to\n{q}")
            fail_tests += 1
        else:
            pass_tests += 1

def test_class_basics(cls, num_args, attr_names, typecorrect_args):
    global pass_tests, fail_tests, unimplemented
    clsname = cls.__name__
    taskname = {"Vec":"Task 2", "Particle":"Task 4"}[clsname]

    # Class needs to have a constructor
    if "__init__" in cls.__dict__:
        pass_tests += 1
    else:
        fail_tests += 1
        print(f"class {cls.__name__} must have a {BOLD}constructor{END}, i.e. a method called __init__", end=" ")
        if hasattr(cls, "__innit__"):
            print(f"(spelled with {BOLD}one{END} n)")
        else:
            print()
        return

    # Constructor needs to have correct number of arguments
    sig = inspect.signature(cls.__init__)
    args = [p for p in sig.parameters.values() if p.name != 'self']

    if len(args) == num_args:
        pass_tests += 1
    else:
        fail_tests += 1
        print(f"class {clsname} should be initialized {BOLD}exactly as it says{END} in {taskname}.")
        return
    
    # Constructor needs to be called successfully
    try: # Create instance with right number of Nones
        dummy_value = cls(*[None] * num_args)
        pass_tests += 1
    except Exception:
        # If student is doing their own data validation, try constructing dummy_value with correct types
        try:
            dummy_value = cls(*typecorrect_args)
            pass_tests += 1
        except Exception:
            # Constructor failed for other reasons
            print(f"Constructing a {clsname} object failed.")
            print("Please check:")
            print(f" - have you followed the instructions in {taskname}?")
            print(f" - does the code have typos, undefined variables, ...?")
            fail_tests += 1
            return

    # Instance variables need to exist and have correct names
    attributes_wrong = False
    for attr in attr_names:
      if hasattr(dummy_value, attr):
        pass_tests += 1
      else:
        print(f"{clsname} has no attribute {BOLD}{attr}{END} yet.")
        fail_tests += 1
        attributes_wrong = True
    if attributes_wrong:
        print("Please check:")
        if len(attr) > 1:
            print("- is the name correct?", end=" ")
            print(f"e.g. {BOLD}{attr}{END}, not {BOLD}{attr[0]}{END}")        
        print(f"- did you forget {BOLD}self{END}?")

def test_and_print_issues_with_dunder_methods(method, method_name, verbose=True):
    source = inspect.getsource(method)
    source_lines = source.splitlines()
    tree = ast.parse(source.lstrip())
    issues = {}
    for node in ast.walk(tree):
        if (isinstance(node, ast.Attribute) and 
            isinstance(node.value, (ast.Name, ast.Attribute)) and
            node.attr in ('x', 'y')):
            full_line = source_lines[node.lineno - 1].strip()
            issues[ast.unparse(node)] = full_line

    # If verbose, just print out all the issues
    if issues and verbose:
        print(f"Problems in {method_name}:")
        for attr,line in issues.items():
            print("  -", f"Manually accessing {BOLD}{attr}{END} on line: {BOLD}{line}{END}")
        print()
        print("Remember that your Vec class has special methods like __rmul__ and __add__.")
        print("Thanks to them, you can use vectors like any mathematical objects. For instance:")
        print(f"if {BOLD}u{END} and {BOLD}v{END} are vectors and {BOLD}f{END} a floating point, then you should write {BOLD}u+v{END}, {BOLD}f*u{END}, etc.")

    # Also returns the issues, use with verbose=False if you prefer different output
    return issues

def _load_modules():
    try:
        import model
    except:
        print("The file model.py not found, or it contains syntax errors.")
        model = None

    try:
        import view
    except:
        print("The file view.py not found, or it contains syntax errors.")
        view = None
    return model, view


def _run_tests(model, view=None):
    global pass_tests, fail_tests, unimplemented

    pass_tests = 0
    fail_tests = 0
    unimplemented = 0

    if not hasattr(model, "Vec"):
        print_statistics()
        print("Hint: start from class Vec in model.py.")
        return []
    
    test_class_basics( \
        cls=model.Vec, num_args=2, \
        attr_names=["x", "y"], typecorrect_args=[1.3, -0.6])

    # If basic tests failed, don't go further
    if fail_tests:
        print_statistics("the Vec class")
        print()
        return []

    class Vec(model.Vec):
      """Extend the user's Vec class with custom equality and repr"""
      def __eq__(self, other, epsilon=1e-9):
        try:
            return math.isclose(self.x, other.x, rel_tol=epsilon) \
            and math.isclose(self.y, other.y, rel_tol=epsilon)
        except:
            return False
      
      def __repr__(self):
        """To produce error messages that the student can copy and paste
        directly into a Python shell, e.g.

          Expected:
              to_canvas_coords(canvas, Vec(10,10))
          found among:
              [… list of accepted answers …]
        """
        return f"Vec({self.x},{self.y})"
    
      if hasattr(model.Vec, "get_coords"):
        def get_coords(self):
            """Better error msg if student returns a Vec instead of tuple"""
            result = super().get_coords()
            if isinstance(result, model.Vec):
                return Vec(result.x, result.y)
            else:
                return result
    
    if hasattr(model, "dot"):
        u1 = Vec(0.123, 4.456)
        u2 = Vec(0.654, -2.09)
        test(model.dot, (u1,u2), -9.232598000000001)
    else:
        unimplemented += 1
        print("dot is not implemented yet!\n")

    if hasattr(Vec, "get_coords"):
        u1 = Vec(0.123, 4.456)
        test(Vec.get_coords, u1, (0.123, 4.456))
        if isinstance(Vec.get_coords(u1), Vec):
            print()
            print(f"{RED}{BOLD}The result of get_coords must be a tuple, not a Vec!{END}")
    else:
        unimplemented += 1
        print("get_coords is not implemented yet!\n")

    if hasattr(model.Vec, "__repr__"):
        u1 = Vec(0.123, 4.456)
        def repr_produces_valid_tuple(user_string, gold_tuple):
          # rather convoluted way to ignore whitespace but ¯\_(ツ)_/¯
          try:
            user_tuple = ast.literal_eval(user_string)
            return user_tuple == gold_tuple
          except:
            return False
        ## NB. we test model.Vec.__repr__ here.
        ## NOT the overwritten one. 
        test(model.Vec.__repr__, u1, (0.123,4.456), eq=repr_produces_valid_tuple)
    else:
        unimplemented += 1
        print("__repr__ is not implemented yet!\n")

    if hasattr(Vec, "__add__"):
        u1 = Vec(0.123, 4.456)
        u2 = Vec(0.654, -2.09)
        test(Vec.__add__, (u1,u2), Vec(0.777,2.3660000000000005))
    else:
        unimplemented += 1
        print("__add__ is not implemented yet!\n")

    if hasattr(Vec, "__sub__"):
        u1 = Vec(0.123, 4.456)
        u2 = Vec(0.654, -2.09)
        test(Vec.__sub__, (u1,u2), Vec(-0.531,6.546))
    else:
        unimplemented += 1
        print("__sub__ is not implemented yet!\n")
        
    if hasattr(Vec, "__rmul__"):
        u1 = Vec(0.123, 4.456)
        test(Vec.__rmul__, (u1,1.23), Vec(0.15129,5.480880000000001))
    else:
        unimplemented += 1
        print("__rmul__ is not implemented yet!\n")

    if hasattr(Vec, "norm"):
        u1 = Vec(0.123, 4.456)
        test(Vec.norm, u1, 4.457697275499987)
    else:
        unimplemented += 1
        print("norm is not implemented yet!\n")

    ##########################################################

    if not hasattr(model, "Particle"):
        print_statistics()
        print()
        print("class Particle is not implemented yet!\n")
        return []

    test_class_basics( \
        cls=model.Particle, num_args=4, \
        attr_names=["mass", "position", "velocity", "radius"], \
        typecorrect_args=(1, Vec(7, 10), Vec(1,1), 1))
    
    # If basic tests failed, don't go further
    if fail_tests:
        print_statistics("the Particle class")
        return []

    # If we got up to this point, the students' Particle has the expected attributes.
    # We can run further tests.
    class Particle(model.Particle):
      """Extend the user's Particle class with
         - custom equality
         - custom prettyprinter
         - helper method new_particle_with, which creates a modified copy"""
      def __eq__(self, other, epsilon=1e-9):
        if hasattr(self, "charge") and hasattr(other, "charge"):
            charge_eq = self.charge == other.charge
        else:
            charge_eq = True
        
        return \
          math.isclose(self.mass, other.mass, rel_tol=epsilon) and \
          Vec.__eq__(self.position, other.position, epsilon) and \
          Vec.__eq__(self.velocity, other.velocity, epsilon) and \
          math.isclose(self.radius, other.radius, rel_tol=epsilon) and \
          charge_eq
        
      def __repr__(self):
        return ", ".join(f"{k}: {v}" for k,v in self.__dict__.items())
      
      def new_particle_with(self, dict):
        new_particle = Particle(self.mass, self.position, self.velocity, self.radius)
        if hasattr(self, "set_charge"):
            new_particle.set_charge(self.charge)
        new_particle.__dict__.update(dict)
        return new_particle

    p = Particle(1, Vec(7, 10), Vec(1,1), 1)

    ## Methods
    fname = "bounding_box"
    if fun := getattr(Particle, fname, None):
        acceptable_corners = [Vec(6,9), Vec(8,11), Vec(6,11), Vec(8,9)]
        found_among = lambda xs, ys: all(x in ys for x in xs)
        test(fun, p, acceptable_corners, eq=found_among)

    else:
        unimplemented += 1
        print(f"Particle.{fname} is not implemented yet!\n")

    fname = "inertial_move"
    if fun := getattr(Particle, fname, None):
        dt = 42
        gold = p.new_particle_with({'position': Vec(49, 52)})
        p.inertial_move(dt)
        try:
            assert p == gold
        except AssertionError:
            print(f"Particle.{fname}: {diff(gold, p)}")
            fail_tests += 1
        else:
            pass_tests += 1
        dunder_issues = test_and_print_issues_with_dunder_methods(fun, f"Particle.{fname}") 
        if dunder_issues:
            fail_tests += 1
            print_statistics(f"the method Particle.{fname}")
            return []
    else:
        unimplemented += 1
        print(f"Particle.{fname} is not implemented yet!\n")

    particles = [Particle(1, Vec(-5,0), Vec(0,0),0.1),
                 Particle(1.1, Vec(5,0), Vec(0,0),0.1),
                 Particle(1.3, Vec(0,5), Vec(0,0),0.1)]
    
    fname = "to_canvas_coords"
    if fun := getattr(view, fname, None):
        standard_canvas = tk.Canvas(tk.Tk(), width=800, height=600)
        f = lambda u : fun(standard_canvas, u)
        # winfo_req{height,width} gives +6, +4 or +2 to the originally defined dimensions
        # accepting both approaches: keep as is, or subtract 6, 4 or 2
        expected = [Vec(403,303), Vec(402,302), Vec(401,301), Vec(400,300)]
        elem = lambda x, xs: x in xs
        test(f, Vec(0,0), expected, eq=elem, fname="to_canvas_coords(canvas,")

        expected = [Vec(706,151.5), Vec(704,151), Vec(702.0,150.5), Vec(700, 150)]
        test(f, Vec(10,5), expected, eq=elem, fname="to_canvas_coords(canvas,")


    fname = "apply_force"
    if fun := getattr(Particle, fname, None):
        dt = 0.1
        gold = p.new_particle_with({'velocity': Vec(1.5, 1.6)})
        try:
            p.apply_force(dt, Vec(5,6))
        except Exception as e:
            if "unsupported operand type(s) for /" in str(e):
                print(f"Error in Particle.{fname}. You probably wrote something like:")
                print(f"    {RED}a = f / self.mass{END}")
                print("The Vec class doesn't implement division by scalar, only multiplication.")
                print(f"So you need to multiply the force vector by the reciprocal of the particle's mass: {BOLD}1/self.mass{END}.")
                print("(Also remember the order: scalar * vector.)")
            else:
                print(f"Particle.{fname} causes a runtime exception:")
                print(f"{RED}{e}{END}")
                print("Halting the tests.")
            fail_tests += 1
            print_statistics(f"the method Particle.{fname}")
            return []
        try:
            assert p == gold
        except AssertionError:
            print(f"Particle.{fname}: {diff(gold, p)}")
            fail_tests += 1
        else:
            pass_tests += 1

        dunder_issues = test_and_print_issues_with_dunder_methods(fun, f"Particle.{fname}") 
        if dunder_issues:
            fail_tests += 1
            print_statistics(f"the method Particle.{fname}")
            return []
    else:
        unimplemented += 1
        print(f"Particle.{fname} is not implemented yet!\n")


    ####################################################
    # Test the optional attributes.
    # test_count is incremented if a feature is present.
    
    # Helper functions
    is_about_n = lambda n,p,q: Particle.__eq__(p, q, float(f"1e-{n}"))
    is_about = lambda p, q: is_about_n(5, p, q)
    new_particles_with = lambda dict, ps: [p.new_particle_with(dict) for p in ps]
    with_velocities = lambda vs, ps: [p.new_particle_with({'velocity': v}) for p,v in zip(ps, vs)]
    with_positions = lambda pos, ps: [p.new_particle_with({'position': c}) for p,c in zip(ps, pos)]
    with_charges = lambda cs, ps: [p.new_particle_with({'charge': c}) for p,c in zip(ps, cs)]
    def reset(ps):
      ps = new_particles_with({'velocity': Vec(0,0)}, ps)      # reset velocity
      ps = with_positions([Vec(-5,0), Vec(5,0), Vec(0,5)], ps) # reset position
      return ps
                    

    implemented_features = []

    fname = "constant_gravitational_field"
    if fun := getattr(model, fname, None):
        positions = [Vec(-5.0,-0.0005499999999999999), Vec(5.0,-0.0005499999999999999), Vec(0.0,4.99945)]
        expected = with_positions(positions, \
                    new_particles_with({'velocity': Vec(0.0,-0.09999999999999999)}, \
                      particles))
        for _ in range(10):
            fun(0.001, particles, 10)
            [p.inertial_move(0.001) for p in particles]
        test_particles(fname, particles, expected, eq=is_about)
        implemented_features.append(fname)
        dunder_issues = test_and_print_issues_with_dunder_methods(fun, fname) 
        if dunder_issues:
            fail_tests += 1
            # Not halting here even when tests fail: features don't depend on each other.

    fname = "gravitational_force"
    if fun := getattr(model, fname, None):
        particles = reset(particles)
        new_vels = [Vec(0.44077,0.27577), Vec(-0.42577,0.27577), Vec(0.021213,-0.445477)]
        expected = with_velocities(new_vels, particles)
        fun(0.1, particles, 150)
        test_particles(fname, particles, expected, eq=is_about)
        implemented_features.append(fname)

    fname = "wall_force"
    if fun := getattr(model, fname, None):
        particles = reset(particles)
        new_vels = [Vec(1,0), Vec(-0.90909,0), Vec(0,-0.76923)]
        expected = with_velocities(new_vels, particles)
        fun(0.1, particles, k=10, n=Vec(1, 0), a=Vec(-4,0))
        fun(0.1, particles, k=10, n=Vec(-1, 0), a=Vec(4,0))
        fun(0.1, particles, k=10, n=Vec(0, -1), a=Vec(0,4))
        test_particles(fname, particles, expected, eq=is_about)
        implemented_features.append(fname)

    fname = "collision"
    if fun := getattr(model, fname, None):
        particles = new_particles_with({'radius': 3.55, 'velocity': Vec(0,0)}, reset(particles))
        new_vels = [Vec(-0.10229,-0.10229), Vec(0.0929915,-0.0929915), Vec(0,0.15737)]
        expected = with_velocities(new_vels, particles)
        for _ in range(5):
            fun(0.1, particles, k=10)
        test_particles(fname, particles, expected, eq=is_about)
        implemented_features.append(fname)

    fname = "vanderwaals_force"
    if fun := getattr(model, fname, None):
        particles = new_particles_with({'radius': 1, 'velocity': Vec(0,0)}, reset(particles))
        new_vels = [Vec(0.0201184,0.011785), Vec(-0.0182894,0.0107137), Vec(0,-0.0181309)]
        expected = with_velocities(new_vels, particles)
        fun(0.1, particles, A=100)
        test_particles(fname, particles, expected, eq=is_about)
        implemented_features.append(fname)

    fname = "circular_arena"
    if fun := getattr(model, fname, None):
        particles = reset(particles)
        new_vels = [Vec(5,0), Vec(-4.545454,0), Vec(0,-3.8461538)]
        expected = with_velocities(new_vels, particles)
        fun(0.1, particles, k=50, R=4)
        test_particles(fname, particles, expected, eq=is_about)
        implemented_features.append(fname)

      
    # To implement these functions, Particle should have charge
    electro_funs = ["electromagnetic_field", "coulomb_force"]
    if hasattr(Particle, "set_charge"):

        fname = "coulomb_force"
        if fun := getattr(model, fname, None):
            particles = with_charges([-0.5, 0.5, 1], reset(particles))
            new_vels = [Vec(0.09571,0.07071), Vec(0.041555,-0.0642824), Vec(-0.108786,0.0)]
            expected = with_velocities(new_vels, particles)
            fun(0.01, particles, k=1000)
            test_particles(fname, particles, expected, eq=is_about)
            implemented_features.append(fname)

        fname = "electromagnetic_field"
        if fun := getattr(model, fname, None):
            particles = with_charges([-0.5, 0.5, 1], reset(particles))
            initial_vels = [Vec(0.1,-1), Vec(1,-1), Vec(0.5,1)]
            particles = with_velocities(initial_vels, particles)
            new_vels_neg_x = [Vec(0.1005,-0.999), Vec(0.9994,-1.0006), Vec(0.5008,1.0004)]
            new_vels_neg_y = [Vec(0.0995,-1.0001), Vec(1.0006,-0.9994), Vec(0.4991,0.9996)]
            expected = zip(\
                  with_velocities(new_vels_neg_x, particles),
                  with_velocities(new_vels_neg_y, particles))

                    
            fun(0.01, particles, B=10, mu=0.01)
            
            def similar_exists(user, golds):
                is_about_3 = lambda p, q: is_about_n(3,p,q)
                return any(is_about_3(user, gold) for gold in golds)
            
            test_particles(fname, particles, expected, eq=similar_exists)

            for _ in range(1000):
                timestep = 0.0001
                p = particles[0].new_particle_with({'position': Vec(0,5)})
                fun(timestep, [p], B=10, mu=0.1)
                p.inertial_move(timestep)

            new_pos_neg_x = Vec(1.005e-5,4.9999)
            new_pos_neg_y = Vec(9.9447e-6,4.9999)
            expected = [\
                  p.new_particle_with({"position": new_pos_neg_x}),
                  p.new_particle_with({"position": new_pos_neg_y})]

            test_particles(fname, [p], [expected], eq=similar_exists)

            implemented_features.append(fname)

    elif any(hasattr(model, electro_fun) for electro_fun in electro_funs):
        unimplemented += 1
        print("-------------------------------------------------------")
        print(" To implement Coulomb force and electromagnetic field,")
        print(" the Particle class needs:   (1) attribute 'charge'")
        print("                             (2) method 'set_charge'")
        print(" Make sure that the names are an exact match.")
        print("-------------------------------------------------------")

    print_statistics()
    return implemented_features

def run():
    model, view = _load_modules()
    return _run_tests(model, view)

if __name__ == "__main__":
    implemented_features = run()

    if implemented_features:
        print("Implemented features:")
        for feature in implemented_features:
            print(f"- {feature}")
    
