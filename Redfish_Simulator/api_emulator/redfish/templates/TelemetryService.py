# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


import copy
import strgen
from api_emulator.utils import replace_recurse

_TEMPLATE = \
{
   "@odata.type": "#TelemetryService.v1_3_4.TelemetryService",
   "Id": "TelemetryService",
   "Name": "Telemetry Service",
   "Status": {
        "State": "Enabled",
        "Health": "OK"
   },
   "ServiceEnabled": True,
   "SupportedCollectionFunctions": [
   "Average",
   "Minimum",
   "Maximum"
   ],
   "MetricDefinitions": {
        "@odata.id": "/redfish/v1/TelemetryService/MetricDefinitions"
   },
   "MetricReportDefinitions": {
        "@odata.id": "/redfish/v1/TelemetryService/MetricReportDefinitions"
   },
   "MetricReports": {
        "@odata.id": "/redfish/v1/TelemetryService/MetricReports"
   },
   "Actions": {
       "#TelemetryService.SubmitTestMetricReport": {
            "target": "/redfish/v1/TelemetryService/Actions/TelemetryService.SubmitTestMetricReport"
        } ,
        "#TelemetryService.ClearMetricReports": {
            "target": "/redfish/v1/TelemetryService/Actions/TelemetryService.ClearMetricReports"
        } ,
        "#TelemetryService.ResetMetricReportDefinitionsToDefaults": {
            "target": "/redfish/v1/TelemetryService/Actions/TelemetryService.ResetMetricReportDefinitionsToDefaults"
        }
    } ,
    "@odata.id": "/redfish/v1/TelemetryService"
}

def get_TelemetryService_instance(wildcards):
    c = copy.deepcopy(_TEMPLATE)
    #replace_recurse(c, wildcards)
    return c
