
import sys
try:
    from ompl import util as ou
    from ompl import base as ob
    from ompl import geometric as og
except ImportError:
    # if the ompl module is not in the PYTHONPATH assume it is installed in a
    # subdirectory of the parent directory called "py-bindings."
    from os.path import abspath, dirname, join
    sys.path.insert(0, join(dirname(dirname(abspath(__file__))), 'py-bindings'))
    from ompl import util as ou
    from ompl import base as ob
    from ompl import geometric as og
from math import sqrt
import argparse

# ## @cond IGNORE
# # Our "collision checker". For this demo, our robot's state space
# # lies in [0,1]x[0,1], with a circular obstacle of radius 0.25
# # centered at (0.5,0.5). Any states lying in this circular region are
# # considered "in collision".
# class ValidityChecker(ob.StateValidityChecker):
#     # Returns whether the given state's position overlaps the
#     # circular obstacle
#     def isValid(self, state):
#         return self.clearance(state) > 0.0

#     # Returns the distance from the given state's position to the
#     # boundary of the circular obstacle.
#     def clearance(self, state):
#         # Extract the robot's (x,y) position from its state
#         x = state[0]
#         y = state[1]

#         # Distance formula between two points, offset by the circle's
#         # radius
#         return sqrt((x-0.5)*(x-0.5) + (y-0.)*(y-0.)) - 0.45


# ## Returns a structure representing the optimization objective to use
# #  for optimal motion planning. This method returns an objective
# #  which attempts to minimize the length in configuration space of
# #  computed paths.
# def getPathLengthObjective(si):
#     return ob.PathLengthOptimizationObjective(si)

# ## Returns an optimization objective which attempts to minimize path
# #  length that is satisfied when a path of length shorter than 1.51
# #  is found.
# def getThresholdPathLengthObj(si):
#     obj = ob.PathLengthOptimizationObjective(si)
#     obj.setCostThreshold(ob.Cost(1.51))
#     return obj

# ## Defines an optimization objective which attempts to steer the
# #  robot away from obstacles. To formulate this objective as a
# #  minimization of path cost, we can define the cost of a path as a
# #  summation of the costs of each of the states along the path, where
# #  each state cost is a function of that state's clearance from
# #  obstacles.
# #
# #  The class StateCostIntegralObjective represents objectives as
# #  summations of state costs, just like we require. All we need to do
# #  then is inherit from that base class and define our specific state
# #  cost function by overriding the stateCost() method.
# #
# class minPathPotentialObjective(ob.OptimizationObjective):
#     def __init__(self, si, start):
#         super(minPathPotentialObjective, self).__init__(si)
#         self.si_ = si
#         self.start_ = start

#     # Our requirement is to maximize path clearance from obstacles,
#     # but we want to represent the objective as a path cost
#     # minimization. Therefore, we set each state's cost to be the
#     # reciprocal of its clearance, so that as state clearance
#     # increases, the state cost decreases.
#     # def stateCost(self, s):
#     #     return ob.Cost(1 / (self.si_.getStateValidityChecker().clearance(s) +
#     #                         sys.float_info.min))

#     def combineCosts(self, c1, c2):
#         return ob.Cost(max(c1.value(), c2.value()))

#     def motionCost(self, s1, s2):
#         return ob.Cost(s2[1] - self.start_[1])
    
    
# ## Return an optimization objective which attempts to steer the robot
# #  away from obstacles.
# def getClearanceObjective(si, start):
#     return minPathPotentialObjective(si, start)

# ## Create an optimization objective which attempts to optimize both
# #  path length and clearance. We do this by defining our individual
# #  objectives, then adding them to a MultiOptimizationObjective
# #  object. This results in an optimization objective where path cost
# #  is equivalent to adding up each of the individual objectives' path
# #  costs.
# #
# #  When adding objectives, we can also optionally specify each
# #  objective's weighting factor to signify how important it is in
# #  optimal planning. If no weight is specified, the weight defaults to
# #  1.0.
# def getBalancedObjective1(si):
#     lengthObj = ob.PathLengthOptimizationObjective(si)
#     clearObj = minPathPotentialObjective(si)

