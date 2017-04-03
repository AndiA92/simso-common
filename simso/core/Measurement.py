class Measurement:
    fieldNames = ['Task Name', 'Activation Time', 'Start Time', 'End Time', 'Deadline', 'Comp Time', 'Resp Time']

    def __init__(self, taskName, activationTime, startTime, endTime, deadline, compTime, respTime):
        self._taskName = taskName
        self._activationTime = activationTime
        self._startTime = startTime
        self._endTime = endTime
        self._deadline = deadline
        self._compTime = compTime
        self._respTime = respTime
