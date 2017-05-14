class Measurement:
    fieldNames = ['TaskName', 'TaskType', 'Aborted', 'ActivationTime', 'StartTime', 'EndTime', 'Deadline', 'CompTime', 'RespTime']

    def __init__(self, taskName, taskType, aborted, activationTime, startTime, endTime, deadline, compTime, respTime):
        self._taskName = taskName
        self._taskType = taskType
        self._aborted = aborted
        self._activationTime = activationTime
        self._startTime = startTime
        self._endTime = endTime
        self._deadline = deadline
        self._compTime = compTime
        self._respTime = respTime
