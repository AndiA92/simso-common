import sys
from simso.core import Model
from simso.configuration import Configuration
from simso.core.Measurement import Measurement
import csv


def main(argv):
    if len(argv) == 3:
        # Configuration load from a file.
        configuration = Configuration(argv[1])
        outputFileName = argv[2]
    else:
        raise Exception("Configuration is not correct.")

        # SPORADIC TASKS ALGOS
    schedulingAlgos = [
        'simso.schedulers.EDCL',
        'simso.schedulers.EDF',
        'simso.schedulers.EDF_US',
        'simso.schedulers.EDHS',
        'simso.schedulers.EDZL',
        'simso.schedulers.G_FL',
        'simso.schedulers.G_FL_ZL',
        'simso.schedulers.LB_P_EDF',
        'simso.schedulers.LLF',
        'simso.schedulers.MLLF',
        'simso.schedulers.PD2',
        'simso.schedulers.P_EDF2',
        'simso.schedulers.P_EDF',
        'simso.schedulers.P_EDF_WF',
        'simso.schedulers.PriD',
        'simso.schedulers.P_RM',
        'simso.schedulers.RM',
        'simso.schedulers.RUN',
        'simso.schedulers.Static_EDF',
    ]

    # Check the config before trying to run it.
    configuration.check_all()

    # open csv file
    with open(outputFileName, 'w') as csvfile:
        fieldnames = ['Algo'] + Measurement.fieldNames
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for scheduler in schedulingAlgos:
            # overwrite scheduling algorithm
            configuration.scheduler_info.clas = scheduler
            # Init a model from the configuration.
            model = Model(configuration)
            # Execute the simulation.
            model.run_model()
            configuration = Configuration(argv[1])

            print("Finished for algo: " + scheduler)

            # Print response times
            for measurement in model._measurements:
                writer.writerow({fieldnames[0]: scheduler,
                                 fieldnames[1]: measurement._taskName,
                                 fieldnames[2]: measurement._taskType,
                                 fieldnames[3]: measurement._activationTime,
                                 fieldnames[4]: measurement._startTime,
                                 fieldnames[5]: measurement._endTime,
                                 fieldnames[6]: measurement._deadline,
                                 fieldnames[7]: measurement._compTime,
                                 fieldnames[8]: measurement._respTime}
                                )

    csvfile.close()


main(sys.argv)
