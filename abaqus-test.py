# def materiel_elastic(E , poisson, Nom):
"""
E: float
poisson: float
Nom: str
"""
    # mdb.models['Model-1'].Material(name=Nom)
    # mdb.models['Model-1'].materials[Nom].Elastic(table=((E, poisson), ))

# materiel_elastic(200000, 0.4, 'steel')

# for i in range(0, 20, 1):
    # E = 200000 + 10000*i
    # materiel_elastic(E, 0.4, 'steel-'+str(E))

class concrete:
    Poisson = 0.2
    Name = "B20"
    DilationAngle = 31
    Eccentricity = 0.1
    fb0_fc0 = 1.16
    K = 0.67
    ViscosityParameter = 0
    fcPrime = 20

    def __init__(self, E, Poisson, Name, DilationAngle, Eccentricity, fb0_fc0, K, ViscosityParameter, fcPrime):
        self.E = E
        self.Poisson = Poisson
        self.Name = Name
        self.DilationAngle = DilationAngle
        self.Eccentricity = Eccentricity
        self.fb0_fc0 = fb0_fc0
        self.K = K
        self.ViscosityParameter = ViscosityParameter

B20 = concrete(0, 0, 0, 0, 0, 0, 0, 0, 0)
B30 = concrete(0, 0, 0, 0, 0, 0, 0, 0, 0)
B40 = concrete(0, 0, 0, 0, 0, 0, 0, 0, 0)
B50 = concrete(0, 0, 0, 0, 0, 0, 0, 0, 0)
"""
class test:
    PI = 3.14
    E = 20000

    def __init__(self, E, PI):
        self.E = E
        self.PI = PI

t = test(2, 5)
"""




#Functions
def beton_hognestad(epsilon0 , fc_prime, increments):
    E = 4500*(fc_prime)**(1/2)
    CPH = []
    CCD = []
    for i in range (0, increments + 1):
        #use variables
        epsilon = 0.4*fc_prime/E + epsilon0/increments*i
        fc = fc_prime*(2*epsilon/epsilon0-(epsilon/epsilon0)**2)
        CCD.append((0 , epsilon - fc/E))
        CPH.append((epsilon - fc/E , fc))
    CPH.append((0.0038 - fc_prime*0.85/E , fc_prime*0.85))
    CCD.append((1-fc_prime*0.85/fc_prime , 0.0038 - fc_prime*0.85/E))
    return CPH , CCD

def beton_tension(epsilontMax, fc_prime, increments):
    E = 4500*(fc_prime)**(1/2)
    ft_prime = 0.6*(fc_prime)**(1/2)
    epsiloncrtc = ft_prime/E
    CTS = []
    CTD = []
    for i in range (0, increments + 1):
        epsilont = epsiloncrtc + epsilontMax/increments*i
        fct = ft_prime/(1+(200*epsilont)**(1/2))
        CTS.append((epsilont - fct/E, fct))
        CTD.append((1-fct/ft_prime, epsilont - fct/E))
    return CTS , CTD


#Part Section
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, engineeringFeatures=OFF)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(referenceRepresentation=ON)
s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=STANDALONE)
s1.rectangle(point1=(0.0, 0.0), point2=(35.0, 15.0))
p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['Part-1']
p.BaseSolidExtrude(sketch=s1, depth=20.0)
s1.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Part-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']

#Material Description
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, engineeringFeatures=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(referenceRepresentation=OFF)
mdb.models['Model-1'].Material(name='Concrete B20')
mdb.models['Model-1'].materials['Concrete B20'].Elastic(table=((21200.0, 0.2), ))
mdb.models['Model-1'].materials['Concrete B20'].ConcreteDamagedPlasticity(table=((31.0, 0.1, 1.16, 0.67, 0.0), ))
mdb.models['Model-1'].materials['Concrete B20'].concreteDamagedPlasticity.ConcreteCompressionHardening(table=((10.2, 0.0), (12.8, 7.73585e-05), (15.0, 0.000173585), (16.8, 0.000288679), (18.2, 0.000422642), (19.2, 0.000575472), (19.8, 0.00074717), (20.0, 0.000937736), (19.8, 0.00114717), (19.2, 0.001375472), (18.2, 0.001622642), (16.8, 0.001888679), (15.0, 0.002173585), (12.8, 0.002477358), (10.2, 0.0028), (7.2, 0.003141509), (3.8, 0.003501887)))
mdb.models['Model-1'].materials['Concrete B20'].concreteDamagedPlasticity.ConcreteTensionStiffening(table=((2.0, 0.0), (0.02, 0.000943396)))
mdb.models['Model-1'].materials['Concrete B20'].concreteDamagedPlasticity.ConcreteCompressionDamage(table=((0.0, 0.0), (0.0, 7.73585e-05), (0.0, 0.000173585), (0.0, 0.000288679), (0.0, 0.000422642), (0.0, 0.000575472), (0.0, 0.00074717), (0.0, 0.000937736), (0.01, 0.00114717), (0.04, 0.001375472), (0.09, 0.001622642), (0.16, 0.001888679), (0.25, 0.002173585), (0.36, 0.002477358), (0.49, 0.0028), (0.64, 0.003141509), (0.81, 0.003501887)))
mdb.models['Model-1'].materials['Concrete B20'].concreteDamagedPlasticity.ConcreteTensionDamage(table=((0.0, 0.0), (0.99, 0.000943396)))



#def material(E, Poisson, DilationAngle, Eccentricity, fb0_fc0, K, ViscosityParameter):
#New Material Description
CPH, CCD = beton_hognestad(0.02, B20.fcPrime, 20)
CTS, CTD = beton_tension(0.05, B20.fcPrime, 20)
mdb.models['Model-1'].Material(name=B20.Name)
mdb.models['Model-1'].materials[B20.Name].Elastic(table=((B20.E, B20.Poisson), ))
mdb.models['Model-1'].materials[B20.Name].ConcreteDamagedPlasticity(table=((B20.DilationAngle, B20.Eccentricity, B20.fb0_fc0, B20.K, B20.ViscosityParameter), ))
mdb.models['Model-1'].materials[B20.Name].concreteDamagedPlasticity.ConcreteCompressionHardening(table=tuple(CPH))
mdb.models['Model-1'].materials[B20.Name].concreteDamagedPlasticity.ConcreteTensionStiffening(table=tuple(CTS))
mdb.models['Model-1'].materials[B20.Name].concreteDamagedPlasticity.ConcreteCompressionDamage(table=tuple(CCD))
mdb.models['Model-1'].materials[B20.Name].concreteDamagedPlasticity.ConcreteTensionDamage(table=tuple(CTD))    

#Section Creation
mdb.models['Model-1'].HomogeneousSolidSection(name='Section-1', material='Concrete B20', thickness=None)

#Section assignment
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
region = regionToolset.Region(cells=cells)
p = mdb.models['Model-1'].parts['Part-1']
p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)

#Step creation
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(adaptiveMeshConstraints=ON, optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial', minInc=1e-10, nlgeom=ON)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')

