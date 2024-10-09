from abaqus import *
from abaqusConstants import *
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
Mdb()

class JobParams:
    """
    Structure contenant la disponibilité des resources de calcul
    """
    def __init__(self, num_cores, active_memory_pct):
        self.cores = num_cores
        self.ram = active_memory_pct

def prepare_models(job_params, mesh_sizes):
    """
    @param number_iterations le nombre de modèles à préparer dans cette paramétrisation

    Crée des cylindres de béton avec ...
    """
    for i in range(len(mesh_sizes)):

        model = "Model - " + str(1 + i)
        job_name = "MeshSensitivityStudy-" + str(1 + i)
        #Create model
        mdb.Model(name=model, modelType=STANDARD_EXPLICIT)
        #: The model "model" has been created.
        currentModel = mdb.models[model]
        a = currentModel.rootAssembly
        currentViewport = session.viewports['Viewport: 1']

        currentViewport.setValues(displayedObject=a)
        #session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Initial')

        #Create part
        currentViewport.partDisplay.setValues(sectionAssignments=OFF, engineeringFeatures=OFF)
        currentViewport.partDisplay.geometryOptions.setValues(referenceRepresentation=ON)
        s = currentModel.ConstrainedSketch(name='__profile__', sheetSize=200.0)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=STANDALONE)
        s.CircleByCenterPerimeter(center=(0.0, 1.25), point1=(-22.5, 18.75))
        s.RadialDimension(curve=g[2], textPoint=(-35.4598770141602, 16.889289855957), radius=75.0)
        p = currentModel.Part(name='Part-1', dimensionality=THREE_D, type=DEFORMABLE_BODY)
        p = currentModel.parts['Part-1']
        p.BaseSolidExtrude(sketch=s, depth=300.0)
        s.unsetPrimaryObject()
        p = currentModel.parts['Part-1']
        currentViewport.setValues(displayedObject=p)
        del currentModel.sketches['__profile__']

        #Create material
        currentViewport.partDisplay.setValues(sectionAssignments=ON, engineeringFeatures=ON)
        currentViewport.partDisplay.geometryOptions.setValues(referenceRepresentation=OFF)
        currentModel.Material(name='Concrete B20')
        currentModel.materials['Concrete B20'].Elastic(table=((21200.0, 0.2), ))
        currentModel.materials['Concrete B20'].ConcreteDamagedPlasticity(table=((31.0, 0.1, 1.16, 0.67, 0.0), ))
        currentModel.materials['Concrete B20'].concreteDamagedPlasticity.ConcreteCompressionHardening(table=((10.2, 0.0), (12.8, 7.73585e-05), (15.0, 0.000173585), (16.8, 0.000288679), (18.2, 0.000422642), (19.2, 0.000575472), (19.8, 0.00074717), (20.0, 0.000937736), (19.8, 0.00114717), (19.2, 0.001375472), (18.2, 0.001622642), (16.8, 0.001888679), (15.0, 0.002173585), (12.8, 0.002477358), (10.2, 0.0028), (7.2, 0.003141509), (3.8, 0.003501887)))
        currentModel.materials['Concrete B20'].concreteDamagedPlasticity.ConcreteTensionStiffening(table=((2.0, 0.0), (0.02, 0.000943396)))
        currentModel.materials['Concrete B20'].concreteDamagedPlasticity.ConcreteCompressionDamage(table=((0.0, 0.0), (0.0, 7.73585e-05), (0.0, 0.000173585), (0.0, 0.000288679), (0.0, 0.000422642), (0.0, 0.000575472), (0.0, 0.00074717), (0.0, 0.000937736), (0.01, 0.00114717), (0.04, 0.001375472), (0.09, 0.001622642), (0.16, 0.001888679), (0.25, 0.002173585), (0.36, 0.002477358), (0.49, 0.0028), (0.64, 0.003141509), (0.81, 0.003501887)))
        currentModel.materials['Concrete B20'].concreteDamagedPlasticity.ConcreteTensionDamage(table=((0.0, 0.0), (0.99, 0.000943396)))

        #Create section
        currentModel.HomogeneousSolidSection(name='Section-1', material='Concrete B20', thickness=None)

        #Assign section to part
        p = currentModel.parts['Part-1']
        c = p.cells
        cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
        region = regionToolset.Region(cells=cells)
        # p = currentModel.parts['Part-1']
        p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, 
            offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)

        #Import part inside the assembly
        a = currentModel.rootAssembly
        currentViewport.setValues(displayedObject=a)
        a1 = currentModel.rootAssembly
        a1.DatumCsysByDefault(CARTESIAN)
        # p = currentModel.parts['Part-1']
        a1.Instance(name='Part-1-1', part=p, dependent=ON)

        #Create step
        currentViewport.assemblyDisplay.setValues(adaptiveMeshConstraints=ON)
        currentModel.StaticStep(name='Step-1', previous='Initial', maxNumInc=1000, initialInc=0.01, maxInc=0.01, nlgeom=ON)
        currentViewport.assemblyDisplay.setValues(step='Step-1')

        #Set field output variables
        currentModel.fieldOutputRequests['F-Output-1'].setValues(
            variables=('S', 'PE', 'PEEQ', 'PEMAG', 'LE', 'U', 'RF', 'CF', 'CSTRESS', 
            'CDISP', 'DAMAGEC', 'DAMAGET'))

        #Boundary conditions
        currentViewport.assemblyDisplay.setValues(loads=ON, bcs=ON, 
            predefinedFields=ON, connectors=ON, adaptiveMeshConstraints=OFF)
        # currentViewport.view.setValues(nearPlane=554.747, 
        #     farPlane=997.733, width=321.182, height=225.75, cameraPosition=(225.216, 
        #     446.867, -444.372), cameraUpVector=(-0.284549, 0.57735, 0.76531))
        a = currentModel.rootAssembly
        f1 = a.instances['Part-1-1'].faces
        faces1 = f1.getSequenceFromMask(mask=('[#4 ]', ), )
        region = regionToolset.Region(faces=faces1)
        currentModel.DisplacementBC(name='Support', 
            createStepName='Step-1', region=region, u1=UNSET, u2=UNSET, u3=0.0, 
            ur1=UNSET, ur2=UNSET, ur3=UNSET, amplitude=UNSET, fixed=OFF, 
            distributionType=UNIFORM, fieldName='', localCsys=None)
        # currentViewport.view.setValues(nearPlane=567.549, 
        #     farPlane=986.956, width=328.594, height=230.96, cameraPosition=(478.28, 
        #     446.867, 570.499), cameraUpVector=(-0.610561, 0.57735, -0.54211), 
        #     cameraTarget=(-5.04425, -10.1677, 141.362))
        a = currentModel.rootAssembly
        f1 = a.instances['Part-1-1'].faces
        faces1 = f1.getSequenceFromMask(mask=('[#2 ]', ), )
        region = regionToolset.Region(faces=faces1)
        
        #
        # Displacement constraint as variable
        #
        currentModel.DisplacementBC(name='Displacement', 
            createStepName='Step-1', region=region, u1=UNSET, u2=UNSET, u3=-1.5, 
            ur1=UNSET, ur2=UNSET, ur3=UNSET, amplitude=UNSET, fixed=OFF, 
            distributionType=UNIFORM, fieldName='', localCsys=None)

        #Meshing
        currentViewport.assemblyDisplay.setValues(mesh=ON, loads=OFF, 
            bcs=OFF, predefinedFields=OFF, connectors=OFF)
        currentViewport.assemblyDisplay.meshOptions.setValues(meshTechnique=ON)
        p = currentModel.parts['Part-1']
        currentViewport.setValues(displayedObject=p)
        currentViewport.partDisplay.setValues(sectionAssignments=OFF, 
            engineeringFeatures=OFF, mesh=ON)
        currentViewport.partDisplay.meshOptions.setValues(meshTechnique=ON)
        
        # 
        #  Which element types?
        #
        elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=STANDARD, 
            kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF, 
            hourglassControl=DEFAULT, distortionControl=DEFAULT)
        elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=STANDARD)
        elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=STANDARD)
        p = currentModel.parts['Part-1']
        c = p.cells
        cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
        pickedRegions =(cells, )
        p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
            elemType3))
        p = currentModel.parts['Part-1']

        p.seedPart(size=mesh_sizes[i], deviationFactor=0.1, minSizeFactor=0.1)
        p = currentModel.parts['Part-1']
        p.generateMesh()

        #Create Job
        a1 = currentModel.rootAssembly
        a1.regenerate()
        a = currentModel.rootAssembly
        currentViewport.setValues(displayedObject=a)
        currentViewport.assemblyDisplay.setValues(mesh=OFF)
        currentViewport.assemblyDisplay.meshOptions.setValues(meshTechnique=OFF)        
        mdb.Job(name=job_name, model=model, description='', 
            type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, 
            memory=job_params.ram, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
            explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
            modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
            scratch='', resultsFormat=ODB, numThreadsPerMpiProcess=1, 
            multiprocessingMode=DEFAULT, numCpus=job_params.cores, numGPUs=0)
        
    mdb.saveAs(pathName='F:/Haitam Work/Gilbert/CDPM/ABAQUS Concrete Cylinders Parametric Study/Parametric study.cae')


#
# Parametrization
#

mesh_sizes = []
for i in range(5):
    mesh_sizes += 20 * (i + 1)

# Combien de processeurssont à ta dispo?
job = JobParams(num_cores=4, active_memory_pct=90)

prepare_models(mesh_sizes=mesh_sizes, job_params=job)