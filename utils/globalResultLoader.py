# coding: utf-8
# Author: Roy Luo
# Version: 1.0


import logging
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
from tabulate import tabulate
import pandas as pd
from io import StringIO
import sys

@dataclass
class GeneralInformation:
    def __init__(self, title, Date, MacVersion, Project, Customer, UnitType, ECUVersion, 
                 Algorithm_version, DisplacementUnit, Calibration, Batch_Mode_File_Name, 
                 StudyType, DataValidityMsg, XMLFileVersion, ProjectPath, ECUPath):
        self.title = title
        self.Date = Date
        self.MacVersion = MacVersion
        self.Project = Project
        self.Customer = Customer
        self.UnitType = UnitType
        self.ECUVersion = ECUVersion
        self.Algorithm_version = Algorithm_version
        self.DisplacementUnit = DisplacementUnit
        self.Calibration = Calibration
        self.Batch_Mode_File_Name = Batch_Mode_File_Name
        self.StudyType = StudyType
        self.DataValidityMsg = DataValidityMsg
        self.XMLFileVersion = XMLFileVersion
        self.ProjectPath = ProjectPath
        self.ECUPath = ECUPath

    title: str
    Date: str
    MacVersion: str
    Project: str
    Customer: str
    UnitType: str
    ECUVersion: str
    Algorithm_version: str
    DisplacementUnit: str
    Calibration: str
    Batch_Mode_File_Name: str
    StudyType: str
    DataValidityMsg: str
    XMLFileVersion: str
    ProjectPath: str
    ECUPath: str


@dataclass
class TimeEvent:
    name: str
    description: str
    compute_displacement: str
    algorithm: str
    category: str


@dataclass
class Channel:
    # 定义 Channel 的属性
    pass


@dataclass
class MultiPreprocessingItem:
    information: Dict[str, str] = field(default_factory=dict)
    file_information: List[Dict[str, str]] = field(default_factory=list)
    file_information_df: pd.DataFrame = field(default_factory=pd.DataFrame)
    
    @dataclass
    class Mechanical:
        @dataclass
        class Parameter:
            name: str
            description: str
            unit: str
            value: float
        parameters: List[Parameter] = field(default_factory=list)
    mechanical: Mechanical = field(default_factory=Mechanical)
    
    @dataclass
    class Preprocessing:
        @dataclass
        class Sensor:
            name: str
            parameters: List[Dict[str, str]] = field(default_factory=list)
        sensors: List[Sensor] = field(default_factory=list)
        
        @dataclass
        class Acquisition:
            parameters: List[Dict[str, str]] = field(default_factory=list)
        acquisition: Acquisition = field(default_factory=Acquisition)
    preprocessing: Preprocessing = field(default_factory=Preprocessing)
    
    @dataclass
    class Drifts:
        @dataclass
        class Electronic:
            @dataclass
            class Drift:
                name: str
                description: str
                unit: str
                min: float
                nom: float
                max: float
                step: float
                points: int
            drifts: List[Drift] = field(default_factory=list)
        mechanical: Dict = field(default_factory=dict)
        electronic: Electronic = field(default_factory=Electronic)
        acquisition: Dict = field(default_factory=dict)
        algorithm: Dict = field(default_factory=dict)
    drifts: Drifts = field(default_factory=Drifts)
    
    @dataclass
    class PerformanceStudy:
        @dataclass
        class TimeEvent:
            name: str
            files: List[Dict[str, str]] = field(default_factory=list)
            df: pd.DataFrame = field(default_factory=pd.DataFrame)
        time_events: List[TimeEvent] = field(default_factory=list)
        time_events_dict: Dict[str, pd.DataFrame] = field(default_factory=dict)
    performance_study: PerformanceStudy = field(default_factory=PerformanceStudy)
    
    @dataclass
    class TimeEventDistribution:
        @dataclass
        class TimeEvent:
            name: str
            @dataclass
            class File:
                name: str
                occurrences: List[Dict[str, float]] = field(default_factory=list)
            files: List[File] = field(default_factory=list)
        time_events: List[TimeEvent] = field(default_factory=list)
    time_event_distribution: TimeEventDistribution = field(default_factory=TimeEventDistribution)
    
    @dataclass
    class FullMarginStudy:
        @dataclass
        class TimeEvent:
            name: str
            @dataclass
            class File:
                name: str
                nominal: Dict[str, Dict[str, str]] = field(default_factory=dict)
                drift_1: Dict[str, Dict[str, str]] = field(default_factory=dict)
            files: List[File] = field(default_factory=list)
        time_events: List[TimeEvent] = field(default_factory=list)
    full_margin_study: FullMarginStudy = field(default_factory=FullMarginStudy)


