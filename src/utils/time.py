from datetime import datetime


def currentTimeStamp(name: str) -> str:
    dateTimeObj = datetime.now()
    return dateTimeObj.year + '_' + dateTimeObj.month + '_' + dateTimeObj.day + '_' + dateTimeObj.hour + '_' + dateTimeObj.minute + '_' + dateTimeObj.second + '_' + name
