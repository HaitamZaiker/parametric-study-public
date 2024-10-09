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

# """
# class test:
#     PI = 3.14
#     E = 20000

#     def __init__(self, E, PI):
#         self.E = E
#         self.PI = PI

# t = test(2, 5)
# """

def calc_young_modulus(fcPrime):
    """
    @param fcPrime f'c force en compression du béton

    Cette fonction réfère à la norme CSA A23.3 pour déterminer la modulus de Young du béton.
    """
    return 4500 * (fcPrime ** 0.5)

class concrete:
    # Poisson = 0.2
    # Name = "B20"
    # DilationAngle = 31
    # Eccentricity = 0.1
    # fb0_fc0 = 1.16
    # K = 0.67
    # ViscosityParameter = 0
    # fcPrime = 20

    def __init__(self, fcPrime=20, Name='B20', DilationAngle=31, Eccentricity=0.1, fb0_fc0=1.16, K=0.67, ViscosityParameter=0, Poisson=0.20):
        self.fcPrime = fcPrime
        self.E = calc_young_modulus(fcPrime)
        self.Name = Name
        self.DilationAngle = DilationAngle
        self.Eccentricity = Eccentricity
        self.fb0_fc0 = fb0_fc0
        self.K = K
        self.ViscosityParameter = ViscosityParameter
        self.Poisson = Poisson

B20 = concrete(20, "B20")
B30 = concrete(30, "B30")
B40 = concrete(40, "B40")
B50 = concrete(50, "B50")

#Functions
def beton_hognestad(epsilon0 , fc_prime, increments, elastic_limit=0.40, crushing_limit=0.0038):
    """
    @param epsilon0
    @param fc_prime f'c force en compression
    @param increments nombre de points requis sur la courbe

    Détermine la relation contrainte-déformation selon le modèle de Hognestad.
    """
    youngs_modulus = calc_young_modulus(fc_prime)
    CPH = []
    CCD = []
    for i in range (0, increments + 1):        
        epsilon = elastic_limit * fc_prime / youngs_modulus + epsilon0 / increments * i
        fc = fc_prime * (2 * epsilon / epsilon0 - ((epsilon/epsilon0) ** 2))
        CCD.append((0 , epsilon - fc / youngs_modulus))
        CPH.append((epsilon - fc / youngs_modulus , fc))
    CPH.append((crushing_limit - fc_prime * 0.85 / youngs_modulus, fc_prime * 0.85))
    CCD.append((1 - fc_prime * 0.85 / fc_prime, crushing_limit - fc_prime * 0.85 / youngs_modulus))
    return CPH , CCD

# Vecchio-Collins
def beton_tension(epsilont_max, fc_prime, increments):
    """

    """
    E = calc_young_modulus(fc_prime)
    ft_prime = 0.6 * (fc_prime ** 0.5)
    epsiloncrtc = ft_prime/E
    CTS = []
    CTD = []
    for i in range (0, increments + 1):
        epsilont = epsiloncrtc + epsilont_max/increments*i
        fct = ft_prime / (1 + (200 * epsilont) ** 0.5)
        CTS.append((epsilont - fct/E, fct))
        CTD.append((1-fct/ft_prime, epsilont - fct/E))
    return CTS , CTD


#Part Section
currentViewport = session.viewports['Viewport: 1']
currentViewport.partDisplay.setValues(sectionAssignments=OFF, engineeringFeatures=OFF)
currentViewport.partDisplay.geometryOptions.setValues(referenceRepresentation=ON)
currentModel = mdb.models['Model-1']
s1 = currentModel.ConstrainedSketch(name='__profile__', sheetSize=200.0)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=STANDALONE)
s1.rectangle(point1=(0.0, 0.0), point2=(35.0, 15.0))
p = currentModel.Part(name='Part-1', dimensionality=THREE_D, type=DEFORMABLE_BODY)
# p = mdb.models['Model-1'].parts['Part-1']
p.BaseSolidExtrude(sketch=s1, depth=20.0)
s1.unsetPrimaryObject()
# p = mdb.models['Model-1'].parts['Part-1']
currentViewport.setValues(displayedObject=p)
del currentModel.sketches['__profile__']

