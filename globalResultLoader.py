# coding: utf-8
# Author: Roy Luo

import logging
from dataclasses import dataclass, field
from typing import List, Dict
# 使用python.sax解析xml文件
from xml.sax import make_parser
from xml.sax.handler import ContentHandler


@dataclass
class GeneralInformation:
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
    @dataclass
    class Mechanical:
        @dataclass
        class MechanicalParameter:
            name: str
            description: str
            unit: str
            value: float
        parameters: List[MechanicalParameter] = field(default_factory=list)

    information: Dict[str, str] = field(default_factory=dict)
    file_information: Dict[str, str] = field(default_factory=dict)
    mechanical: Mechanical = field(default_factory=Mechanical)
        

    @dataclass
    class Preprocessing:
        @dataclass
        class Sensor:
            name: str
            description: str
            unit: str
            value: str


class GlobalResultLoader(ContentHandler):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.current_data = ""
        self.path: List[str] = []

        self.general_information: GeneralInformation = GeneralInformation()
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
            '''
            elif current_path.startswith('Margin_Test_Report.CalibrationDisplayInformation'):
                if len(self.path) == 2:
                    self.data_content['Margin_Test_Report.CalibrationDisplayInformation'].append({})
                self.data_content['Margin_Test_Report.CalibrationDisplayInformation'][-1][tag] = dict(attrs)
            
            elif current_path.startswith('Margin_Test_Report.CalibrationSpecificationInformation'):
                if len(self.path) == 2:
                    self.data_content['Margin_Test_Report.CalibrationSpecificationInformation'].append({})
                self.data_content['Margin_Test_Report.CalibrationSpecificationInformation'][-1][tag] = dict(attrs)
            
            elif current_path.startswith('Margin_Test_Report.MultiPreprocessingData'):
                if len(self.path) == 2:
                    self.data_content['Margin_Test_Report.MultiPreprocessingData'].append({})
                current_item = self.data_content['Margin_Test_Report.MultiPreprocessingData'][-1]
                for sub_path in self.path[2:]:
                    if sub_path not in current_item:
                        current_item[sub_path] = {}
                    current_item = current_item[sub_path]
                current_item.update(dict(attrs))
            
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
        pass


def main(xml_file_path):
    handler = GlobalResultLoader()
    parser = make_parser()
    parser.setContentHandler(handler)

    try:
        parser.parse(xml_file_path)
        handler.print_summary()

        data = handler.get_data()
        print(data["GeneralInformation"].Date)
        return data  # 返回解析后的数据

    except Exception as e:
        print(f"解析过程中发生错误: {str(e)}")
        return None


if __name__ == "__main__":
    xml_file_path = r"testUsing.xml"
    result = main(xml_file_path)
