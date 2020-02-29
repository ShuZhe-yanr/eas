import time
import eas.target
import eas.factor
import eas.boundary
import eas.selection
import numpy as np
from eas import HRO

# 常规参数项
eas.log_flag = False  # 用于记录日志开关，当前记录信息
times = 50  # 算法执行的总次数
gen = 3000  # 3000  # 一次算法的迭代次数
_np = 60  # 60  # 总群个体的数量
n = 10  # 10  # 解向量的维数
# 向量越界策略
boundary_strategy = eas.boundary.Boundary.BOUNDARY
# 目标函数，其最优解为 100
fitness_func = eas.target.f8

# 参数项
upperxs = np.array([500] * n) # 向量各分量上限
lowerxs = np.array([-500] * n) # 向量各分量下限
eas.TrialSolution.TRIAL_LIMIT = 8  # HRO 个体检验的最大次数

# 开始
time_str = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
log_file = open(
    './storages/logs/HRO-function-08-%s-summary.tsv' % time_str,
    mode='ab')

for i in range(times):
    print('round %d start: ' % (i + 1))
    # 由于因子有生成次数限制，所以需要在 times 循环体内重新创建
    factors = {
        'r1': eas.factor.RandomFactor([-1.0, 1.0], gen, n),
        'r2': eas.factor.RandomFactor([-1.0, 1.0], gen, n),
        'r3': eas.factor.RandomFactor([0.0, 1.0], gen, n),
    }

    algo = HRO(_np, n, upperxs, lowerxs,
               factors=factors,
               optimal_minimal=True,
               fitness_func=fitness_func,
               boundary_strategy=boundary_strategy,
               solution_class='TrialSolution')

    algo.fit(gen)
    np.savetxt(log_file, np.array(algo.best_fitness_store).T[np.newaxis], delimiter=',')

    print('round %d end: ' % (i + 1))

log_file.close()




