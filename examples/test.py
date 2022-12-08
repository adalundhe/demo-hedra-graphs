# from hedra import (
# 	Setup,
# 	Execute,
# 	Analyze,
# 	Submit,
# 	JSONConfig,
# 	action,
# )

# class SetupStage(Setup):
#     batch_size=1000
#     total_time='1m'


# class ExecuteStage(Execute):

#     @action()
#     async def http_get(self):
#         return await self.client.http.get('')


# class AnalyzeStage(Analyze):
#     pass


# class SubmitResultsStage(Submit):
#     config=JSONConfig(
#         events_filepath='./events.json',
#         metrics_filepath='./metrics.json'
#     )
