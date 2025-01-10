from typing import List

from phi.tools import Toolkit
from phi.utils.log import logger
from ixnetwork_restpy.testplatform.testplatform import TestPlatform
import os
from ixnetwork_restpy import SessionAssistant, Files
from typing import List
import json

class IxNetworkRestPy(Toolkit):
    def __init__(self):
        super().__init__(name="IxNetworkRestPy")
        self.register(self.get_session_information)
        self.register(self.get_all_sessions)
        self.register(self.deleteSession)
        self.register(self.create_session)
        self.register(self.get_list_of_ixia_configuration_files)
        self.register(self.load_ixia_configuration_into_the_session)


    def get_session_information(self, testPlatform: object=None, apiServerIp: str=None, sessionId: str= None) -> List:
        """This method gets session information of single session by querying sessionID

        Args:
            testPlatform (object): testPlatform Object used to interace with IxNetwork Web Instance
            apiServerIp(str): IP address for IxNetwork Web Instance
            sessionId (str): sessionId to be queried

        Returns:
            List: List of different session values.
        """
        if not testPlatform:
            testPlatform = self.get_tp_object(apiServerIp)
        session = testPlatform.Sessions.find(Id=sessionId)
        sessionStatus = "NOERROR"
    
        ixNetwork = session.Ixnetwork.Globals
        errorList = session.Ixnetwork.Globals.find().AppErrors.find().Error.find(ErrorLevel='kError')
        errorCount = session.Ixnetwork.Globals.find().AppErrors.find().ErrorCount
        list_of_errors = [a.Name for a in errorList]
        if list_of_errors: sessionStatus = "ERROR"
            
        sessionName = session.Name
        vports = session.Ixnetwork.Vport.find()
        port_info = []
        
        for index ,port in enumerate(vports):
                portobj = vports[index]
                connectionState = portobj.ConnectionState
                assignedDisplayName = portobj.AssignedToDisplayName
                port_info.append(f"{assignedDisplayName}_{connectionState}")
        
        return [str(sessionId), sessionName, sessionStatus, str(errorCount), "--".join(list_of_errors), ixNetwork.Username]

    def get_all_sessions(self, apiServerIp:str) -> List:
        """This method will get information about all the IxNetwork Sessions on IxNetwork Web API Server
        Args:
            apiServerIp (object): IP address of IxNetwork Web Instance
        Returns: 
            String represenation of all the sessions information
        """      
        list_of_lists = []                                
        testPlatform = self.get_tp_object(apiServerIp)

        
        for session in testPlatform.Sessions.find():
            sessionId = session[0].Id
            list_of_lists.append(self.get_session_information(testPlatform=testPlatform, sessionId=sessionId))

        # Define the headers (keys for the dictionaries)
        headers = ['sessionId', 'sessionName', 'sessionStatus', 'errorCount', 'ErrorList', 'User']
        import pandas as pd
        # Convert each list into a dictionary by mapping the headers to each item in the list
        list_of_dicts = [dict(zip(headers, item)) for item in list_of_lists]
        # Output the result as a list of dictionaries              
        if isinstance(list_of_dicts, list) and all(isinstance(item, dict) for item in list_of_dicts):
        # Convert the data into a Pandas DataFrame for tabular format
            from tabulate import tabulate
            # Create a tabular string format
            table = tabulate(list_of_dicts, headers="keys", tablefmt="grid")
            return table
        else:
            print("Response is not in the expected format.")                                                                                                                           
            return table


    def get_tp_object(self, apiServerIp: str, rest_port: str = '443', platform: str='linux'):
        """This method creates a testPlatform Object to interact with IxNetwork Web Test Sessions

        Args:
            apiServerIp (str): IP address of IxNetwork Web Instance
            rest_port (str, optional): Rest Port to connect on IxNetwork Web API Server_. Defaults to '443'.
            platform (str, optional): Platfrom IxNetwork Web Instance. Defaults to 'linux'.

        Returns:
            Object: testPlatform Object
        """
        testPlatform = TestPlatform(apiServerIp, rest_port=rest_port, platform=platform)
        testPlatform.Authenticate("admin", "admin")
        return testPlatform

    def deleteSession(self, testPlatform=None, Id=None, apiServerIp=None):
        """This method deletes sessions provided a SessionId

        Args:
            testPlatform (Object, optional): testPlatform object
            apiServerIp (str): IP address of IxNetwork Web Instance
            Id (str, optional): SessionId to be deleted
        Returns:
            Object: testPlatform Object
        """
        if not testPlatform:
            testPlatform = self.get_tp_object(apiServerIp)
        session_obj = testPlatform.Sessions.find(Id=Id)
        try:
            session_obj.Id
            session_obj.remove()
        except IndexError:
            return (f"====> Session ID {Id} is not present on the IxNetwork Web Instance")
        return (f"====> Session ID {Id} Deleted")

    def create_session(self, apiServerIp: str, session_name:str=None):
        """This method creates a new IxNetwork Web Session usinf TestPlatform create_session API's.
        If user provided session name use it else just use none

        Args:
            apiServerIp (str): IxNetworkWeb API server IP
            name(str): If a user wants to name a session something
            ixncfg_filename:str = None: Start an Ixia Session with Configuration

        Returns:
            _type_: List of dictionary of session information with default header
        """
        list_of_lists = []
        testPlatform = self.get_tp_object(apiServerIp)
        session = testPlatform.Sessions.add(ApplicationType='ixnrest', Name=session_name)

        list_of_lists.append(self.get_session_information(testPlatform, session.Id))

        # Define the headers (keys for the dictionaries)
        headers = ['sessionId', 'sessionName', 'sessionStatus', 'errorCount', 'ErrorList', 'User']
        list_of_dicts = [dict(zip(headers, item)) for item in list_of_lists]
        # Output the result as a list of dictionaries                                                                                                                                     
        return json.dumps(list_of_dicts)


    def get_ixnetwork_session_assistant(self, apiServerIp: str, session_name: str, session_id:str):
        # Step 1: Connect to the IxNetwork API
        session = SessionAssistant(
            IpAddress=apiServerIp,  # Replace with your IxNetwork server IP
            RestPort=443,         # Replace with the appropriate REST port
            UserName="admin",
            Password="admin",
            SessionName=session_name,
            SessionId=session_id,
            LogLevel=SessionAssistant.LOGLEVEL_INFO,
            ClearConfig=True
        )
        ixnetwork = session.Ixnetwork
        return ixnetwork

    # Step 2: List all files with the desired extension
    def get_list_of_ixia_configuration_files(self, directory: str, extension: str):
        """
        This method lists all the Ixia Configuration Files.

        :param directory: Path to the directory containing files.
        :param extension: File extension to filter (e.g., '.csv', '.json', '.ixncfg).
        :return: List of matching file paths.
        """
        return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(extension)]

    def load_ixia_configuration_into_the_session(self, apiServerIP:str, configuration_file:str, session_name:str = None, session_id:str = None):  
        """This method will load configuration file into existing session

        Args:
            apiServerIP (str): Linux API server web instance
            configuration_file (str): .ixncfg file to use
            session_name (str): Session Name to connect and load the configuration file
            session_id: Session Id to connect to and load the configuration file
        """
        ixNetwork = self.get_ixnetwork_session_assistant(apiServerIP, session_name, session_id)
        ixNetwork.info('Loading config file: {0}'.format("./ixiaConfigs/"+configuration_file))
        ixNetwork.LoadConfig(Files(configuration_file, local_file=True))
        return f"File {configuration_file} upoaded successfully to {session_id}, {session_name}"