#     opt = ob.MultiOptimizationObjective(si)
#     opt.addObjective(lengthObj, 5.0)
#     opt.addObjective(clearObj, 1.0)

#     return opt

# ## Create an optimization objective equivalent to the one returned by
# #  getBalancedObjective1(), but use an alternate syntax.
# #  THIS DOESN'T WORK YET. THE OPERATORS SOMEHOW AREN'T EXPORTED BY Py++.
# # def getBalancedObjective2(si):
# #     lengthObj = ob.PathLengthOptimizationObjective(si)
# #     clearObj = ClearanceObjective(si)
# #
# #     return 5.0*lengthObj + clearObj


# ## Create an optimization objective for minimizing path length, and
# #  specify a cost-to-go heuristic suitable for this optimal planning
# #  problem.
# def getPathLengthObjWithCostToGo(si):
#     obj = ob.PathLengthOptimizationObjective(si)
#     obj.setCostToGoHeuristic(ob.CostToGoHeuristic(ob.goalRegionCostToGo))
#     return obj


# # Keep these in alphabetical order and all lower case
# def allocatePlanner(si, plannerType):
#     if plannerType.lower() == "bfmtstar":
#         return og.BFMT(si)
#     elif plannerType.lower() == "bitstar":
#         return og.BITstar(si)
#     elif plannerType.lower() == "fmtstar":
#         return og.FMT(si)
#     elif plannerType.lower() == "informedrrtstar":
#         return og.InformedRRTstar(si)
#     elif plannerType.lower() == "prmstar":
#         return og.PRMstar(si)
#     elif plannerType.lower() == "rrtstar":
#         return og.RRTstar(si)
#     elif plannerType.lower() == "sorrtstar":
#         return og.SORRTstar(si)
#     else:
#         ou.OMPL_ERROR("Planner-type is not implemented in allocation function.")


# # Keep these in alphabetical order and all lower case
# def allocateObjective(si, objectiveType, start):
#     if objectiveType.lower() == "pathclearance":
#         return getClearanceObjective(si, start)
#     elif objectiveType.lower() == "pathlength":
#         return getPathLengthObjective(si)
#     elif objectiveType.lower() == "thresholdpathlength":
#         return getThresholdPathLengthObj(si)
#     elif objectiveType.lower() == "weightedlengthandclearancecombo":
#         return getBalancedObjective1(si)
#     else:
#         ou.OMPL_ERROR("Optimization-objective is not implemented in allocation function.")



# def plan(runTime, plannerType, objectiveType, fname):
#     # Construct the robot state space in which we're planning. We're
#     # planning in [0,1]x[0,1], a subset of R^2.
#     space = ob.RealVectorStateSpace(2)

#     # Set the bounds of space to be in [0,1].
#     space.setBounds(0.0, 1.0)

#     # Construct a space information instance for this state space
#     si = ob.SpaceInformation(space)

#     # Set the object used to check which states in the space are valid
#     validityChecker = ValidityChecker(si)
#     si.setStateValidityChecker(validityChecker)

#     si.setup()

#     # Set our robot's starting state to be the bottom-left corner of
#     # the environment, or (0,0).
#     start = ob.State(space)
#     start[0] = 0.0
#     start[1] = 0.0

#     # Set our robot's goal state to be the top-right corner of the
#     # environment, or (1,1).
#     goal = ob.State(space)
#     goal[0] = 1.0
#     goal[1] = 0.0

#     # Create a problem instance
#     pdef = ob.ProblemDefinition(si)

#     # Set the start and goal states
#     pdef.setStartAndGoalStates(start, goal)

#     # Create the optimization objective specified by our command-line argument.
#     # This helper function is simply a switch statement.
#     pdef.setOptimizationObjective(allocateObjective(si, objectiveType, start))