class GlobalResultLoader(ContentHandler):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.current_data = ""
        self.path: List[str] = []

        self.general_information: GeneralInformation = GeneralInformation(
            title="",
            Date="",
            MacVersion="",
            Project="",
            Customer="",
            UnitType="",
            ECUVersion="",
            Algorithm_version="",
            DisplacementUnit="",
            Calibration="",
            Batch_Mode_File_Name="",
            StudyType="",
            DataValidityMsg="",
            XMLFileVersion="",
            ProjectPath="",
            ECUPath=""
        )
        self.time_events: List[TimeEvent] = []
        self.time_events_df: pd.DataFrame = pd.DataFrame()
        self.calibration: List[Dict] = []
        self.calibration_configuration: List[Dict] = []
        self.calibration_display: List[Dict] = []
        self.calibration_specification: List[Dict] = []
        self.multi_preprocessing_items: List[MultiPreprocessingItem] = []
        self.project_channels: List[Channel] = []
        self.multireprocessing_tab: List[MultiPreprocessingItem] = []
        self.current_multi_preprocessing_item: Optional[MultiPreprocessingItem] = None
        self.current_time_event: Optional[MultiPreprocessingItem.PerformanceStudy.TimeEvent] = None
        self.current_distribution_time_event: Optional[MultiPreprocessingItem.TimeEventDistribution.TimeEvent] = None
        self.current_full_margin_time_event: Optional[MultiPreprocessingItem.FullMarginStudy.TimeEvent] = None
        self.current_performance_study_time_event: Optional[MultiPreprocessingItem.PerformanceStudy.TimeEvent] = None

    # 开始解析xml文件
    def startElement(self, tag, attrs):
        try:
            self.path.append(tag)
            current_path = '.'.join(self.path)

            if current_path == 'Margin_Test_Report.GeneralInformation':
                for key, value in attrs.items():
                    setattr(self.general_information, key, value)

            elif current_path.startswith('Margin_Test_Report.TimeEventInformation.TimeEvent'):
                self.time_events.append(TimeEvent(**attrs))
                self.time_events_df = pd.DataFrame(self.time_events)
                self.time_events_df.set_index('name', inplace=True)

            elif current_path.startswith('Margin_Test_Report.Calibration'):
                self.calibration.append(dict(attrs))

            elif current_path.startswith('Margin_Test_Report.CalibrationConfigurationInformation'):
                self.data_content['CalibrationConfigurationInformation'].append({})
                self.data_content['CalibrationConfigurationInformation'][-1][tag] = dict(attrs)
            
            elif current_path == 'Margin_Test_Report.MultiPreprocessingData.MultiPreprocessingItem':
                self.current_multi_preprocessing_item = MultiPreprocessingItem()
                self.multi_preprocessing_items.append(self.current_multi_preprocessing_item)
            
            elif current_path == 'Margin_Test_Report.MultiPreprocessingData.MultiPreprocessingItem.MultiPreprocessingItemInformation':
                self.current_multi_preprocessing_item.information = dict(attrs)
            
            elif current_path == 'Margin_Test_Report.MultiPreprocessingData.MultiPreprocessingItem.FileInformation.File':
                file_info = dict(attrs)
                self.current_multi_preprocessing_item.file_information.append(file_info)
                # 每次添加新的文件信息时，更新 DataFrame
                self.current_multi_preprocessing_item.file_information_df = pd.DataFrame(self.current_multi_preprocessing_item.file_information)
            
            elif current_path == 'Margin_Test_Report.MultiPreprocessingData.MultiPreprocessingItem.Mechanical.Parameter':
                param = MultiPreprocessingItem.Mechanical.Parameter(**attrs)
                self.current_multi_preprocessing_item.mechanical.parameters.append(param)
            
            elif current_path == 'Margin_Test_Report.MultiPreprocessingData.MultiPreprocessingItem.Preprocessing.Sensor':
                sensor = MultiPreprocessingItem.Preprocessing.Sensor(name=attrs['name'])
                self.current_multi_preprocessing_item.preprocessing.sensors.append(sensor)
            
            elif current_path == 'Margin_Test_Report.MultiPreprocessingData.MultiPreprocessingItem.Preprocessing.Sensor.Parameter':
                self.current_multi_preprocessing_item.preprocessing.sensors[-1].parameters.append(dict(attrs))
            
            elif current_path == 'Margin_Test_Report.MultiPreprocessingData.MultiPreprocessingItem.Preprocessing.Acquisition.Parameter':
                self.current_multi_preprocessing_item.preprocessing.acquisition.parameters.append(dict(attrs))
            
            elif current_path == 'Margin_Test_Report.MultiPreprocessingData.MultiPreprocessingItem.Drifts.Electronic.Drift':
                drift = MultiPreprocessingItem.Drifts.Electronic.Drift(**attrs)
                self.current_multi_preprocessing_item.drifts.electronic.drifts.append(drift)
            
            elif current_path == 'Margin_Test_Report.MultiPreprocessingData.MultiPreprocessingItem.PerformanceStudy.TimeEvent':
                self.current_performance_study_time_event = MultiPreprocessingItem.PerformanceStudy.TimeEvent(name=attrs['name'])
                self.current_multi_preprocessing_item.performance_study.time_events.append(self.current_performance_study_time_event)
            
            elif current_path == 'Margin_Test_Report.MultiPreprocessingData.MultiPreprocessingItem.PerformanceStudy.TimeEvent.File':
                file_info = dict(attrs)
                self.current_performance_study_time_event.files.append(file_info)
                # 每次添加新的文件信息时，更新 DataFrame
                self.current_performance_study_time_event.df = pd.DataFrame(self.current_performance_study_time_event.files)

                # 更新 time_events_dict
                self.current_multi_preprocessing_item.performance_study.time_events_dict[self.current_performance_study_time_event.name] = self.current_performance_study_time_event.df

            # ... 添加 TimeEventDistribution 和 FullMarginStudy 的解析逻辑 ...

            self.current_data = tag
        except Exception as e:
            self.logger.error(f"Error in startElement for tag {tag}: {str(e)}")

    def endElement(self, tag):
        try:
            self.path.pop()
            self.current_data = ""
        except Exception as e:
            self.logger.error(f"Error in endElement for tag {tag}: {str(e)}")

    def characters(self, content):
        try:
            if content.strip():
                current_path = '.'.join(self.path)
                if current_path.startswith('Margin_Test_Report.GeneralInformation'):
                    self.data_content['Margin_Test_Report.GeneralInformation'][self.current_data] = content.strip()
                # 其他元素的文本内容处理可以根据需要添加
        except Exception as e:
            self.logger.error(f"Error in characters: {str(e)}")

    def get_data(self):
        """
        此方法返回一个字典,包含所有从XML文件中提取的数据。

        返回:
        dict: 包含以下键值对的字典:
            - "GeneralInformation": GeneralInformation对象
            - "TimeEventInformation": TimeEvent对象列表
            - "Calibration": 字典列表
            - "CalibrationConfigurationInformation": 字典列表
            - "CalibrationDisplayInformation": 字典列表
            - "CalibrationSpecificationInformation": 字典列表
            - "MultiPreprocessingData": 字典列表
            - "Channels": 包含两个键的字典:
                - "ProjectChannels": Channel对象列表
                - "MultireprocessingTab": Channel对象列表

        使用示例:
        loader = GlobalResultLoader()
        parser = make_parser()
        parser.setContentHandler(loader)
        parser.parse("your_xml_file.xml")
        data = loader.get_data()
        print(data["GeneralInformation"].Date)
        """
        data = {
            "GeneralInformation": self.general_information,
            "TimeEventInformation": self.time_events,
            "TimeEventInformation_df": self.time_events_df,
            "Calibration": self.calibration,
            "CalibrationConfigurationInformation": self.calibration_configuration,
            "CalibrationDisplayInformation": self.calibration_display,
            "CalibrationSpecificationInformation": self.calibration_specification,
            "MultiPreprocessingData": self.multi_preprocessing_items,
            "Channels": {
                "ProjectChannels": self.project_channels,
                "MultireprocessingTab": self.multireprocessing_tab
            }
        }
        return data

    def print_summary(self):
        old_stdout = sys.stdout
        result = StringIO()
        sys.stdout = result
        
        print_general_information(self.general_information)
        print_time_event_information(self.time_events)
        
        sys.stdout = old_stdout
        return result.getvalue()

