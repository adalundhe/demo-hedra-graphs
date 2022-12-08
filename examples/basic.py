from hedra import (
    action,
    depends,
    Execute,
    Setup,
    Submit,
    Analyze,
)
from xml_reporter import (
    XMLReporter,
    XMLReporterConfig
)


class StageFourSetup(Setup):
    batch_size=8000
    total_time="1m"



@depends(StageFourSetup)
class StageFour(Execute):

    @action()
    async def httpbin_get(self):
        return await self.client.http.get('https://httpbin.org/get')
        

@depends(StageFour)
class AnalyzeResults(Analyze):
    pass


@depends(AnalyzeResults)
class XMLResults(Submit):
    config=XMLReporterConfig(
        events_filepath='./events.xml',
        metrics_filepath='./metrics.xml'
    )
    plugins={
        'xml': XMLReporter
    }
