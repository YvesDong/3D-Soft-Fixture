import os.path as osp
import sys
sys.path.insert(0, osp.join(osp.dirname(osp.abspath(__file__)), '../'))
from cagingSearchAlgo import *
import pybullet as p
from utils import *
from time import sleep
import numpy as np

# for test03: band-hourglass
r1 = 0.74
r2 = 1.0
h = 0.86
# k = 1.0
n = np.asarray(list(range(7,10)))
k = np.asarray(list(range(7,10)))
alpha = 180 / n
alpha = alpha / 180 * np.pi
R1 = r1 / np.cos(alpha)
s1 = 2 * r1 * np.tan(alpha)
s2 = 2 * r2 * np.tan(alpha)
# E1 = np.asarray([0.0]*7)
E2 = 0.5 * k * n * (s2-s1)**2 # E_true = 1.3847808

if __name__ == '__main__':
    for s in range(7):
        args, parser = argument_parser()
        # basePosBounds=[[-5,5], [-5,5], [-3,5]] # searching bounds

        # create caging environment and items in pybullet
        # if args.object in get_non_articulated_objects():
        #     env = RigidObjectCaging(args)
        #     env.add_obstacles(scale=[.1]*3, pos=[0,0,0], qtn=p.getQuaternionFromEuler([1.57, 0, 0]))

        if args.object == 'Ring':
            start = [0.5798,0.0094,1.391,0,0,0]
            goal = [1.5,0,1.5]+[1.57,1.57,0]
            goalSpaceBounds = [[1.4,2], [-.5,.5], [1.3,2.1]] + [[math.radians(-180), math.radians(180)]] + [[-.1, .1]]*2
            env = RigidObjectCaging(args)
            env.add_obstacles(scale=[.1]*3, pos=[0,0,2], qtn=p.getQuaternionFromEuler([1.57, -0.3, 0]))
            env.robot.set_search_bounds(basePosBounds=[[-.3,2], [-.5,.5], [1.3,2.8]])
            env.reset_start_and_goal(start=start, goal=goal)
        if args.object == 'FishHole':
            env = RigidObjectCaging(args)
            goalSpaceBounds = [[-1,1], [-.5,3], [1.2,1.3]] + [[math.radians(-180), math.radians(180)]]*3
            env.add_obstacles(scale=[.1]*3, pos=[0.5,1.150,3.60], qtn=[0.223,0.0,0.0,0.974])
            env.robot.set_search_bounds(basePosBounds=[[-3,3], [-1,5], [0,6]])
            objEul = list(p.getEulerFromQuaternion([0.381828,-0.174,-0.06460,0.90529]))
            env.reset_start_and_goal(start=[-0.0522,1.4564,2.3247,]+objEul, goal=[0,3,2]+[0,0,0])
        elif args.object == 'Fish':
            objScale = 1
            env = ArticulatedObjectCaging(args, objScale)
            env.add_obstacles(scale=[1]*3, pos=[0,0,2], qtn=p.getQuaternionFromEuler([0, 0, 0]))
            env.reset_start_and_goal(start=[0,0,3.8]+[0,0,0]+[0]*env.robot.articulate_num, goal=[0,0,.1]+[0,0,0]+[0]*env.robot.articulate_num)
        elif args.object == 'Snaplock':
            objScale = 3
            env = ArticulatedObjectCaging(args, objScale)
            env.add_obstacles(scale=[.1]*3, pos=[-.5,0,3], qtn=p.getQuaternionFromEuler([0, 0, 0])) # ring
            # env.robot.set_search_bounds(basePosBounds=[[-2,2], [-2,2], [0,3.5]])
            env.reset_start_and_goal(start=[0,0,1.8,0,0,1.57]+[0], goal=[0,0,.01]+[0,1.57,0]+[0])
        elif args.object == 'Starfish':
            objScale = 1
            env = ArticulatedObjectCaging(args, objScale)
            env.add_obstacles(scale=[1]*3, pos=[0,0,.6], qtn=p.getQuaternionFromEuler([0, 0, 0])) # splash bowl
            # env.add_obstacles(scale=[10]*3, pos=[0,0,1], qtn=p.getQuaternionFromEuler([1.57, 0, 0])) # 3fGripper
            # env.robot.set_search_bounds(basePosBounds=[[-2,2], [-2,2], [0,3.5]])
            start = [-0.401751, -0.198753, 1.46589, -0.529868, 0.138347, -0.357632, -0.5, 0.5, -0.17, 0.35, 0.5, 0.5, 0.22, 0.5, 0.5, 0.41]
            env.reset_start_and_goal(start=start, goal=[0,0,.01]+[0,0,1.57]+[0]*env.robot.articulate_num)
        elif args.object == 'Band':
            numCtrlPoint = 6
            start = generate_circle_points(numCtrlPoint, rad=.3, z=1.4)
            goal = generate_circle_points(numCtrlPoint, rad=.3, z=.1)
            # start = generate_circle_points(numCtrlPoint, rad=.8, z=0.98)
            # goal = generate_circle_points(numCtrlPoint, rad=.2, z=2.18)
            env = ElasticBandCaging(args, numCtrlPoint, start, goal)
            env.add_obstacles(scale=[1]*3, pos=[0,0,0], qtn=p.getQuaternionFromEuler([0, 0, 0]))
        elif args.object == 'BandHorizon':
            numCtrlPoint = n[s].item()
            goalSpaceBounds = [[-2,2], [-2,2],]*numCtrlPoint + [[0.88, 2]]
            start = generate_circle_points(numCtrlPoint, rad=R1[s].item(), z=0.01, obj=args.object) # r1=0.735, r2 = 1.0, h=0.86
            goal = generate_circle_points(numCtrlPoint, rad=R1[s].item(), z=1.5, obj=args.object)
            env = ElasticBandCaging(args, numCtrlPoint, start, goal)
            env.add_obstacles(scale=[1]*3, pos=[0,0,0], qtn=p.getQuaternionFromEuler([0, 0, 0]))
            env.robot.set_search_bounds(basePosBounds=[[-2,2], [-2,2], [0.01, 2]], start=start)
        elif args.object == 'Rope':
            numCtrlPoint = 4
            linkLen = 0.3
            start = [0,0,.7,1.57,0,0] + [math.radians(360/(numCtrlPoint+1)),0]*numCtrlPoint
            goal = [0,0,.1,0,1.57,0] + [math.radians(360/(numCtrlPoint+1)),0]*numCtrlPoint
            env = RopeCaging(args, numCtrlPoint, linkLen, start, goal)
            env.add_obstacles(scale=[1]*3, pos=[0,0,.5], qtn=p.getQuaternionFromEuler([0, 0, 0])) # bucket
        elif args.object == 'Chain':
            numCtrlPoint = 4 # numCtrlPoint+3 links
            linkLen = 0.7
            start = [-.5,0.3,1.,1.,0,1.57] + [math.radians(360/(numCtrlPoint+3)-1),0]*numCtrlPoint + [0]
            goal = [0,0,.1,0,1.57,0] + [math.radians(360/(numCtrlPoint+3)-1),0]*numCtrlPoint + [0]
            env = ChainCaging(args, numCtrlPoint, linkLen, start, goal)
            env.robot.set_search_bounds(vis=1, basePosBounds=[[-2,2], [-2,2], [0, 3]])
            env.add_obstacles(scale=[10]*3, pos=[0,-.5,2.2], qtn=p.getQuaternionFromEuler([-1.57, -2, 1.57])) # 3fGripper
        elif args.object == 'Jelly':
            numCtrlPoint = 4
            l = 1
            zs = 1
            ofs = 0.7
            start = [-l/2,-l/2,-l/2+zs] + [-l/2,-l/2,l/2+zs] + [l/2,-l/2,l/2+zs] + [-l/2,l/2,l/2+zs]
            goal = [-l/2-ofs,-l/2-ofs,-l/2+zs] + [-l/2-ofs,-l/2-ofs,l/2+zs] + [l/2-ofs,-l/2-ofs,l/2+zs] + [-l/2-ofs,l/2-ofs,l/2+zs]
            env = ElasticJellyCaging(args, numCtrlPoint, start, goal)
            env.add_obstacles(scale=[1]*3, pos=[0,0,0], qtn=p.getQuaternionFromEuler([0, 0, 0])) # maze
            env.robot.set_search_bounds(basePosBounds=[[-2,2], [-2,2], [0,3]])
        elif args.object == '2Dlock':
            objScale = 1
            basePosBounds = [[-5, 5], [-5, 5]]
            env = SnapLock2DCaging(args, objScale, basePosBounds)
            env.add_obstacles(scale=[1]*3, pos=[1.25,-2.9,0], qtn=p.getQuaternionFromEuler([0, 0, 3.7]))
            env.reset_start_and_goal(start=[-2,2,0,-0.36], goal=[2,2,0,0])

        env.create_ompl_interface()
        print('STATE IS VALID',env.pb_ompl_interface.is_state_valid(start))
        env.pb_ompl_interface.set_goal_space_bounds(goalSpaceBounds)
        if args.object == 'BandHorizon':
            springneutralLen = s1[s].item()
            k_spring = k[s].item()
            env.pb_ompl_interface.set_spring_params(springneutralLen, k_spring)
        
        # Choose from different searching methods
        if args.search == 'BisectionSearch':
            # useGreedySearch = False # True: bisection search; False: Conservative search
            # env.bound_shrink_search(useGreedySearch)
            env.energy_bisection_search(maxTimeTaken=40, useBisectionSearch=1)
            env.visualize_bisection_search() # visualize

        elif args.search == 'EnergyBiasedSearch':
            numInnerIter = 2
            env.energy_biased_search(numIter=numInnerIter, save_escape_path=0, )
            E2real = env.sol_final_costs
            # env.visualize_energy_biased_search()
            print('Energy costs of current obstacle and object config: {}'.format(env.sol_final_costs))

            with open('./data2.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(E2real)
                
        # shut down pybullet (GUI)
        p.disconnect()

        # TODO: comapare the results with ground truth (Open3d OBB - donut model)