def load_global_result(xml_file_path):
    handler = GlobalResultLoader()
    parser = make_parser()
    parser.setContentHandler(handler)

    try:
        # 使用 utf-8 编码打开 XML 文件
        with open(xml_file_path, 'r', encoding='utf-8') as xml_file:
            parser.parse(xml_file)
        return handler

    except Exception as e:
        print(f"解析过程中发生错误: {str(e)}")
        return None

def print_general_information(general_info):
    data = [
        ["Date", general_info.Date],
        ["MAC Version", general_info.MacVersion],
        ["Program", general_info.Project],
        ["Customer", general_info.Customer],
        ["AlgoVersion", general_info.Algorithm_version],
        ["Calibration File", general_info.Calibration.split("\\")[-1]],
    ]
    
    print("\n一般信息:")
    print(tabulate(data, headers=["Key", "Value"], tablefmt="grid"))

def print_time_event_information(time_events):
    data = [
        [event.name, event.description, event.compute_displacement, event.algorithm, event.category]
        for event in time_events
    ]
    
    print("\nTime Event Information:")
    print(tabulate(data, headers=["Name", "Description", "Compute Displacement", "Algorithm", "Category"], tablefmt="grid"))


if __name__ == "__main__":
    xml_file_path = r"./tests/EH3_23MY_F01_Crash_TTF&Gain_Backup_MS_20230828_Global Result.xml"
    result = load_global_result(xml_file_path)
    multi_preprocessing_items = result.get_data()["MultiPreprocessingData"]
    names = [item.information.get('Name') for item in multi_preprocessing_items]
    print(result.get_data()["MultiPreprocessingData"][0])
    #print(result.get_data()["MultiPreprocessingData"][1].information.get("Name"))
    #print(names)