#     # Construct the optimal planner specified by our command line argument.
#     # This helper function is simply a switch statement.
#     optimizingPlanner = allocatePlanner(si, plannerType)

#     # Set the problem instance for our planner to solve
#     optimizingPlanner.setProblemDefinition(pdef)
#     optimizingPlanner.setup()

#     # attempt to solve the planning problem in the given runtime
#     solved = optimizingPlanner.solve(runTime)

#     if solved:
#         # Output the length of the path found
#         print('{0} found solution of path length {1:.4f} with an optimization ' \
#             'objective value of {2:.4f}'.format( \
#             optimizingPlanner.getName(), \
#             pdef.getSolutionPath().length(), \
#             pdef.getSolutionPath().cost(pdef.getOptimizationObjective()).value()))
#         print(pdef.getSolutionPath())

#         # If a filename was specified, output the path as a matrix to
#         # that file for visualization
#         if fname:
#             with open(fname, 'w') as outFile:
#                 outFile.write(pdef.getSolutionPath().printAsMatrix())
#     else:
#         print("No solution found.")

# if __name__ == "__main__":
#     # Create an argument parser
#     parser = argparse.ArgumentParser(description='Optimal motion planning demo program.')

#     # Add a filename argument
#     parser.add_argument('-t', '--runtime', type=float, default=1.0, help=\
#         '(Optional) Specify the runtime in seconds. Defaults to 1 and must be greater than 0.')
#     parser.add_argument('-p', '--planner', default='BITstar', \
#         choices=['BFMTstar', 'BITstar', 'FMTstar', 'InformedRRTstar', 'PRMstar', 'RRTstar', \
#         'SORRTstar'], \
#         help='(Optional) Specify the optimal planner to use, defaults to RRTstar if not given.')
#     parser.add_argument('-o', '--objective', default='PathClearance', \
#         choices=['PathClearance', 'PathLength', 'ThresholdPathLength', \
#         'WeightedLengthAndClearanceCombo'], \
#         help='(Optional) Specify the optimization objective, defaults to PathLength if not given.')
#     parser.add_argument('-f', '--file', default=None, \
#         help='(Optional) Specify an output path for the found solution path.')
#     parser.add_argument('-i', '--info', type=int, default=0, choices=[0, 1, 2], \
#         help='(Optional) Set the OMPL log level. 0 for WARN, 1 for INFO, 2 for DEBUG.' \
#         ' Defaults to WARN.')

#     # Parse the arguments
#     args = parser.parse_args()

#     # Check that time is positive
#     if args.runtime <= 0:
#         raise argparse.ArgumentTypeError(
#             "argument -t/--runtime: invalid choice: %r (choose a positive number greater than 0)" \
#             % (args.runtime,))

#     # Set the log level
#     if args.info == 0:
#         ou.setLogLevel(ou.LOG_WARN)
#     elif args.info == 1:
#         ou.setLogLevel(ou.LOG_INFO)
#     elif args.info == 2:
#         ou.setLogLevel(ou.LOG_DEBUG)
#     else:
#         ou.OMPL_ERROR("Invalid log-level integer.")

#     # Solve the planning problem
#     plan(args.runtime, args.planner, args.objective, args.file)




#########################################################################


# import kinpy as kp
# import math

# chain = kp.build_chain_from_urdf(open("models/articulate_fish.xacro").read())
# print(chain)

# th = {'joint0': math.pi / 4.0, 'joint1': math.pi / 4.0}
# th = {'joint0': 0 / 4.0, 'joint1': 0 / 4.0}
# ret = chain.forward_kinematics(th)
# print(ret)


#########################################################################

import pybullet as p
import time

p.connect(p.GUI)
# p.setGravity(0, 0, -9.8)
p.setTimeStep(1./240.)
# p.setAdditionalSearchPath(pybullet_data.getDataPath())

