from hedra import (
	Setup,
	Execute,
	action,
	Analyze,
	JSONConfig,
	Submit,
	depends,
)

class SetupStage(Setup):
    batch_size=1000
    total_time='1m'


@depends(SetupStage)
class ExecuteStage(Execute):

    @action()
    async def http_get(self):
        return await self.client.http.get('')


@depends(ExecuteStage)
class AnalyzeStage(Analyze):
    pass


@depends(AnalyzeStage)
class SubmitResultsStage(Submit):
    config=JSONConfig(
        events_filepath='./events.json',
        metrics_filepath='./metrics.json'
    )