#Material Description
currentViewport.partDisplay.setValues(sectionAssignments=ON, engineeringFeatures=ON)
currentViewport.partDisplay.geometryOptions.setValues(referenceRepresentation=OFF)
material_b20 = currentModel.Material(name='Concrete B20')
material_b20.Elastic(table=((21200.0, 0.2), ))
material_b20.ConcreteDamagedPlasticity(table=((31.0, 0.1, 1.16, 0.67, 0.0), ))
material_b20.concreteDamagedPlasticity.ConcreteCompressionHardening(table=((10.2, 0.0), (12.8, 7.73585e-05), (15.0, 0.000173585), 
                                                                           (16.8, 0.000288679), (18.2, 0.000422642), (19.2, 0.000575472), (19.8, 0.00074717), (20.0, 0.000937736), (19.8, 0.00114717), (19.2, 0.001375472), (18.2, 0.001622642), (16.8, 0.001888679), (15.0, 0.002173585), (12.8, 0.002477358), (10.2, 0.0028), (7.2, 0.003141509), (3.8, 0.003501887)))
material_b20.concreteDamagedPlasticity.ConcreteTensionStiffening(table=((2.0, 0.0), (0.02, 0.000943396)))
material_b20.concreteDamagedPlasticity.ConcreteCompressionDamage(table=((0.0, 0.0), (0.0, 7.73585e-05), (0.0, 0.000173585), 
                                                                        (0.0, 0.000288679), (0.0, 0.000422642), (0.0, 0.000575472), (0.0, 0.00074717), (0.0, 0.000937736), (0.01, 0.00114717), (0.04, 0.001375472), (0.09, 0.001622642), (0.16, 0.001888679), (0.25, 0.002173585), (0.36, 0.002477358), (0.49, 0.0028), (0.64, 0.003141509), (0.81, 0.003501887)))
material_b20.concreteDamagedPlasticity.ConcreteTensionDamage(table=((0.0, 0.0), (0.99, 0.000943396)))



#def material(E, Poisson, DilationAngle, Eccentricity, fb0_fc0, K, ViscosityParameter):
#New Material Description
CPH, CCD = beton_hognestad(0.02, B20.fcPrime, 20)
CTS, CTD = beton_tension(0.05, B20.fcPrime, 20)
material_b20 = currentModel.Material(name=B20.Name)
material_b20.Elastic(table=((B20.E, B20.Poisson), ))
material_b20.ConcreteDamagedPlasticity(table=((B20.DilationAngle, B20.Eccentricity, B20.fb0_fc0, B20.K, B20.ViscosityParameter), ))
material_b20.concreteDamagedPlasticity.ConcreteCompressionHardening(table=tuple(CPH))
material_b20.concreteDamagedPlasticity.ConcreteTensionStiffening(table=tuple(CTS))
material_b20.concreteDamagedPlasticity.ConcreteCompressionDamage(table=tuple(CCD))
material_b20.concreteDamagedPlasticity.ConcreteTensionDamage(table=tuple(CTD))    

#Section Creation
currentModel.HomogeneousSolidSection(name='Section-1', material='Concrete B20', thickness=None)

#Section assignment
p = currentModel.parts['Part-1']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
region = regionToolset.Region(cells=cells)
# p = mdb.models['Model-1'].parts['Part-1']
p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)

#Step creation
a = currentModel.rootAssembly
currentViewport.setValues(displayedObject=a)
currentViewport.assemblyDisplay.setValues(adaptiveMeshConstraints=ON, optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
currentModel.StaticStep(name='Step-1', previous='Initial', minInc=1e-10, nlgeom=ON)
currentViewport.assemblyDisplay.setValues(step='Step-1')