GRAVITY = -10
p.setRealTimeSimulation(0)
# bowl = p.loadURDF('models/bowl/bowl.urdf', (0,0,0), (0,0,1,1), globalScaling=5)
fish = p.loadURDF('models/fish/fishWithRing.xacro', (1,-2.1,1), (0,1,0,1))

# name_in = 'models/triple_hook/triple_hook.obj'
# name_out = 'models/triple_hook/triple_hook_vhacd.obj'
# name_log = "log.txt"
# p.vhacd(name_in, name_out, name_log)
# ring = p.loadURDF('models/fish/ring2_vhacd.OBJ', (0,0,1), (0,0,1,1))

# p.changeDynamics(bowl, -1, mass=0)

# Upload the mesh data to PyBullet and create a static object
# mesh_scale = [.04, .04, .04]  # The scale of the mesh
# mesh_collision_shape = p.createCollisionShape(
#     shapeType=p.GEOM_MESH,
#     fileName="models/fish/ring2_vhacd.OBJ",
#     meshScale=mesh_scale,
#     # flags=p.GEOM_FORCE_CONCAVE_TRIMESH,
#     # meshData=mesh_data,
# )
# mesh_visual_shape = -1  # Use the same shape for visualization
# mesh_position = [0.3, 0, 2]  # The position of the mesh
# mesh_orientation = p.getQuaternionFromEuler([.6, 1.57, 0])  # The orientation of the mesh
# ring = p.createMultiBody(
#     baseMass=1.,
#     baseCollisionShapeIndex=mesh_collision_shape,
#     baseVisualShapeIndex=mesh_visual_shape,
#     basePosition=mesh_position,
#     baseOrientation=mesh_orientation,
# )

mesh_scale = [.1, .1, .1]  # The scale of the mesh
mesh_collision_shape = p.createCollisionShape(
    shapeType=p.GEOM_MESH,
    fileName="models/triple_hook/triple_hook_vhacd.obj",
    meshScale=mesh_scale,
    # flags=p.GEOM_FORCE_CONCAVE_TRIMESH,
    # meshData=mesh_data,
)
mesh_visual_shape = -1  # Use the same shape for visualization
mesh_position = [0, 0, 0]  # The position of the mesh
mesh_orientation = p.getQuaternionFromEuler([1.57, 0, 0])  # The orientation of the mesh
hook = p.createMultiBody(
    baseCollisionShapeIndex=mesh_collision_shape,
    baseVisualShapeIndex=mesh_visual_shape,
    basePosition=mesh_position,
    baseOrientation=mesh_orientation,
)

def getJointStates(robot):
  joint_states = p.getJointStates(robot, range(p.getNumJoints(robot)))
  joint_positions = [state[0] for state in joint_states]
  joint_velocities = [state[1] for state in joint_states]
  joint_torques = [state[3] for state in joint_states]
  return joint_positions, joint_velocities, joint_torques

i = 0
jointPositionsSce = []
gemPosAll = []
gemOrnAll = []
while (1):
    p.stepSimulation()
    #p.setJointMotorControl2(botId, 1, p.TORQUE_CONTROL, force=1098.0)
    # p.applyExternalTorque(mesh_id, -1, [1,0,0], p.WORLD_FRAME)
    # print(gemPos, gemOrn)
    p.setGravity(0, 0, GRAVITY)
    time.sleep(7/240.)
    i += 1

    # CP = p.getClosestPoints(bodyA=fish, bodyB=mesh_id, distance=-0.01)
    # if len(CP)>0:
    #     dis = [CP[i][8] for i in range(len(CP))]
    #     print('!!!!CP', dis)

    # if i % 20 == 0:
    #     jointPositions,_,_ = getJointStates(fish) # list(11)
    #     gemPos, gemOrn = p.getBasePositionAndOrientation(fish) # tuple(3), tuple(4)
    #     jointPositionsSce.append(jointPositions)
    #     gemPosAll.append(list(gemPos))
    #     gemOrnAll.append(list(gemOrn))
    
    # if i == 500:
    #     break
    # # print(jointPositions)

# replay



