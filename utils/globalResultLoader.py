# coding: utf-8
# Author: Roy Luo

import logging
from dataclasses import dataclass, field
from typing import List, Dict
# 使用python.sax解析xml文件
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
from tabulate import tabulate
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
    file_information: Dict[str, str] = field(default_factory=dict)
    @dataclass
    class Mechanical:
        @dataclass
        class MechanicalParameter:
            name: str
            description: str
            unit: str
            value: float
        parameters: List[MechanicalParameter] = field(default_factory=list)
    mechanical: Mechanical = field(default_factory=Mechanical)

    @dataclass
    class Preprocessing:
        # 这部分暂时用不到
        @dataclass
        class Sensor:
            name: str
            description: str
            unit: str
            value: str
    @dataclass
    class Drifts:
        pass

    @dataclass
    class PerformanceStudy:
        # 这个类用于解构performance study,这个节点是MultiPreprocessingData下的一个子节点
        '''
        这个节点参考xml段如下
        <PerformanceStudy>
        <TimeEvent name="DR1">
            <File name="EH3_FLC_15KORB_20230417_LSB_2K_HCR8" min="40.5" nom="40.5" max="40.5" NF_presence="0" opt_min="-1" opt_nom="-1" opt_max="-1"/>
            <File name="EH3_FLV_15K_ORB_20230814_LSB_2K_HCR8" min="55.5" nom="55.5" max="55.5" NF_presence="0" opt_min="-1" opt_nom="-1" opt_max="-1"/>
            <File name="EH3_FCC_25KFFB_20230418_LSB_2K_HCR8" min="35" nom="35" max="35" NF_presence="0" opt_min="-1" opt_nom="25" opt_max="-1"/>
        </TimeEvent>
        <TimeEvent name="PA1">
            <File name="EH3_FLC_15KORB_20230417_LSB_2K_HCR8" min="40.5" nom="40.5" max="40.5" NF_presence="0" opt_min="-1" opt_nom="-1" opt_max="-1"/>
            <File name="EH3_FLC_15KORB_20230417_LSB_2K_HCR8" min="40.5" nom="40.5" max="40.5" NF_presence="0" opt_min="-1" opt_nom="-1" opt_max="-1"/>
            <File name="EH3_FLV_15K_ORB_20230814_LSB_2K_HCR8" min="55.5" nom="55.5" max="55.5" NF_presence="0" opt_min="-1" opt_nom="-1" opt_max="-1"/>
        </TimeEvent>
        </PerformanceStudy>
        '''
        @dataclass
        class TimeEvent:
            name:str
            # 定义File类，用于存储PerformanceStudy节点下的File节点信息
            @dataclass
            class File:
                name: str
                min: float
                nom: float
                max: float
                NF_presence: float
                opt_min: float
                opt_nom: float
                opt_max: float
            files: List[File] = field(default_factory=list)
            


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
        self.calibration: List[Dict] = []
        self.calibration_configuration: List[Dict] = []
        self.calibration_display: List[Dict] = []
        self.calibration_specification: List[Dict] = []
        self.multi_preprocessing_data: List[Dict] = []
        self.project_channels: List[Channel] = []
        self.multireprocessing_tab: List[MultiPreprocessingItem] = []

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

            elif current_path.startswith('Margin_Test_Report.Calibration'):
                self.calibration.append(dict(attrs))

            elif current_path.startswith('Margin_Test_Report.CalibrationConfigurationInformation'):
                self.data_content['CalibrationConfigurationInformation'].append({})
                self.data_content['CalibrationConfigurationInformation'][-1][tag] = dict(attrs)
            
            elif current_path.startswith('Margin_Test_Report.MultiPreprocessingData'):
                # 依照定义好的MultiPreprocessingItem类进行处理
                #self.multi_preprocessing_data.append(MultiPreprocessingItem(**attrs))
                pass
            '''
            elif current_path.startswith('Margin_Test_Report.Channels'):
                if current_path == 'Margin_Test_Report.Channels.ProjectChannels.Channel':
                    self.data_content['Margin_Test_Report.Channels']['ProjectChannels'].append(dict(attrs))
                elif current_path == 'Margin_Test_Report.Channels.MultireprocessingTab.Channel':
                    self.data_content['Margin_Test_Report.Channels']['MultireprocessingTab'].append(dict(attrs))
            '''
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
        return {
            "GeneralInformation": self.general_information,
            "TimeEventInformation": self.time_events,
            "Calibration": self.calibration,
            "CalibrationConfigurationInformation": self.calibration_configuration,
            "CalibrationDisplayInformation": self.calibration_display,
            "CalibrationSpecificationInformation": self.calibration_specification,
            "MultiPreprocessingData": self.multi_preprocessing_data,
            "Channels": {
                "ProjectChannels": self.project_channels,
                "MultireprocessingTab": self.multireprocessing_tab
            }
        }

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
        parser.parse(xml_file_path)
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
    xml_file_path = r"./tests/testUsing.xml"
    result = load_global_result(xml_file_path)
