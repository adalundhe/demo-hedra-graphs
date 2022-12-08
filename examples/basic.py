from hedra import (
    action,
    depends,
    Execute,
    Setup,
    Submit,
    Analyze,
    JSONConfig
)


class StageFourSetup(Setup):
    batch_size=2000
    total_time="15s"



@depends(StageFourSetup)
class StageFour(Execute):

    @action()
    async def httpbin_get(self):
        return await self.client.http.get('https://httpbin.org/get')
        

@depends(StageFour)
class AnalyzeResults(Analyze):
    pass


@depends(AnalyzeResults)
class JSONResults(Submit):
    config=JSONConfig(
        events_filepath='./events.json',
        metrics_filepath='./metrics.json'
    )
