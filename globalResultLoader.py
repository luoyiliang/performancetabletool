# coding: utf-8
# Author: Roy Luo

# 使用python.sax解析xml文件
from xml.sax import make_parser
from xml.sax.handler import ContentHandler

class GlobalResultLoader(ContentHandler):
    def __init__(self):
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
        # 顶级元素在self.data_content中定义了
        # 现在需要做的就是依照self.data_content的定义，将解析到的内容存储到self.data_content中
        if tag in self.data_content:
            # 这里需要逐个处理
            if tag == "GeneralInformation":
                # 解析
                for key, value in attrs.items():
                    self.data_content["GeneralInformation"][key] = value
            elif tag == "TimeEventInformation":
                self.data_content["TimeEventInformation"].append({
                    "name": attrs.get("name"),
                    "description": attrs.get("description"),
                    "compute_displacement": attrs.get("compute_displacement"),
                    "algorithm": attrs.get("algorithm"),
                    "category": attrs.get("category")
                })
            elif tag == "Calibration":
                self.data_content["Calibration"].append({
                    "name": attrs.get("name"),
                    "description": attrs.get("description"),
                    "unit": attrs.get("unit"),
                    "value": attrs.get("value"),
                    "value_hex": attrs.get("value_hex"),
                    "lock_state": attrs.get("lock_state"),
                    "neutral_value": attrs.get("neutral_value")
                })
            elif tag == "CalibrationConfigurationInformation":
                pass
            elif tag == "CalibrationDisplayInformation":
                pass
            elif tag == "CalibrationSpecificationInformation":
                pass
            elif tag == "MultiPreprocessingData":
                # 在当前的MultiPreprocessingData中，可能存在多个MultipreprocessingItem，所以需要使用列表进行存储
                # 每个MultipreprocessingItem中，信息的结构是固定的
                # 例如，下面表示一个MultiPreprocessingItem，不同的锁进代表层级。
                # MultiPreprocessingItem
                #  MultiPreprocessingItemInformation
                #  FileInformation
                #  Mechanical
                #  Preprocessing
                #  Acquisition
                #  Drifts
                #  PerformaceStudy
                #  TimeEventDistribution

                # 在解析的时候，需要使用递归的方式进行解析
                # 例如，在解析MultiPreprocessingItemInformation的时候，需要解析MultiPreprocessingItemInformation下的所有内容
                # 在解析FileInformation的时候，需要解析FileInformation下的所有内容
                # 在解析Mechanical的时候，需要解析Mechanical下的所有内容
                # 在解析Preprocessing的时候，需要解析Preprocessing下的所有内容
                # 在解析Acquisition的时候，需要解析Acquisition下的所有内容
                # 在解析Drifts的时候，需要解析Drifts下的所有内容
                # 在解析PerformaceStudy的时候，需要解析PerformaceStudy下的所有内容
                # 在解析TimeEventDistribution的时候，需要解析TimeEventDistribution下的所有内容  

                self.data_content["MultiPreprocessingData"].append({
                    "MultiPreprocessingItem": {
                        # MultiPreprocessingItemInformation中包含的元素有：
                        # 1. Name
                        # 2. Vehicle
                        # 3. Preprocessing
                        # 4. Acquisition
                        # 5. File_List
                        # 6. Mechanical_Computation_Mode
                        # 7. Statistical_Computation_Mode
                        # 8. Iteration_NumberForOneFileValid
                        "MultiPreprocessingItemInformation": {
                            "Name": attrs.get("name"),
                            "Vehicle": attrs.get("vehicle"),
                            "Preprocessing": attrs.get("preprocessing"),
                            "Acquisition": attrs.get("acquisition"),
                            "File_List": attrs.get("file_list"),
                            "Mechanical_Computation_Mode": attrs.get("mechanical_computation_mode"),
                            "Statistical_Computation_Mode": attrs.get("statistical_computation_mode"),
                            "Iteration_NumberForOneFileValid": attrs.get("iteration_number_for_one_file_valid")
                        },
                        # FileInformation中包含多个File，每个File包含如下字段
                        # 1. name
                        # 2. CrashSpeed
                        # 3. CrashSpeedUnit
                        # 4. TestDescription
                        # 5. LeftRightHandDrivenCar
                        # 6. TestReference
                        # 7. VehicleCode
                        # 8. VehicleSpeed
                        # 9. SideOfImpact
                        # 10. EventCode
                        # 11. TestPhase
                        # 12. NumberOfChannels
                        # 13. UnitType
                        # 14. ChannelsOrientation
                        # 15. InstrumentationNumber
                        # 16. ImpactSpeedUnit
                        # 17. ImpactSpeed
                        "FileInformation": {
                            
                        },
                        "Mechanical": {},
                        "Preprocessing": {},
                        "Acquisition": {},
                        "Drifts": {},
                        "PerformaceStudy": {},
                        "TimeEventDistribution": {}
                    }
                })


            elif tag == "Channels":
                pass