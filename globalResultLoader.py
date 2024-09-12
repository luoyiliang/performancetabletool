# coding: utf-8
# Author: Roy Luo

# 使用python.sax解析xml文件
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
import logging

class GlobalResultLoader(ContentHandler):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.current_data = ""
        self.data_content = {
            "GeneralInformation": {
                "title": "",
                "Date": "",
                "MacVersion": "",
                "Project": "",
                "Customer": "",
                "UnitType": "",
                "ECUVersion": "",
                "Algorithm_version": "",
                "DisplacementUnit": "",
                "Calibration":"",
                "Batch_Mode_File_Name":"",
                "StudyType":"",
                "DataValidityMsg":"",
                "XMLFileVersion":"",
                "ProjectPath":"",
                "ECUPath":""},
            "TimeEventInformation":[],
            "Calibration":[],
            "CalibrationConfigurationInformation":[],
            "CalibrationDisplayInformation":[],
            "CalibrationSpecificationInformation":[],
            "MultiPreprocessingData":[],
            "Channels":{
                "ProjectChannels":[],
                "MultireprocessingTab":[]
            }
        }

    # 开始解析xml文件
    def startElement(self, tag, attrs):
        try:
            self.path.append(tag)
            current_path = '.'.join(self.path)

            if current_path == 'GeneralInformation':
                for key, value in attrs.items():
                    self.data_content['GeneralInformation'][key] = value
            
            elif current_path == 'TimeEventInformation.TimeEvent':
                self.data_content['TimeEventInformation'].append(dict(attrs))
            
            elif current_path == 'Calibration.CalibrationItem':
                self.data_content['Calibration'].append(dict(attrs))
            
            elif current_path.startswith('CalibrationConfigurationInformation'):
                if len(self.path) == 2:
                    self.data_content['CalibrationConfigurationInformation'].append({})
                self.data_content['CalibrationConfigurationInformation'][-1][tag] = dict(attrs)
            
            elif current_path.startswith('CalibrationDisplayInformation'):
                if len(self.path) == 2:
                    self.data_content['CalibrationDisplayInformation'].append({})
                self.data_content['CalibrationDisplayInformation'][-1][tag] = dict(attrs)
            
            elif current_path.startswith('CalibrationSpecificationInformation'):
                if len(self.path) == 2:
                    self.data_content['CalibrationSpecificationInformation'].append({})
                self.data_content['CalibrationSpecificationInformation'][-1][tag] = dict(attrs)
            
            elif current_path.startswith('MultiPreprocessingData'):
                if len(self.path) == 2:
                    self.data_content['MultiPreprocessingData'].append({})
                current_item = self.data_content['MultiPreprocessingData'][-1]
                for sub_path in self.path[2:]:
                    if sub_path not in current_item:
                        current_item[sub_path] = {}
                    current_item = current_item[sub_path]
                current_item.update(dict(attrs))
            
            elif current_path.startswith('Channels'):
                if current_path == 'Channels.ProjectChannels.Channel':
                    self.data_content['Channels']['ProjectChannels'].append(dict(attrs))
                elif current_path == 'Channels.MultireprocessingTab.Channel':
                    self.data_content['Channels']['MultireprocessingTab'].append(dict(attrs))

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
                if current_path.startswith('GeneralInformation'):
                    self.data_content['GeneralInformation'][self.current_data] = content.strip()
                # 其他元素的文本内容处理可以根据需要添加
        except Exception as e:
            self.logger.error(f"Error in characters: {str(e)}")

    def get_data(self):
        return self.data_content


def main():
    handler = GlobalResultLoader()
    parser = make_parser()
    parser.setContentHandler(handler)
    
if __name__ == "__main__":
    main()