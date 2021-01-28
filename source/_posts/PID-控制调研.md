---
title: PID 控制调研
date: 2021-01-28 21:36:29
tags: [PID, 控制]
---
### 前言
在推荐页的某些场景下，我们需要对不同类型的内容做分发控制，以满足产品策略确定的分发量或分发占比。PID 控制是一种自动控制领域比较常见的控制方式。本文编写 PID 控制代码，并模拟被控制系统，调研使用 PID 控制的可行性。
### 测试代码
```python
def limit_by_bounds(value, bounds):
    if not bounds:
        return value

    if bounds[0] is not None and value < bounds[0]:
        return bounds[0]
    if bounds[1] is not None and value > bounds[1]:
        return bounds[1]

    return value


class PIDController(object):

    def __init__(self, kp, ki, kd, set_value, i_sum_bounds=None, bounds=None):
        """ 初始化 PIDController（简化版，不包含采样时间，用于离线模拟 PID 控制的过程）
        :param kp: Kp
        :param ki: Ki
        :param kd: Kd
        :param set_value: 设置值
        :param i_sum_bounds: error 积分的最大值
        :param bounds: PID 输出的最大区间
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.set_value = set_value
        self.bounds = bounds
        self.i_sum_bounds = i_sum_bounds

        self.last_err = None  #上一次执行的 Error
        self.integral_sum = 0  # Error 累积值

    def update(self, cur_value):
        """ 根据当前的状态，计算最新的 PID_output
        :param cur_value: 测量模块测得的系统最新值
        :return: PID_output
        """
        cur_err = self.set_value - cur_value  # 当前误差
        self.integral_sum = limit_by_bounds(self.integral_sum + cur_err, self.i_sum_bounds)  # 误差积分

        o1 = self.kp * cur_err  # 比例控制部分输出
        o2 = self.ki * self.integral_sum  # 积分控制部分输出
        o3 = self.kd * (cur_err - self.last_err) if self.last_err else 0  # 微分部分输出

        # print(o1, o2, o3)
        self.last_err = cur_err  #更新 last_err
        return limit_by_bounds(o1 + o2 + o3, self.bounds)  # return PID_output

    def reset(self):
        """ 重置 PIDController """
        self.last_err = None
        self.integral_sum = 0


class ControlledSystem(object):
    """ 模拟一个被控制的系统，这里模拟一个 tuner 调参的场景，具体逻辑为：
    假设我们要控制某一类内容的「分发占比」情况，且 tuner 权重与分发占比的关系为：分发占比 = 当前权重 * coefficient
    若当前权重为 0.2，coefficient 为 10，则分发占比为 2%...
    为了模拟更真实的状况，coefficient 随着自动控制的进行，会不断的发生变化，通过传入参数 setting 来实现
    """

    def __init__(self, init_weight, setting=None):
        """
        :param init_weight: PID 开始运行时的初始权重
        :param setting: coefficient 设置
        """
        self.cur_w = init_weight
        self.setting = setting if setting else [10, 12, 8, 15]

    def process(self, round_, pid_output):
        """
        针对 PID_output 的处理方式一：将 PID_output 简单的加到内部维护的当前权重 cur_w 上
        :param round_: 当前是第 X 次施加控制，用于实现 coefficient 自动变化
        :param pid_output: PID_output
        :return: 新的「分发占比」
        """
        coefficient = self.setting[(round_ // 30) % len(self.setting)]  #实现 coefficient 的自动变化

        self.cur_w += pid_output  # 更新权重
        return self.cur_w * coefficient

    def process2(self, round_, pid_output):
        """ 针对 PID_output 的处理方式二：将 PID_output 直接作为当前权重 cur_w """
        coefficient = self.setting[(round_ // 30) % len(self.setting)]
        return pid_output * coefficient


def test(kp, ki, kd, set_value, init_weight, init_value, round_num, by_process2=False, pid_bounds=None):
    pid_controller = PIDController(kp, ki, kd, set_value, bounds=pid_bounds)
    controller_system = ControlledSystem(init_weight=init_weight)

    cur_value = init_value
    values = [cur_value]
    for i in range(round_num):
        output = pid_controller.update(cur_value)
        if by_process2:
            cur_value = controller_system.process2(i, output)
        else:
            cur_value = controller_system.process(i, output)

        values.append(cur_value)
    return values
```
### 方案一
执行
```python
test(kp, ki, kd, 5, 0.3, 3, 100)
```
若将 ki，kd 固定为 0，将 kp 分别取 0.01，0.07，0.1，0.13，得到（纵轴为 test 函数输出的 values，横轴为对应的 0,1,2...(len(values) - 1)，下同）
<img src="/images/pid1.png" width="80%" height="80%">可见，根据不同的系统状态（coefficient），这些参数都能将系统调节到 set_value，但是不同的状态下，最优的 kp 是不同的

若将 ki，kd 固定为 0，将 kp 取 0.2，得到
<img src="/images/pid2.png" width="80%" height="80%">若 kp 超出特定的范围，会出现失控的状况。在这里，当 coefficient 为 10 时，kp >= 0.2(1/10 * 2) 时会出现这种状况
### 方案二
执行
```python
test(kp, ki, kd, 5, 0.3, 3, 100, by_process2=True)
```
若将 ki，kd 固定为 0，调节 kp，可得
<img src="/images/pid3.png" width="80%" height="80%">可见是存在稳态误差的

若将 kp 固定为 0.06，kd 固定为 0，调节 ki，可得
<img src="/images/pid4.png" width="80%" height="80%">可见 PI 是也能达到预期的控制目的的，但如果参数超出范围，仍会出现「失控」的情况
### 参考
1. [超清楚的PID控制官方科普教程](https://www.bilibili.com/video/BV1wT4y1G7UQ?from=search&seid=4297002407491516846)
2. [如何通俗地解释 PID 参数整定？](https://www.zhihu.com/question/23088613)
3. [PID控制器](https://zh.wikipedia.org/wiki/PID%E6%8E%A7%E5%88%B6%E5%99%A8)
