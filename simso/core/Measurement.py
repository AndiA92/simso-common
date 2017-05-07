class Measurement:
    fieldNames = ['TaskName', 'TaskType', 'ActivationTime', 'StartTime', 'EndTime', 'Deadline', 'CompTime', 'RespTime']

    def __init__(self, taskName, taskType, activationTime, startTime, endTime, deadline, compTime, respTime):
        self._taskName = taskName
        self._taskType = taskType
        self._activationTime = activationTime
        self._startTime = startTime
        self._endTime = endTime
        self._deadline = deadline
        self._compTime = compTime
        self._respTime = respTime
