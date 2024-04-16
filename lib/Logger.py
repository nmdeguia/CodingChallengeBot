import os
import datetime

class Logger:
    def __init__(self,
                logfile = "app.log",
                shared = False,
                identifier = None):
        #create_mode = "w+" if shared == False else "a"
        with open(logfile, "a") as file:
            if shared == False: file.write("Log file created\n")
            else: file.write("Log file opened\n")
            
        self.identifier =  "" if identifier == None else " "+str(identifier)+":"
            
    def write_to_logfile(self): pass
    
    def datestamp(self):
        time = datetime.datetime.now()
        return time.strftime("%Y-%m-%d")
            
    def timestamp_raw(self):
        time = datetime.datetime.now()
        return {datetime.datetime.timestamp(time), time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]}
        
    def timestamp(self):
        time = datetime.datetime.now()
        return time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            
    def info(self, *args):
        print(f"[{self.timestamp()}] INFO:{self.identifier}", *args)
        
    def warning(self, *args):
        print(f"[{self.timestamp()}] WARNING:{self.identifier}", *args)
        
    def error(self, *args):
        print(f"[{self.timestamp()}] ERROR:{self.identifier}", *args)
    
class Severity:
    def __init__(self):
        self.INFO = "INFO"
        self.WARNING = "WARNING"
        self.ERROR = "ERROR"
        self.FATAL = "FATAL"
        self.CRITICAL = "CRITICAL"