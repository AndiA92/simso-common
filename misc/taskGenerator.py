import sys
import random
import csv
import math

from simso.configuration import Configuration
from simso.core import Model
from simso.generator.task_generator import StaffordRandFixedSum, \
    gen_periods_loguniform, gen_tasksets


def get_periods():
    return ("lunif", 1.0, 1000.0, False)


def gen_arrivals(period, min_, max_, round_to_int=False):
    def trunc(x, p):
        return int(x * 10 ** p) / float(10 ** p)

    dates = []
    n = min_ - period
    while True:
        n += next_arrival_poisson(period) + period
        if round_to_int:
            n = int(round(n))
        else:
            n = trunc(n, 6)
        if n > max_:
            break
        dates.append(n)
    return dates


def next_arrival_poisson(period):
    return -math.log(1.0 - random.random()) * period


def main(argv):
    global procCount
    if len(argv) == 8:
        # Configuration load from a file.
        nrOfRuns = int(argv[1])
        nrOfProc = int(argv[2])
        minNrOfPeriodicTasks = int(argv[3])
        maxNrOfPeriodicTasks = int(argv[4])
        minNrOfSporadicTasks = int(argv[5])
        maxNrOfSporadicTasks = int(argv[6])
        tasksFileName = argv[7]
    else:
        raise Exception("Configuration is not correct.")

    schedulingAlgos = [
        'simso.schedulers.EDCL',
        'simso.schedulers.EDF',
        # 'simso.schedulers.EDF_US',
        'simso.schedulers.EDHS',
        # 'simso.schedulers.EDZL',
        'simso.schedulers.G_FL',
        # 'simso.schedulers.G_FL_ZL',
        'simso.schedulers.LB_P_EDF',
        # 'simso.schedulers.LLF',
        # 'simso.schedulers.MLLF',
        # 'simso.schedulers.PD2',
        # 'simso.schedulers.P_EDF2',
        # 'simso.schedulers.P_EDF',
        # 'simso.schedulers.P_EDF_WF',
        # 'simso.schedulers.PriD',
        'simso.schedulers.P_RM',
        'simso.schedulers.RM',
        'simso.schedulers.RUN',
        # 'simso.schedulers.Static_EDF',
    ]

    with open(tasksFileName, 'w+') as csvfile:
        fieldnames = ['Index', 'Successful', 'Algo', 'NrOfProc', 'Utilization', 'NrOfPeriodic', 'NrOfSporadic', 'AvgPeriod_Periodic',
                      'AvgActivation_Sporadic', 'TaskName', 'TaskType', 'RespTime', 'Avg_CPU']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for runCounter in range(1, nrOfRuns + 1):
            nrOfPeriodic = random.randint(minNrOfPeriodicTasks, maxNrOfPeriodicTasks)
            nrOfSporadic = random.randint(minNrOfSporadicTasks, maxNrOfSporadicTasks)
            utilization = round(random.uniform(nrOfProc/2, nrOfProc), 1)

            u = StaffordRandFixedSum(nrOfPeriodic + nrOfSporadic, utilization, 1)
            p_types = get_periods()
            p = gen_periods_loguniform(nrOfPeriodic + nrOfSporadic, 1, p_types[1], p_types[2], p_types[3])

            if u and p:
                taskset = gen_tasksets(u, p)[0]

                print (
                    "Generating configuration with id " + str(runCounter) + " NrOfPeriodic: " + str(nrOfPeriodic) + ", NrOfSporadic: " + str(nrOfSporadic) + ", Utilization: " + str(utilization))

                configuration = Configuration()
                configuration.duration = 100 * configuration.cycles_per_ms

                for procCount in range(1, nrOfProc+1):
                    configuration.add_processor(name = "CPU_" + procCount.__str__(), identifier=procCount)

                i = 0
                sumOfPeriods_Periodic = 0
                sumOfActivations_Sporadic = 0
                for ci, pi in taskset:
                    i += 1
                    if i <= nrOfPeriodic:
                        configuration.add_task(
                            "Task " + str(i), i, period=pi, wcet=ci, deadline=pi)
                        sumOfPeriods_Periodic += pi
                    else:
                        list_activation_dates = gen_arrivals(pi, 0, configuration.duration_ms)
                        configuration.add_task(
                            "Task " + str(i), i, period=pi, wcet=ci, deadline=pi,
                            task_type="Sporadic", list_activation_dates=list_activation_dates)

                        if (len(list_activation_dates) == 0):
                            sumOfActivations_Sporadic += 0
                        else:
                            sumOfActivations_Sporadic += sum(list_activation_dates) / len(list_activation_dates)

                for scheduler in schedulingAlgos:
                    configuration.scheduler_info.clas = scheduler
                    # Init a model from the configuration.
                    model = Model(configuration)
                    # Execute the simulation.

                    successFul = False
                    try:
                        model.run_model()
                        successFul = True
                    except:
                        print('Algorithm ' + scheduler + " failed!")
                        successFul = False

                    print("Finished for algo: " + scheduler)

                    if(successFul):
                        # Print response times
                        for measurement in model._measurements:
                            taskName = measurement._taskName
                            taskType = measurement._taskType
                            respTime = measurement._respTime

                            averageCPULoad = model.getAverageLoad()

                            writer.writerow({fieldnames[0]: runCounter,
                                            fieldnames[1]: successFul,
                                            fieldnames[2]: scheduler,
                                            fieldnames[3]: procCount,
                                            fieldnames[4]: utilization,
                                            fieldnames[5]: nrOfPeriodic,
                                            fieldnames[6]: nrOfSporadic,
                                            fieldnames[7]: sumOfPeriods_Periodic / nrOfPeriodic,
                                            fieldnames[8]: sumOfActivations_Sporadic / nrOfSporadic,
                                            fieldnames[9]: taskName,
                                            fieldnames[10]: taskType,
                                            fieldnames[11]: respTime,
                                            fieldnames[12]: averageCPULoad}
                                            )

            else:
                print(
                "Incorrect configuration: NrOfPeriodic: " + str(nrOfPeriodic) + ", NrOfSporadic: " + str(nrOfSporadic) + ", Utilization: " + str(utilization))

        csvfile.close()

main(sys.argv)


